
# ===== Queue (คิวเหตุการณ์ทั่วไป) =====

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, event_name):
        # เพิ่มท้ายคิว O(1)
        new_node = Node(event_name)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def dequeue(self):
        # เอาหัวคิวออก O(1) ถ้าคิวว่างคืน None
        if self.is_empty():
            return None

        event_name = self.head.data
        self.head = self.head.next

        # คิวว่างแล้ว ต้องเคลียร์ tail ด้วย
        if self.head is None:
            self.tail = None

        self.size -= 1
        return event_name

    def peek(self):
        # ดูหัวคิวโดยไม่เอาออก O(1)
        if self.is_empty():
            return None

        return self.head.data

    def to_list(self):
        # ไล่ดูทั้งคิวตามลำดับ โดยไม่เอาข้อมูลออก O(n)
        result = []
        current = self.head

        while current is not None:
            result.append(current.data)
            current = current.next

        return result

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size
