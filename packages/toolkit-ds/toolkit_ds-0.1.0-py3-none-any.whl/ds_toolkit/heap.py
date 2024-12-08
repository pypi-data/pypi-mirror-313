class BinaryMinHeap:
    """Binary Min Heap implementation."""

    def __init__(self):
        self._heap = []

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def insert(self, value):
        """Insert a value into the heap."""
        self._heap.append(value)
        self._heapify_up(len(self._heap) - 1)

    def _heapify_up(self, index):
        """Ensure the heap property is maintained while inserting."""
        while index > 0 and self._heap[index] < self._heap[self._parent(index)]:
            self._swap(index, self._parent(index))
            index = self._parent(index)

    def extract_min(self):
        """Remove and return the minimum value from the heap."""
        if not self._heap:
            raise IndexError("Extract from an empty heap")
        if len(self._heap) == 1:
            return self._heap.pop()

        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index):
        """Ensure the heap property is maintained while extracting."""
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)

        if left < len(self._heap) and self._heap[left] < self._heap[smallest]:
            smallest = left
        if right < len(self._heap) and self._heap[right] < self._heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def get_min(self):
        """Return the minimum value without removing it."""
        if not self._heap:
            raise IndexError("Get from an empty heap")
        return self._heap[0]

    def size(self):
        """Return the size of the heap."""
        return len(self._heap)

    def is_empty(self):
        """Check if the heap is empty."""
        return len(self._heap) == 0

    def to_list(self):
        """Return the heap as a list."""
        return self._heap[:]
