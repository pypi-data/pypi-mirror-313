import unittest
from ds_toolkit.union_find import UnionFind


class TestUnionFind(unittest.TestCase):
    def setUp(self):
        """Initialize a new UnionFind data structure for each test."""
        self.uf = UnionFind(10)  # Creates 10 sets (0 to 9)

    def test_union_and_find(self):
        """Test union and find operations."""
        self.uf.union(1, 2)
        self.uf.union(2, 3)
        self.assertEqual(self.uf.find(1), self.uf.find(3))
        self.assertNotEqual(self.uf.find(1), self.uf.find(4))

    def test_connected(self):
        """Test if two elements are connected (i.e., belong to the same set)."""
        self.uf.union(1, 2)
        self.uf.union(2, 3)
        self.assertTrue(self.uf.connected(1, 3))
        self.assertFalse(self.uf.connected(1, 4))

    def test_union_by_rank(self):
        """Test union by rank to ensure the tree remains flat."""
        self.uf.union(1, 2)
        self.uf.union(3, 4)
        self.uf.union(1, 3)
        # The parent of 3 should now be 1, as 1 is the root of the combined set
        self.assertEqual(self.uf.find(3), self.uf.find(1))

    def test_path_compression(self):
        """Test path compression to flatten the tree structure."""
        self.uf.union(1, 2)
        self.uf.union(2, 3)
        self.uf.union(3, 4)
        self.uf.find(4)  # This should perform path compression
        # After path compression, all elements should have the same root
        self.assertEqual(self.uf.find(1), self.uf.find(2))
        self.assertEqual(self.uf.find(3), self.uf.find(4))

    def test_multiple_unions(self):
        """Test performing multiple union operations."""
        self.uf.union(1, 2)
        self.uf.union(3, 4)
        self.uf.union(2, 3)
        self.assertTrue(self.uf.connected(1, 4))
        self.assertTrue(self.uf.connected(2, 3))

    def test_disjoint_sets(self):
        """Test that initially all sets are disjoint."""
        self.assertNotEqual(self.uf.find(0), self.uf.find(1))
        self.assertNotEqual(self.uf.find(2), self.uf.find(3))

    def test_to_list(self):
        """Test converting the UnionFind structure to a list of parents."""
        self.uf.union(1, 2)
        self.uf.union(3, 4)
        uf_list = self.uf.to_list()
        self.assertEqual(uf_list[1], uf_list[2])
        self.assertEqual(uf_list[3], uf_list[4])
        self.assertNotEqual(uf_list[1], uf_list[3])

    def test_connected_no_union(self):
        """Test that two elements that haven't been unioned are not connected."""
        self.assertFalse(self.uf.connected(1, 3))


if __name__ == "__main__":
    unittest.main()
