class BSTNode:
    """Node class for a Binary Search Tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation."""
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value into the BST."""
        if not self.root:
            self.root = BSTNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        """Recursive insertion."""
        if value < node.value:
            if not node.left:
                node.left = BSTNode(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if not node.right:
                node.right = BSTNode(value)
            else:
                self._insert(node.right, value)

    def find(self, value):
        """Search for a value in the BST."""
        return self._find(self.root, value)

    def _find(self, node, value):
        """Recursive search."""
        if not node:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._find(node.left, value)
        else:
            return self._find(node.right, value)

    def delete(self, value):
        """Delete a value from the BST."""
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        """Recursive deletion."""
        if not node:
            return node

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
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        return node

    def _min_value_node(self, node):
        """Get the node with the minimum value."""
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        """Perform an inorder traversal."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self):
        """Perform a preorder traversal."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        """Perform a postorder traversal."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
