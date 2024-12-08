import unittest
from ds_toolkit.doubly_linked_list import DoublyLinkedList


class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        """Initialize a new Doubly Linked List for each test."""
        self.dll = DoublyLinkedList()

    def test_push_front(self):
        """Test inserting nodes at the front."""
        self.dll.push_front(10)
        self.dll.push_front(20)
        self.assertEqual(self.dll.to_list(), [20, 10])

    def test_push_back(self):
        """Test inserting nodes at the back."""
        self.dll.push_back(10)
        self.dll.push_back(20)
        self.assertEqual(self.dll.to_list(), [10, 20])

    def test_pop_front(self):
        """Test removing nodes from the front."""
        self.dll.push_front(10)
        self.dll.push_front(20)
        self.assertEqual(self.dll.pop_front(), 20)
        self.assertEqual(self.dll.to_list(), [10])

    def test_pop_back(self):
        """Test removing nodes from the back."""
        self.dll.push_back(10)
        self.dll.push_back(20)
        self.assertEqual(self.dll.pop_back(), 20)
        self.assertEqual(self.dll.to_list(), [10])

    def test_find(self):
        """Test searching for nodes."""
        values = [10, 20, 30, 40]
        for val in values:
            self.dll.push_back(val)
        self.assertTrue(self.dll.find(20))
        self.assertFalse(self.dll.find(50))

    def test_pop_from_empty_list(self):
        """Test popping from an empty list."""
        with self.assertRaises(IndexError):
            self.dll.pop_front()
        with self.assertRaises(IndexError):
            self.dll.pop_back()

    def test_empty_list(self):
        """Test the state of an empty list."""
        self.assertEqual(self.dll.to_list(), [])

    def test_push_and_pop_combination(self):
        """Test a combination of push and pop operations."""
        self.dll.push_front(10)
        self.dll.push_back(20)
        self.assertEqual(self.dll.pop_front(), 10)
        self.assertEqual(self.dll.pop_back(), 20)
        self.assertEqual(self.dll.to_list(), [])


if __name__ == "__main__":
    unittest.main()
