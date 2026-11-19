
def show_pending(urgent_heap, normal_queue):
    # ดึงรายการจากโครงสร้างข้อมูล
    urgent_list = urgent_heap.to_sorted_list()
    normal_list = normal_queue.to_list()

    print("\n===== Pending Incidents =====")

    # แสดงเหตุการณ์ด่วน
    print("\n--- Urgent Queue ---")

    if len(urgent_list) == 0:
        print("ไม่มีเหตุการณ์ด่วน")
    else:
        for priority, incident in urgent_list:
            print(
                f'{incident["id"]} | '
                f'{incident["description"]} | '
                f'Priority: {priority}'
            )

    # แสดงเหตุการณ์ทั่วไป
    print("\n--- Normal Queue ---")

    if len(normal_list) == 0:
        print("ไม่มีเหตุการณ์ทั่วไป")
    else:
        for incident in normal_list:
            print(
                f'{incident["id"]} | '
                f'{incident["description"]}'
            )


def show_summary(urgent_heap, normal_queue,
                 urgent_done, normal_done):
    # นับเหตุการณ์ที่ยังรอตรวจจาก Queue และ Heap
    urgent_wait = urgent_heap.get_size()
    normal_wait = normal_queue.get_size()

    # คำนวณยอดรวม
    total_wait = urgent_wait + normal_wait
    total_done = urgent_done + normal_done

    print("\n===== Incident Summary =====")
    print("ด่วนรอตรวจ:", urgent_wait)
    print("ทั่วไปรอตรวจ:", normal_wait)
    print("ด่วนตรวจแล้ว:", urgent_done)
    print("ทั่วไปตรวจแล้ว:", normal_done)
    print("-------------------------")
    print("รอตรวจทั้งหมด:", total_wait)
    print("ตรวจแล้วทั้งหมด:", total_done)
