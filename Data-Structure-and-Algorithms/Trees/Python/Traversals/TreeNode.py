"""
TreeNode.py

Defines the basic binary tree node used throughout the project.
"""


class TreeNode:
    """
    A node in a binary tree.

    Attributes:
        val   : Value stored in the node.
        left  : Reference to the left child.
        right : Reference to the right child.
    """

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right