import unittest
from ds_toolkit.avl import AVLTree


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        """Initialize a new AVL Tree for each test."""
        self.avl = AVLTree()

    def test_insert_single(self):
        """Test inserting a single value."""
        self.avl.insert(10)
        self.assertEqual(self.avl.inorder(), [10])

    def test_insert_multiple(self):
        """Test inserting multiple values and checking balance."""
        values = [10, 20, 30, 40, 50, 25]
        for val in values:
            self.avl.insert(val)
        self.assertEqual(self.avl.inorder(), [10, 20, 25, 30, 40, 50])

    def test_delete_leaf(self):
        """Test deleting a leaf node."""
        values = [10, 20, 30, 40, 50, 25]
        for val in values:
            self.avl.insert(val)
        self.avl.delete(50)
        self.assertEqual(self.avl.inorder(), [10, 20, 25, 30, 40])

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        values = [10, 20, 30]
        for val in values:
            self.avl.insert(val)
        self.avl.delete(30)
        self.assertEqual(self.avl.inorder(), [10, 20])

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        values = [10, 20, 30, 40, 50, 25]
        for val in values:
            self.avl.insert(val)
        self.avl.delete(20)
        self.assertEqual(self.avl.inorder(), [10, 25, 30, 40, 50])

    def test_inorder_traversal(self):
        """Test the inorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.avl.insert(val)
        self.assertEqual(self.avl.inorder(), [10, 20, 30, 40, 50, 60])

    def test_preorder_traversal(self):
        """Test the preorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.avl.insert(val)
        self.assertEqual(self.avl.preorder(), [40, 20, 10, 30, 50, 60])

    def test_postorder_traversal(self):
        """Test the postorder traversal."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.avl.insert(val)
        self.assertEqual(self.avl.postorder(), [10, 30, 20, 60, 50, 40])

    def test_delete_root(self):
        """Test deleting the root node."""
        values = [40, 20, 10, 30, 50, 60]
        for val in values:
            self.avl.insert(val)
        self.avl.delete(40)
        self.assertEqual(self.avl.inorder(), [10, 20, 30, 50, 60])

    def test_rebalancing(self):
        """Test that the AVL Tree remains balanced after insertions."""
        values = [10, 20, 30, 40, 50, 25]
        for val in values:
            self.avl.insert(val)
        # Manually checking tree balance
        root_balance = self.avl.get_balance(self.avl.root)
        self.assertIn(root_balance, [-1, 0, 1])

    def test_empty_tree_delete(self):
        """Test deleting from an empty tree."""
        with self.assertRaises(Exception):
            self.avl.delete(10)

    def test_empty_tree_traversal(self):
        """Test traversals on an empty tree."""
        self.assertEqual(self.avl.inorder(), [])
        self.assertEqual(self.avl.preorder(), [])
        self.assertEqual(self.avl.postorder(), [])


if __name__ == "__main__":
    unittest.main()