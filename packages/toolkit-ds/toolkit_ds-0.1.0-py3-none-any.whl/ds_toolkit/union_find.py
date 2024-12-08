class UnionFind:
    """Union-Find (Disjoint Set Union) data structure with path compression and union by rank."""

    def __init__(self, size):
        """Initialize the UnionFind data structure with `size` elements."""
        self.parent = list(range(size))  # Each element is its own parent initially
        self.rank = [1] * size  # Rank to keep the tree flat

    def find(self, x):
        """Find the representative (root) of the set that `x` belongs to."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        """Union the sets containing `x` and `y`."""
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            # Union by rank: attach the smaller tree under the larger tree
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

    def connected(self, x, y):
        """Check if elements `x` and `y` belong to the same set."""
        return self.find(x) == self.find(y)

    def to_list(self):
        """Return the list of parents for all elements."""
        return self.parent
