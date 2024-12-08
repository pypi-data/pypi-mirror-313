import unittest
from ds_toolkit.singly_linked_list import SinglyLinkedList


class TestSinglyLinkedList(unittest.TestCase):
    def setUp(self):
        """Initialize a new Singly Linked List for each test."""
        self.sll = SinglyLinkedList()

    def test_push_front(self):
        """Test inserting nodes at the front."""
        self.sll.push_front(10)
        self.sll.push_front(20)
        self.assertEqual(self.sll.to_list(), [20, 10])

    def test_push_back(self):
        """Test inserting nodes at the back."""
        self.sll.push_back(10)
        self.sll.push_back(20)
        self.assertEqual(self.sll.to_list(), [10, 20])

    def test_pop_front(self):
        """Test removing nodes from the front."""
        self.sll.push_front(10)
        self.sll.push_front(20)
        self.assertEqual(self.sll.pop_front(), 20)
        self.assertEqual(self.sll.to_list(), [10])

    def test_find(self):
        """Test searching for nodes."""
        values = [10, 20, 30, 40]
        for val in values:
            self.sll.push_back(val)
        self.assertTrue(self.sll.find(20))
        self.assertFalse(self.sll.find(50))

    def test_pop_from_empty_list(self):
        """Test popping from an empty list."""
        with self.assertRaises(IndexError):
            self.sll.pop_front()

    def test_size(self):
        """Test getting the size of the list."""
        self.assertEqual(self.sll.size(), 0)
        self.sll.push_front(10)
        self.sll.push_back(20)
        self.assertEqual(self.sll.size(), 2)

    def test_empty_list(self):
        """Test the state of an empty list."""
        self.assertEqual(self.sll.to_list(), [])

    def test_push_and_pop_combination(self):
        """Test a combination of push and pop operations."""
        self.sll.push_front(10)
        self.sll.push_back(20)
        self.assertEqual(self.sll.pop_front(), 10)
        self.assertEqual(self.sll.pop_front(), 20)
        self.assertEqual(self.sll.to_list(), [])


if __name__ == "__main__":
    unittest.main()
