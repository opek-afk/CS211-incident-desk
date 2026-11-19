
from display import show_pending, show_summary
from incident_queue import Queue
from min_heap import MinHeap

# สร้างโครงสร้างข้อมูลจาก Class
normal_queue = Queue()
urgent_heap = MinHeap()

# ตัวแปรเก็บจำนวนที่ตรวจแล้ว
urgent_done = 0
normal_done = 0

# ตัวนับรหัสเหตุการณ์
next_id = 1


def add_incident():
    global next_id

    # รับรายละเอียดเหตุการณ์ใหม่
    description = input("Incident description: ").strip()

    # ตรวจสอบว่าข้อมูลไม่ว่าง
    if description == "":
        print("กรุณากรอกชื่อเหตุการณ์")
        return

    # เลือกประเภทของเหตุการณ์
    print("\n1. Normal")
    print("2. Urgent")
    type_choice = input("Choose type: ").strip()

    if type_choice not in ("1", "2"):
        print("ประเภทเหตุการณ์ไม่ถูกต้อง")
        return

    priority = None

    # ถ้าเป็น Urgent ให้รับระดับความด่วน
    if type_choice == "2":
        priority_input = input(
            "Priority (1-5, 1 is highest): "
        ).strip()

        # ตรวจสอบ Priority ก่อนแปลงเป็น int
        if priority_input not in ("1", "2", "3", "4", "5"):
            print("Priority ต้องอยู่ระหว่าง 1-5")
            return

        priority = int(priority_input)

    # กำหนดประเภทของเหตุการณ์
    if type_choice == "2":
        incident_type = "urgent"
    else:
        incident_type = "normal"

    # สร้าง Dictionary เก็บเหตุการณ์
    incident = {
        "id": f"INC{next_id:03d}",
        "description": description,
        "type": incident_type,
        "priority": priority
    }

    # ส่งข้อมูลไปเก็บในโครงสร้างที่เหมาะสม
    if incident_type == "urgent":
        urgent_heap.insert(priority, incident)
    else:
        normal_queue.enqueue(incident)

    # เพิ่มหมายเลข ID สำหรับเหตุการณ์ถัดไป
    next_id += 1

    print(
        f'เพิ่มเหตุการณ์ {incident["id"]} สำเร็จ '
        f'({incident_type})'
    )


def process_next():
    global urgent_done, normal_done

    print("\n===== Process Next Incident =====")

    # ตรวจเหตุการณ์ด่วนก่อนเสมอ
    if not urgent_heap.is_empty():
        priority, incident = urgent_heap.extract_min()

        urgent_done += 1

        print("กำลังตรวจเหตุการณ์ด่วน")
        print("ID:", incident["id"])
        print("Description:", incident["description"])
        print("Priority:", priority)

    # ถ้าไม่มีเหตุการณ์ด่วน ค่อยตรวจคิวทั่วไป
    elif not normal_queue.is_empty():
        incident = normal_queue.dequeue()

        normal_done += 1

        print("กำลังตรวจเหตุการณ์ทั่วไป")
        print("ID:", incident["id"])
        print("Description:", incident["description"])

    # กรณีไม่มีเหตุการณ์เหลืออยู่
    else:
        print("ไม่มีเหตุการณ์รอตรวจ")


def main_menu():
    # วนแสดงเมนูจนกว่าผู้ใช้จะเลือกออก
    while True:
        print("\n===== Cybersecurity Incident Queue =====")
        print("1. Add Incident")
        print("2. Process Next Incident")
        print("3. View Pending Incidents")
        print("4. Incident Summary")
        print("0. Exit")

        choice = input("Choose menu: ").strip()

        if choice == "1":
            # เพิ่มเหตุการณ์ใหม่
            add_incident()

        elif choice == "2":
            # เรียกเหตุการณ์ถัดไป
            process_next()

        elif choice == "3":
            # แสดงเหตุการณ์ที่รอตรวจ
            show_pending(urgent_heap, normal_queue)

        elif choice == "4":
            # แสดงยอดสรุป
            show_summary(
                urgent_heap,
                normal_queue,
                urgent_done,
                normal_done
            )

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid menu")


# เริ่มทำงานเมื่อรันไฟล์ main.py
if __name__ == "__main__":
    main_menu()
