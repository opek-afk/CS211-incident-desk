
# ===== Min-Heap (คิวเหตุการณ์ด่วน) =====

class MinHeap:
    def __init__(self):
        # list เป็นแค่ถังเก็บภายในคลาส
        self.items = []

        # ลำดับการเข้า ใช้ตัดสินเมื่อระดับด่วนเท่ากัน
        self.next_order = 0

    def insert(self, severity, event_name):
        # เก็บเป็น (ระดับด่วน, ลำดับเข้า, ชื่อ)
        # เทียบ tuple จากซ้ายไปขวา O(log n)

        if severity < 1 or severity > 5:
            raise ValueError("ระดับด่วนต้องอยู่ระหว่าง 1-5")

        self.items.append(
            (severity, self.next_order, event_name)
        )

        self.next_order += 1
        self._sift_up(len(self.items) - 1)

    def extract_min(self):
        # เอาเหตุการณ์ที่ด่วนที่สุดออก O(log n)
        # ถ้าว่างคืน None

        if self.is_empty():
            return None

        top = self.items[0]
        last = self.items.pop()

        if not self.is_empty():
            # เอาตัวท้ายมาแทนราก แล้วให้จมลง
            self.items[0] = last
            self._sift_down(0)

        # คืนเฉพาะ (ระดับด่วน, ชื่อ)
        return (top[0], top[2])

    def peek(self):
        # ดูตัวที่ด่วนที่สุดโดยไม่เอาออก O(1)
        if self.is_empty():
            return None

        return (self.items[0][0], self.items[0][2])

    def to_sorted_list(self):
        # ดูทั้งหมดเรียงตามลำดับที่จะถูกเรียก
        # โดยไม่แก้ heap จริง O(n log n)

        temp = MinHeap()
        temp.items = list(self.items)

        result = []

        while not temp.is_empty():
            result.append(temp.extract_min())

        return result

    def is_empty(self):
        return len(self.items) == 0

    def get_size(self):
        return len(self.items)

    def _sift_up(self, index):
        # ลอยขึ้นจนแม่น้อยกว่าลูก O(log n)

        while index > 0:
            parent = (index - 1) // 2

            if self.items[index] < self.items[parent]:
                self.items[index], self.items[parent] = (
                    self.items[parent],
                    self.items[index]
                )
                index = parent
            else:
                break

    def _sift_down(self, index):
        # จมลงจนไม่มีลูกที่น้อยกว่า O(log n)

        n = len(self.items)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.items[left] < self.items[smallest]:
                smallest = left

            if right < n and self.items[right] < self.items[smallest]:
                smallest = right

            if smallest == index:
                break

            self.items[index], self.items[smallest] = (
                self.items[smallest],
                self.items[index]
            )

            index = smallest
