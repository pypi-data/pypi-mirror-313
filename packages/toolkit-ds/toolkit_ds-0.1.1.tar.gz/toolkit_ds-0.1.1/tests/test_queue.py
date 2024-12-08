import unittest
from ds_toolkit.queue import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        """Initialize a new Queue for each test."""
        self.queue = Queue()

    def test_enqueue_and_front(self):
        """Test enqueueing and getting the front element."""
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.front(), 10)

    def test_dequeue(self):
        """Test dequeuing elements from the front."""
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.dequeue(), 10)
        self.assertEqual(self.queue.front(), 20)

    def test_dequeue_from_empty_queue(self):
        """Test dequeuing from an empty queue raises an error."""
        with self.assertRaises(IndexError):
            self.queue.dequeue()

    def test_is_empty(self):
        """Test checking if the queue is empty."""
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(10)
        self.assertFalse(self.queue.is_empty())

    def test_size(self):
        """Test getting the size of the queue."""
        self.assertEqual(self.queue.size(), 0)
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.assertEqual(self.queue.size(), 2)

    def test_to_list(self):
        """Test converting the queue to a list."""
        values = [10, 20, 30]
        for val in values:
            self.queue.enqueue(val)
        queue_list = self.queue.to_list()
        self.assertEqual(queue_list, values)

    def test_front_from_empty_queue(self):
        """Test getting the front element from an empty queue raises an error."""
        with self.assertRaises(IndexError):
            self.queue.front()

    def test_multiple_enqueue_dequeue(self):
        """Test enqueueing and dequeueing multiple elements."""
        values = [10, 20, 30, 40]
        for val in values:
            self.queue.enqueue(val)

        dequeued_values = [self.queue.dequeue() for _ in range(4)]
        self.assertEqual(dequeued_values, values)

    def test_enqueue_and_dequeue_combination(self):
        """Test a combination of enqueue and dequeue operations."""
        self.queue.enqueue(10)
        self.queue.enqueue(20)
        self.queue.dequeue()
        self.queue.enqueue(30)
        self.queue.enqueue(40)
        self.assertEqual(self.queue.front(), 20)
        self.assertEqual(self.queue.size(), 3)


if __name__ == "__main__":
    unittest.main()
