import unittest
from ds_toolkit.stack import Stack


class TestStack(unittest.TestCase):
    def setUp(self):
        """Initialize a new Stack for each test."""
        self.stack = Stack()

    def test_push_and_top(self):
        """Test pushing an element and checking the top element."""
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.top(), 20)

    def test_pop(self):
        """Test popping the top element from the stack."""
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.pop(), 20)
        self.assertEqual(self.stack.top(), 10)

    def test_pop_from_empty_stack(self):
        """Test popping from an empty stack raises an error."""
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_is_empty(self):
        """Test checking if the stack is empty."""
        self.assertTrue(self.stack.is_empty())
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())

    def test_size(self):
        """Test getting the size of the stack."""
        self.assertEqual(self.stack.size(), 0)
        self.stack.push(10)
        self.stack.push(20)
        self.assertEqual(self.stack.size(), 2)

    def test_to_list(self):
        """Test converting the stack to a list."""
        values = [10, 20, 30]
        for val in values:
            self.stack.push(val)
        stack_list = self.stack.to_list()
        self.assertEqual(stack_list, values)

    def test_top_from_empty_stack(self):
        """Test getting the top element from an empty stack raises an error."""
        with self.assertRaises(IndexError):
            self.stack.top()

    def test_push_and_pop_combination(self):
        """Test a combination of push and pop operations."""
        self.stack.push(10)
        self.stack.push(20)
        self.stack.pop()
        self.stack.push(30)
        self.assertEqual(self.stack.top(), 30)
        self.assertEqual(self.stack.size(), 2)


if __name__ == "__main__":
    unittest.main()
