
import unittest
from incident_queue import Queue
from min_heap import MinHeap


class TestSystem(unittest.TestCase):

    def test_queue_fifo(self):
        # ทดสอบ Queue แบบมาก่อนออกก่อน
        q = Queue()

        q.enqueue({"id": "INC001"})
        q.enqueue({"id": "INC002"})

        self.assertEqual(q.dequeue()["id"], "INC001")
        self.assertEqual(q.dequeue()["id"], "INC002")

    def test_queue_empty(self):
        # ทดสอบตอน Queue ว่าง
        q = Queue()

        self.assertTrue(q.is_empty())
        self.assertIsNone(q.dequeue())

    def test_heap_priority(self):
        # ทดสอบการจัดลำดับความสำคัญ
        h = MinHeap()

        h.insert(3, {"id": "INC001"})
        h.insert(1, {"id": "INC002"})
        h.insert(2, {"id": "INC003"})

        # Priority 1 ต้องออกก่อน
        priority, incident = h.extract_min()

        self.assertEqual(priority, 1)
        self.assertEqual(incident["id"], "INC002")

    def test_heap_same_priority(self):
        # ทดสอบ Priority เท่ากัน
        h = MinHeap()

        h.insert(2, {"id": "INC001"})
        h.insert(2, {"id": "INC002"})

        # เหตุการณ์แรกต้องถูกเรียกก่อน
        self.assertEqual(h.extract_min()[1]["id"], "INC001")
        self.assertEqual(h.extract_min()[1]["id"], "INC002")

    def test_heap_empty(self):
        # ทดสอบตอน Heap ว่าง
        h = MinHeap()

        self.assertTrue(h.is_empty())
        self.assertIsNone(h.extract_min())

    def test_invalid_priority(self):
        # ทดสอบ Priority ที่เกินช่วง 1-5
        h = MinHeap()

        with self.assertRaises(ValueError):
            h.insert(6, {"id": "INC001"})

    def test_display_does_not_remove(self):
        # ทดสอบว่าแสดงรายการแล้วข้อมูลไม่หาย
        h = MinHeap()

        h.insert(2, {"id": "INC001"})
        h.insert(1, {"id": "INC002"})

        pending = h.to_sorted_list()

        self.assertEqual(len(pending), 2)
        self.assertEqual(h.get_size(), 2)
        self.assertEqual(pending[0][1]["id"], "INC002")


if __name__ == "__main__":
    unittest.main()
