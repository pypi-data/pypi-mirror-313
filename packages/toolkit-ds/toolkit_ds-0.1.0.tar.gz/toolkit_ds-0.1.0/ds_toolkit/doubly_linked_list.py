class DoublyLinkedListNode:
    """Node class for a doubly linked list."""
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """Doubly Linked List implementation."""
    def __init__(self):
        self.head = None
        self.tail = None

    def push_front(self, value):
        """Insert a node at the front of the list."""
        new_node = DoublyLinkedListNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def push_back(self, value):
        """Insert a node at the end of the list."""
        new_node = DoublyLinkedListNode(value)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def pop_front(self):
        """Remove and return the node from the front of the list."""
        if not self.head:
            raise IndexError("Pop from empty list")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return value

    def pop_back(self):
        """Remove and return the node from the end of the list."""
        if not self.tail:
            raise IndexError("Pop from empty list")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        return value

    def find(self, value):
        """Search for a node with the given value."""
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_list(self):
        """Convert the linked list to a Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result
