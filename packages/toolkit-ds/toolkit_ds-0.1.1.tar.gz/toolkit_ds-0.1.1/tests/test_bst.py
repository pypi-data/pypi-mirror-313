import unittest
from ds_toolkit.bst import BinarySearchTree


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        """Initialize a new BST for each test."""
        self.bst = BinarySearchTree()

    def test_insert_single(self):
        """Test inserting a single value."""
        self.bst.insert(10)
        self.assertEqual(self.bst.inorder(), [10])

    def test_insert_multiple(self):
        """Test inserting multiple values."""
        values = [10, 5, 15, 3, 7, 12, 18]
        for val in values:
            self.bst.insert(val)
        self.assertEqual(self.bst.inorder(), [3, 5, 7, 10, 12, 15, 18])

    def test_find_existing(self):
        """Test finding an existing value."""
        values = [10, 5, 15, 3, 7, 12, 18]
        for val in values:
            self.bst.insert(val)
        self.assertTrue(self.bst.find(7))
        self.assertTrue(self.bst.find(10))

    def test_find_non_existing(self):
        """Test finding a non-existing value."""
        values = [10, 5, 15]
        for val in values:
            self.bst.insert(val)
        self.assertFalse(self.bst.find(20))
        self.assertFalse(self.bst.find(1))

    def test_delete_leaf(self):
        """Test deleting a leaf node."""
        values = [10, 5, 15, 3, 7]
        for val in values:
            self.bst.insert(val)
        self.bst.delete(3)
        self.assertEqual(self.bst.inorder(), [5, 7, 10, 15])

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        values = [10, 5, 15, 3]
        for val in values:
            self.bst.insert(val)
        self.bst.delete(5)
        self.assertEqual(self.bst.inorder(), [3, 10, 15])

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        values = [10, 5, 15, 3, 7, 12, 18]
        for val in values:
            self.bst.insert(val)
        self.bst.delete(10)
        self.assertEqual(self.bst.inorder(), [3, 5, 7, 12, 15, 18])

    def test_inorder_traversal(self):
        """Test the inorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.bst.insert(val)
        self.assertEqual(self.bst.inorder(), [10, 20, 30, 40, 50, 60])

    def test_preorder_traversal(self):
        """Test the preorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.bst.insert(val)
        self.assertEqual(self.bst.preorder(), [40, 20, 10, 30, 50, 60])

    def test_postorder_traversal(self):
        """Test the postorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.bst.insert(val)
        self.assertEqual(self.bst.postorder(), [10, 30, 20, 60, 50, 40])

    def test_empty_tree_find(self):
        """Test finding a value in an empty tree."""
        self.assertFalse(self.bst.find(10))

    def test_empty_tree_traversal(self):
        """Test traversals on an empty tree."""
        self.assertEqual(self.bst.inorder(), [])
        self.assertEqual(self.bst.preorder(), [])
        self.assertEqual(self.bst.postorder(), [])

    def test_empty_tree_delete(self):
        """Test deleting a value from an empty tree."""
        self.bst.delete(10)  # Should not raise an exception
        self.assertEqual(self.bst.inorder(), [])


if __name__ == "__main__":
    unittest.main()
