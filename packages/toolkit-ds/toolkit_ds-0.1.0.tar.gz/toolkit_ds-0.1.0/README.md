# DS Toolkit

DS Toolkit is a Python package providing implementations of common data structures such as Stack, Queue, Linked List, Binary Search Tree (BST), AVL Tree, and more. This toolkit helps developers easily use these data structures in their Python projects.

## Features

- **Stack**: A simple implementation of a stack data structure using Python lists.
- **Queue**: A basic queue implementation with both list-based and linked list-based options.
- **Binary Search Tree (BST)**: An implementation of a binary search tree.
- **AVL Tree**: An implementation of a self-balancing binary search tree.
- **Union Find**: Data structure for handling disjoint sets.

## Installation

You can install the `ds_toolkit` package directly from PyPI using pip:

```bash
pip install ds-toolkit
```

Alternatively, if you want to install it directly from the source, clone the repository and use the following:

```bash
git clone https://github.com/ARAVIND281/ds_toolkit.git
cd ds_toolkit
pip install .
```
## Usage

### Stack

The stack is a simple Last In, First Out (LIFO) data structure. You can perform the following operations on the stack:

- **push(value)**: Adds a value to the top of the stack.
- **pop()**: Removes and returns the value at the top of the stack.
- **top()**: Returns the value at the top without removing it.
- **is_empty()**: Checks if the stack is empty.
- **size()**: Returns the number of elements in the stack.
- **to_list()**: Returns a list representation of the stack.

#### Example:

```python
from ds_toolkit.stack import Stack

stack = Stack()

# Push items onto the stack
stack.push(10)
stack.push(20)

# Pop the top item
print(stack.pop())  # Output: 20

# Peek at the top item
print(stack.top())  # Output: 10

# Check if the stack is empty
print(stack.is_empty())  # Output: False

# Get the size of the stack
print(stack.size())  # Output: 1

# Convert stack to list
print(stack.to_list())  # Output: [10]
```

### Queue

The queue is a simple First In, First Out (FIFO) data structure. You can perform the following operations on the queue:

### Queue

A queue is a First In, First Out (FIFO) data structure. This means that elements are processed in the order in which they are added, with the first element added being the first one to be removed. The following operations are supported:

- **enqueue(value)**: Adds a value to the end of the queue.
- **dequeue()**: Removes and returns the value at the front of the queue.
- **front()**: Returns the value at the front of the queue without removing it.
- **is_empty()**: Checks if the queue is empty.
- **size()**: Returns the number of elements in the queue.
- **to_list()**: Returns the queue as a list.

#### Example:

```python
from ds_toolkit.queue import Queue

# Create a new Queue instance
queue = Queue()

# Enqueue items into the queue
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)

# Dequeue the first item (10)
print(queue.dequeue())  # Output: 10

# Check if the queue is empty
print(queue.is_empty())  # Output: False

# Get the size of the queue
print(queue.size())  # Output: 2

# Peek at the front item (20)
print(queue.front())  # Output: 20

# Convert the queue to a list
print(queue.to_list())  # Output: [20, 30]
```

### Binary Search Tree (BST)

A **Binary Search Tree (BST)** is a type of binary tree where each node has at most two children, and for each node:

- The left child has a value less than the node's value.
- The right child has a value greater than the node's value.

BST supports efficient search, insertion, and deletion operations, with an average time complexity of **O(log n)**.

#### Operations:

- **insert(value)**: Inserts a value into the BST.
- **search(value)**: Searches for a value in the BST and returns `True` if it exists, otherwise `False`.
- **delete(value)**: Deletes a node with the given value.
- **find_min()**: Returns the minimum value in the BST.
- **find_max()**: Returns the maximum value in the BST.
- **inorder_traversal()**: Returns a list of values in ascending order (left-root-right traversal).
- **preorder_traversal()**: Returns a list of values in preorder (root-left-right traversal).
- **postorder_traversal()**: Returns a list of values in postorder (left-right-root traversal).
- **height()**: Returns the height (max depth) of the tree.

#### Example:

```python
from ds_toolkit.bst import BinarySearchTree

# Create a new Binary Search Tree
bst = BinarySearchTree()

# Insert values into the BST
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)
bst.insert(60)
bst.insert(80)

# Search for a value
print(bst.search(40))  # Output: True
print(bst.search(25))  # Output: False

# Inorder traversal (sorted order)
print(bst.inorder_traversal())  # Output: [20, 30, 40, 50, 60, 70, 80]

# Find minimum and maximum values
print(bst.find_min())  # Output: 20
print(bst.find_max())  # Output: 80

# Delete a node
bst.delete(20)  # Deletes the node with value 20
print(bst.inorder_traversal())  # Output: [30, 40, 50, 60, 70, 80]

# Get tree height
print(bst.height())  # Output: 3 (based on the tree's structure)
```

