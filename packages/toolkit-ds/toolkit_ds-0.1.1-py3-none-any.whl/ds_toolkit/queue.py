class Queue:
    """Queue implementation using a list."""
    
    def __init__(self):
        self._queue = []

    def enqueue(self, value):
        """Add an element to the end of the queue."""
        self._queue.append(value)

    def dequeue(self):
        """Remove and return the element from the front of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        return self._queue.pop(0)

    def front(self):
        """Return the element at the front of the queue without removing it."""
        if self.is_empty():
            raise IndexError("Front from an empty queue")
        return self._queue[0]

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self._queue) == 0

    def size(self):
        """Return the size of the queue."""
        return len(self._queue)

    def to_list(self):
        """Return the queue as a list."""
        return self._queue[:]

class LinkedListQueue:
    """Queue implementation using a singly linked list."""

    class Node:
        """Node class for the linked list."""
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        """Check if the queue is empty."""
        return self.size == 0

    def enqueue(self, value):
        """Add an element to the queue."""
        new_node = self.Node(value)
        if self.rear:
            self.rear.next = new_node
        self.rear = new_node
        if self.front is None:
            self.front = new_node
        self.size += 1

    def dequeue(self):
        """Remove and return the front element of the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        value = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return value

    def peek(self):
        """Return the front element without removing it."""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.front.data

    def size(self):
        """Return the size of the queue."""
        return self.size

    def to_list(self):
        """Return the queue as a list."""
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result
