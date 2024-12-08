class SinglyLinkedListNode:
    """Node class for a singly linked list."""
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """Singly Linked List implementation."""
    def __init__(self):
        self.head = None

    def push_front(self, value):
        """Insert a node at the front of the list."""
        new_node = SinglyLinkedListNode(value)
        new_node.next = self.head
        self.head = new_node

    def push_back(self, value):
        """Insert a node at the end of the list."""
        new_node = SinglyLinkedListNode(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def pop_front(self):
        """Remove and return the node from the front of the list."""
        if not self.head:
            raise IndexError("Pop from empty list")
        value = self.head.value
        self.head = self.head.next
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

    def size(self):
        """Return the size of the list."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
