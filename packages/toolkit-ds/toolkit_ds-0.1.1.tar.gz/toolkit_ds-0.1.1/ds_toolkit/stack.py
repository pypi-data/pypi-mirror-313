class Stack:
    """Stack implementation using a list."""

    def __init__(self):
        self._stack = []

    def push(self, value):
        """Push an element onto the stack."""
        self._stack.append(value)

    def pop(self):
        """Pop the top element from the stack."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self._stack.pop()

    def top(self):
        """Return the top element of the stack without removing it."""
        if self.is_empty():
            raise IndexError("Top from an empty stack")
        return self._stack[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._stack) == 0

    def size(self):
        """Return the size of the stack."""
        return len(self._stack)

    def to_list(self):
        """Return the stack as a list."""
        return self._stack[:]


class LinkedListStack:
    """Stack implementation using a linked list."""

    class Node:
        """A simple Node class for the linked list."""
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.top = None
        self.size = 0

    def is_empty(self):
        """Check if the stack is empty."""
        return self.size == 0

    def push(self, value):
        """Push an element onto the stack."""
        new_node = self.Node(value)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        """Pop the top element from the stack."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        popped_value = self.top.data
        self.top = self.top.next
        self.size -= 1
        return popped_value

    def top(self):
        """Return the top element of the stack without removing it."""
        if self.is_empty():
            raise IndexError("Top from an empty stack")
        return self.top.data

    def size(self):
        """Return the size of the stack."""
        return self.size

    def to_list(self):
        """Return the stack as a list."""
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result
