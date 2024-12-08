class AVLNode:
    """Node class for AVL Tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL Tree implementation."""

    def __init__(self):
        self.root = None

    def get_height(self, node):
        """Get the height of a node."""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Get the balance factor of a node."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, z):
        """Perform a right rotation."""
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        """Perform a left rotation."""
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, value):
        """Insert a value into the AVL tree."""
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        """Recursive function to insert a value."""
        if not node:
            return AVLNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        # Update the height of the node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get the balance factor
        balance = self.get_balance(node)

        # Perform rotations to balance the tree
        # Case 1: Left Left
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)
        # Case 2: Right Right
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)
        # Case 3: Left Right
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Case 4: Right Left
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, value):
        """Delete a value from the AVL tree."""
        if self.is_empty():
            raise Exception("Cannot delete from an empty tree")
        self.root = self._delete(self.root, value)
    
    def is_empty(self):
        return self.root is None


    def _delete(self, node, value):
        """Recursive function to delete a value."""
        if not node:
            return node

        # Perform standard BST delete
        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: Get the inorder successor
            temp = self._get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        # Update the height of the node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get the balance factor
        balance = self.get_balance(node)

        # Perform rotations to balance the tree
        # Case 1: Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        # Case 2: Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        # Case 3: Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Case 4: Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _get_min_value_node(self, node):
        """Get the node with the smallest value."""
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        """Perform inorder traversal and return the result as a list."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if not node:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)

    def preorder(self):
        """Perform preorder traversal and return the result as a list."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if not node:
            return
        result.append(node.value)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def postorder(self):
        """Perform postorder traversal and return the result as a list."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if not node:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.value)
