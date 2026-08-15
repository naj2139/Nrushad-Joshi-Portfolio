from __future__ import annotations


class TreeNode:
    """
    Basic binary tree node.
    """

    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_example_tree() -> TreeNode:
    """
    Construct the example binary tree.

                                50
                         /               \
                       25                 75
                     /    \             /    \
                   10      35         60      90
                  /  \    /  \       /  \    /  \
                 5   15  30  40    55  65  80   95
                / \                               / \
               2   7                            92 100
              /
             1

    Minimum Node Value = 1
    """

    root = TreeNode(50)

    # Level 2
    root.left, root.right = TreeNode(25), TreeNode(75)

    # Level 3
    root.left.left, root.left.right = TreeNode(10), TreeNode(35)
    root.right.left, root.right.right = TreeNode(60), TreeNode(90)

    # Level 4
    root.left.left.left, root.left.left.right = TreeNode(5), TreeNode(15)
    root.left.right.left, root.left.right.right = TreeNode(30), TreeNode(40)
    root.right.left.left, root.right.left.right = TreeNode(55), TreeNode(65)
    root.right.right.left, root.right.right.right = TreeNode(80), TreeNode(95)

    # Level 5
    root.left.left.left.left, root.left.left.left.right = TreeNode(2), TreeNode(7)
    root.right.right.right.left, root.right.right.right.right = TreeNode(92), TreeNode(100)

    # Level 6
    root.left.left.left.left.left = TreeNode(1)

    return root

def min_node_value(root: TreeNode | None) -> int:
    """
    Returns the minimum value stored in the binary tree.

    Bottom-Up Recursion
    """

    # Base Case:
    # An empty tree has no value, so return positive infinity.
    # This ensures it never becomes the minimum when compared
    # with actual node values.
    if root is None:
        return float("inf")

    # Base Case:
    # A leaf node is the minimum value of its own subtree.
    if root.left is None and root.right is None:
        return root.val

    # Recursively compute the minimum value in the left
    # and right subtrees.
    left = min_node_value(root.left)
    right = min_node_value(root.right)

    # Compare the current node's value with the minimum
    # values returned by the left and right subtrees.
    # Return the smallest value to the parent.
    return min(root.val, left, right)

def main() -> None:
    root = build_example_tree()
    print("Minimum Node Value:", min_node_value(root))

if __name__ == "__main__":
    main()