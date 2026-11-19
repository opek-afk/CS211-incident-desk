"""Local web interface for the CS211 Cybersecurity Incident Queue."""

import argparse
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sqlite3
from threading import Lock, Timer
from urllib.parse import parse_qs, urlsplit
import webbrowser

from incident_queue import Queue
from min_heap import MinHeap


APP_DIR = Path(__file__).resolve().parent
MAX_DESCRIPTION = 240


class QueueChanged(Exception):
    """The browser's displayed next incident is no longer at the front."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class IncidentBoard:
    def __init__(self, database):
        self.lock = Lock()
        self.database = sqlite3.connect(database, check_same_thread=False)
        self.database.row_factory = sqlite3.Row
        self.database.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                sequence INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('urgent', 'normal')),
                priority INTEGER,
                created_at TEXT NOT NULL,
                processed_at TEXT,
                processed_order INTEGER UNIQUE,
                CHECK (
                    (type = 'normal' AND priority IS NULL) OR
                    (type = 'urgent' AND priority IS NOT NULL AND priority BETWEEN 1 AND 5)
                )
            )
        """)
        self.normal = Queue()
        self.urgent = MinHeap()
        self.history = []
        self.done_counts = {"urgent": 0, "normal": 0}
        self.next_sequence = 1

        rows = self.database.execute(
            "SELECT * FROM incidents ORDER BY processed_order, sequence"
        )
        for row in rows:
            incident = dict(row)
            incident["id"] = f"INC{incident['sequence']:03d}"
            self.next_sequence = max(self.next_sequence, incident["sequence"] + 1)
            if incident.pop("processed_order") is None:
                self._enqueue(incident)
            else:
                self._record_processed(incident)

    def _enqueue(self, incident):
        if incident["type"] == "urgent":
            self.urgent.insert(incident["priority"], incident)
        else:
            self.normal.enqueue(incident)

    def _record_processed(self, incident):
        self.history.append(incident)
        self.done_counts[incident["type"]] += 1

    def _peek(self):
        urgent = self.urgent.peek()
        return urgent[1] if urgent is not None else self.normal.peek()

    def snapshot(self):
        return {
            "next": self._peek(),
            "pending": [incident for _, incident in self.urgent.to_sorted_list()]
            + self.normal.to_list(),
            "history": list(reversed(self.history)),
            "counts": {
                "urgent": self.urgent.get_size(),
                "normal": self.normal.get_size(),
                "urgent_done": self.done_counts["urgent"],
                "normal_done": self.done_counts["normal"],
            },
        }

    def add(self, description, incident_type, priority=None):
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= MAX_DESCRIPTION:
            raise ValueError("กรอกรายละเอียดเหตุการณ์ 1–240 ตัวอักษร")
        if incident_type not in ("normal", "urgent"):
            raise ValueError("เลือกประเภทเหตุการณ์")
        if incident_type == "urgent":
            if type(priority) is not int or not 1 <= priority <= 5:
                raise ValueError("เลือกระดับความด่วน 1–5")
        else:
            priority = None

        sequence = self.next_sequence
        incident = {
            "sequence": sequence,
            "id": f"INC{sequence:03d}",
            "description": description.strip(),
            "type": incident_type,
            "priority": priority,
            "created_at": now(),
            "processed_at": None,
        }
        with self.database:
            self.database.execute("""
                INSERT INTO incidents (sequence, description, type, priority, created_at)
                VALUES (:sequence, :description, :type, :priority, :created_at)
            """, incident)

        self._enqueue(incident)
        self.next_sequence += 1
        return incident

    def process_next(self, expected_id):
        incident = self._peek()
        if incident is None or incident["id"] != expected_id:
            raise QueueChanged("คิวถัดไปเปลี่ยนแล้ว กรุณาตรวจสอบรายการล่าสุด")

        completed = {**incident, "processed_at": now()}
        with self.database:
            self.database.execute("""
                UPDATE incidents SET processed_at = ?, processed_order = ?
                WHERE sequence = ?
            """, (completed["processed_at"], len(self.history) + 1, incident["sequence"]))

        if incident["type"] == "urgent":
            self.urgent.extract_min()
        else:
            self.normal.dequeue()
        self._record_processed(completed)
        return completed


def make_demo_board():
    board = IncidentBoard(":memory:")
    completed = [
        ("ตรวจสอบการแจ้งเตือนจากโปรแกรมป้องกันไวรัส", "urgent", 3),
        ("ตรวจสอบสิทธิ์เข้าโฟลเดอร์ของพนักงานใหม่", "normal", None),
        ("ตรวจสอบสถานะการสำรองข้อมูลประจำวัน", "normal", None),
    ]
    for description, incident_type, priority in completed:
        incident = board.add(description, incident_type, priority)
        board.process_next(incident["id"])

    board.add("แจ้งอีเมลน่าสงสัยจากฝ่ายบัญชี", "urgent", 2)
    board.add("ตรวจสอบอุปกรณ์ที่ไม่ได้ลงทะเบียนในเครือข่าย", "normal")
    board.add("พบการเข้าสู่ระบบผิดปกติในบัญชีผู้ดูแล", "urgent", 1)
    board.add("ตรวจสอบรายการซอฟต์แวร์บนเครื่องสำนักงาน", "normal")
    board.add("แจ้งไฟล์แนบผิดปกติจากฝ่ายจัดซื้อ", "urgent", 2)
    board.add("ตรวจสอบการแจ้งเตือนจากเครื่องปลายทาง", "urgent", 4)
    return board


class DeskServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, database):
        super().__init__(address, DeskHandler)
        try:
            self.page = (APP_DIR / "index.html").read_bytes()
            self.boards = {"live": IncidentBoard(database), "demo": make_demo_board()}
        except BaseException:
            self.server_close()
            raise


class DeskHandler(BaseHTTPRequestHandler):
    def _send(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
            "connect-src 'self'; base-uri 'none'; form-action 'self'",
        )
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, "application/json; charset=utf-8", body)

   
    def _route(self):
        port = self.server.server_port
        hosts = {
            f"127.0.0.1:{port}",
            f"localhost:{port}"
        }

        public_host = os.environ.get(
            "RENDER_EXTERNAL_HOSTNAME", ""
        ).lower()

        if public_host:
            hosts.add(public_host)
            hosts.add(f"{public_host}:443")

        if self.headers.get("Host") not in hosts:
            self._json(
                HTTPStatus.FORBIDDEN,
                {"error": "ไม่อนุญาตให้เข้าถึงผ่าน URL นี้"}
            )
            return None

        return urlsplit(self.path)



    def _board(self, route):
        mode = parse_qs(route.query).get("mode", ["live"])[0]
        board = self.server.boards.get(mode)
        if board is None:
            self._json(HTTPStatus.BAD_REQUEST, {"error": "โหมดการใช้งานไม่ถูกต้อง"})
        return board

    def do_GET(self):
        route = self._route()
        if route is None:
            return
        if route.path in ("/", "/index.html"):
            self._send(HTTPStatus.OK, "text/html; charset=utf-8", self.server.page)
        elif route.path == "/api/state":
            board = self._board(route)
            if board is not None:
                with board.lock:
                    self._json(HTTPStatus.OK, board.snapshot())
        elif route.path == "/favicon.ico":
            self._send(HTTPStatus.NO_CONTENT, "image/x-icon", b"")
        else:
            self._json(HTTPStatus.NOT_FOUND, {"error": "ไม่พบหน้าที่ต้องการ"})

    def do_POST(self):
        route = self._route()
        if route is None:
            return
        if route.path not in ("/api/incidents", "/api/process"):
            self._json(HTTPStatus.NOT_FOUND, {"error": "ไม่พบคำสั่งที่ต้องการ"})
            return

        board = self._board(route)
        if board is None:
            return
        if self.headers.get_content_type() != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "รองรับข้อมูลรูปแบบ JSON"})
            return
        try:
            length = int(self.headers.get("Content-Length", -1))
            if not 0 < length <= 4096:
                raise ValueError("ขนาดข้อมูลไม่ถูกต้อง")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("ข้อมูลต้องเป็นออบเจ็กต์ JSON")
        except (ValueError, UnicodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "อ่านข้อมูลที่ส่งมาไม่ได้"})
            return

        with board.lock:
            try:
                if route.path == "/api/incidents":
                    incident = board.add(
                        payload.get("description"), payload.get("type"), payload.get("priority")
                    )
                    status = HTTPStatus.CREATED
                else:
                    incident = board.process_next(payload.get("id"))
                    status = HTTPStatus.OK
                self._json(status, {"incident": incident, "state": board.snapshot()})
            except QueueChanged as error:
                self._json(HTTPStatus.CONFLICT, {"error": str(error), "state": board.snapshot()})
            except ValueError as error:
                self._json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            except sqlite3.Error:
                self._json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "บันทึกข้อมูลไม่สำเร็จ กรุณาลองอีกครั้ง"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--database", default=str(APP_DIR / "incident-desk.sqlite3"))
    parser.add_argument("--open", action="store_true", help="Open the browser on startup")
    options = parser.parse_args()
    try:
        with DeskServer((options.host, options.port), options.database) as server:
            url = f"http://127.0.0.1:{server.server_port}"
            print(f"Incident Desk: {url}  (Ctrl+C to stop)", flush=True)
            if options.open:
                browser = Timer(0.2, webbrowser.open, args=(url,))
                browser.daemon = True
                browser.start()
            server.serve_forever()
    except KeyboardInterrupt:
        return
    except (OSError, sqlite3.Error) as error:
        parser.exit(1, f"Incident Desk could not start: {error}\n")


if __name__ == "__main__":
    main()
