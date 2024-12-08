import unittest
from ds_toolkit.heap import BinaryMinHeap


class TestBinaryMinHeap(unittest.TestCase):
    def setUp(self):
        """Initialize a new Binary Min Heap for each test."""
        self.heap = BinaryMinHeap()

    def test_insert_and_get_min(self):
        """Test inserting values and getting the minimum value."""
        self.heap.insert(10)
        self.heap.insert(20)
        self.heap.insert(5)
        self.assertEqual(self.heap.get_min(), 5)

    def test_extract_min(self):
        """Test extracting the minimum value."""
        values = [10, 20, 5, 7, 15]
        for val in values:
            self.heap.insert(val)

        min_val = self.heap.extract_min()
        self.assertEqual(min_val, 5)
        self.assertEqual(self.heap.get_min(), 7)

    def test_heap_property_after_extraction(self):
        """Ensure the heap property is maintained after extraction."""
        values = [10, 15, 5, 7, 20]
        for val in values:
            self.heap.insert(val)

        extracted = []
        while not self.heap.is_empty():
            extracted.append(self.heap.extract_min())

        self.assertEqual(extracted, [5, 7, 10, 15, 20])

    def test_is_empty(self):
        """Test checking if the heap is empty."""
        self.assertTrue(self.heap.is_empty())
        self.heap.insert(10)
        self.assertFalse(self.heap.is_empty())

    def test_size(self):
        """Test getting the size of the heap."""
        self.assertEqual(self.heap.size(), 0)
        self.heap.insert(10)
        self.heap.insert(20)
        self.assertEqual(self.heap.size(), 2)

    def test_to_list(self):
        """Test converting the heap to a list."""
        values = [10, 15, 5, 7, 20]
        for val in values:
            self.heap.insert(val)
        heap_list = self.heap.to_list()
        self.assertIn(5, heap_list)
        self.assertIn(20, heap_list)
        self.assertEqual(len(heap_list), 5)

    def test_extract_from_empty_heap(self):
        """Test extracting from an empty heap raises an error."""
        with self.assertRaises(IndexError):
            self.heap.extract_min()

    def test_get_min_from_empty_heap(self):
        """Test getting the minimum value from an empty heap raises an error."""
        with self.assertRaises(IndexError):
            self.heap.get_min()


if __name__ == "__main__":
    unittest.main()