### AVL Tree

An **AVL Tree** is a self-balancing binary search tree (BST) where the difference in heights between the left and right subtrees (the balance factor) is at most 1 for all nodes. If the balance factor goes beyond this limit, the tree is rebalanced using rotations.

#### Operations:

- **insert(value)**: Inserts a value into the AVL tree while maintaining the balance.
- **delete(value)**: Deletes a node with the specified value while maintaining the balance.
- **search(value)**: Searches for a value in the AVL tree and returns `True` if found, otherwise `False`.
- **find_min()**: Returns the node with the minimum value.
- **find_max()**: Returns the node with the maximum value.
- **height()**: Returns the height (maximum depth) of the AVL tree.
- **inorder_traversal()**: Returns a list of values in ascending order (left-root-right traversal).
- **preorder_traversal()**: Returns a list of values in preorder (root-left-right traversal).
- **postorder_traversal()**: Returns a list of values in postorder (left-right-root traversal).

#### Example:

```python
from ds_toolkit.avl import AVLTree

# Create a new AVL Tree
avl = AVLTree()

# Insert values into the AVL Tree
avl.insert(50)
avl.insert(30)
avl.insert(70)
avl.insert(20)
avl.insert(40)
avl.insert(60)
avl.insert(80)

# Search for a value
print(avl.search(40))  # Output: True
print(avl.search(25))  # Output: False

# Inorder traversal (sorted order)
print(avl.inorder_traversal())  # Output: [20, 30, 40, 50, 60, 70, 80]

# Find minimum and maximum values
print(avl.find_min())  # Output: 20
print(avl.find_max())  # Output: 80

# Delete a node
avl.delete(20)  # Deletes the node with value 20
print(avl.inorder_traversal())  # Output: [30, 40, 50, 60, 70, 80]

# Get tree height
print(avl.height())  # Output: 3 (based on the tree's structure)
```

### Union Find (Disjoint Set Union - DSU)

The **Union Find** data structure efficiently handles the dynamic connectivity problem. It supports two primary operations:
1. **Union**: Merges two sets into one.
2. **Find**: Determines which set an element belongs to.

Union Find is commonly used for problems involving connectivity, such as determining connected components in a graph or finding the minimum spanning tree.

#### Operations:

- **find(x)**: Returns the representative (or leader) of the set containing element `x`.
- **union(x, y)**: Merges the sets containing `x` and `y`.
- **connected(x, y)**: Returns `True` if `x` and `y` are in the same set, otherwise `False`.
- **size(x)**: Returns the size of the set containing element `x`.
- **make_set(x)**: Initializes a set for a new element `x`.

#### Example:

```python
from ds_toolkit.union_find import UnionFind

# Create a UnionFind object
uf = UnionFind()

# Add elements to the UnionFind structure
uf.make_set(1)
uf.make_set(2)
uf.make_set(3)
uf.make_set(4)
uf.make_set(5)

# Perform union operations
uf.union(1, 2)  # Union of 1 and 2
uf.union(3, 4)  # Union of 3 and 4
uf.union(2, 3)  # Union of 2 and 3 (now 1, 2, 3, and 4 are in the same set)

# Check if two elements are connected
print(uf.connected(1, 4))  # Output: True (since 1, 2, 3, and 4 are in the same set)
print(uf.connected(1, 5))  # Output: False (1 and 5 are in different sets)

# Find the representative of a set
print(uf.find(3))  # Output: 1 (since 1, 2, 3, and 4 are all connected, and 1 is the root)

# Check the size of a set
print(uf.size(1))  # Output: 4 (the set containing 1, 2, 3, and 4 has size 4)
```

## Author

This project is maintained by [Aravind S](https://github.com/ARAVIND281). 

If you have any questions or suggestions, feel free to reach out via GitHub or through the issues section of the repository.

### About the Author

This project is developed by **Aravind S**, the founder of **Finmitr** and **Golden Crop**.

- GitHub: [@ARAVIND281](https://github.com/ARAVIND281)
- Email: [aravind@inbo.tech](mailto:aravind@inbo.tech)
- Website: [inbo.tech](https://inbo.tech)

You can connect with Aravind on [LinkedIn](https://www.linkedin.com/in/aravinds28/).

---

Thank you for exploring this project!
