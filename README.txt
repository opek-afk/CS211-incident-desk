Incident Desk
CS211 Data Structures and Algorithm Group Assignment

เปิด Incident Desk บน Windows

1. คลิกขวาที่ CS211_Incident_Desk.zip แล้วเลือก Extract All (แยกทั้งหมด)
   เปิดโฟลเดอร์ CS211_Incident_Desk ที่แตกออกมาจนเห็นไฟล์ web_app.py

2. พิมพ์ cmd ในแถบที่อยู่ของ File Explorer แล้วกด Enter
   Command Prompt จะเปิดในโฟลเดอร์ที่มี web_app.py

3. เช็กว่ามี Python 3 โดยพิมพ์

       python --version

   ถ้าคำสั่งนี้ใช้ไม่ได้ ให้ลอง py --version
   ถ้าทั้งสองคำสั่งใช้ไม่ได้ ให้ติดตั้ง Python 3 จาก
   https://www.python.org/downloads/windows/
   จากนั้นปิด Command Prompt แล้วเปิดใหม่จากโฟลเดอร์เดิม

4. เปิดระบบด้วยคำสั่ง

       python web_app.py --open

   ถ้าเครื่องใช้คำสั่ง py ให้รัน py web_app.py --open แทน
   เบราว์เซอร์จะเปิด Incident Desk ขึ้นมาเอง ถ้าไม่เปิด ให้คัดลอก URL
   ที่ขึ้นใน Command Prompt ไปเปิด โดยปกติคือ http://127.0.0.1:8765

5. เปิด Command Prompt ค้างไว้ระหว่างใช้งาน และกด Ctrl+C เมื่อต้องการหยุดระบบ

หลังติดตั้ง Python แล้ว ระบบใช้งานออฟไลน์ได้และไม่ต้องติดตั้งแพ็กเกจเพิ่ม
สำหรับ Windows ให้เปิดระบบผ่านคำสั่งในข้อ 4 แล้วเข้าเว็บจาก URL ที่แสดง

เปิดไม่ได้บน Windows
• ขึ้น can't open file หรือหา web_app.py ไม่เจอ
  ให้กลับไปเปิด cmd จากโฟลเดอร์ที่เห็นไฟล์ web_app.py แล้วรันอีกครั้ง
• พอร์ต 8765 ถูกใช้งานอยู่
  ให้รัน python web_app.py --open --port 0 เพื่อให้ระบบเลือกพอร์ตที่ว่าง
  ถ้าใช้ py ให้เปลี่ยน python เป็น py แล้วเปิด URL ที่แสดงหลังรันคำสั่ง
• เปิด index.html แล้วขึ้นว่า “ระบบยังไม่พร้อม”
  ให้เริ่มระบบด้วยคำสั่งในข้อ 4 แล้วเปิด URL จาก Command Prompt

เปิดบน macOS
แตกไฟล์ ZIP แล้วเปิด Start.command หรือรัน python3 web_app.py --open
จาก Terminal ในโฟลเดอร์ CS211_Incident_Desk

วิธีเดโม
• เปิด “โหมดสาธิต” เพื่อทดลองด้วยข้อมูลที่เตรียมไว้
• สังเกตว่าเหตุระดับ 1 ขึ้นก่อน และเหตุระดับเดียวกันเรียงตามเวลาแจ้ง
• กด “บันทึกว่าตรวจแล้ว” เพื่อเลื่อนไปคิวถัดไปและดูผลใน “ประวัติการตรวจ”
• เปิด “โครงสร้างข้อมูล” เพื่อดูเหตุผลที่เลือกใช้ Queue และ Min-Heap พร้อม Big-O

การจัดเก็บ
ข้อมูลจริงเริ่มจากคิวว่างและถูกบันทึกใน incident-desk.sqlite3 ข้างไฟล์ระบบ
โหมดสาธิตแยกจากข้อมูลจริงและจะเริ่มใหม่เมื่อเปิดระบบใหม่

ไฟล์หลัก
• index.html — หน้าเว็บและส่วนติดต่อผู้ใช้
• web_app.py — เชื่อมหน้าเว็บกับโค้ด Python และบันทึกข้อมูลลง SQLite
• incident_queue.py และ min_heap.py — โครงสร้างข้อมูลจากโครงการเดิม
• main.py และ display.py — เมนู Command Line เดิม บน Windows รัน python main.py
• test_system.py — ชุดทดสอบเดิม บน Windows รัน python -m unittest -v
  ถ้าเครื่องใช้ py ให้แทน python ด้วย py ในสองคำสั่งข้างต้น

ข้อมูลสำหรับส่วน “การใช้ AI” ในรายงาน
AI ช่วยพัฒนาหน้าเว็บและส่วนเชื่อมต่อ รวมทั้งตรวจลำดับคิวและการบันทึกข้อมูล
คลาส Queue และ Min-Heap ใช้ไฟล์จากโครงการเดิมโดยตรง
