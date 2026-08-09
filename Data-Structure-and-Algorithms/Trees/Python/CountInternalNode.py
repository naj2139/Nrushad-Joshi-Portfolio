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

    Internal nodes = 10
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


def count_internal_node(root: TreeNode | None) -> int:
    """
    Return the total number of internal nodes in a binary tree.

    An internal node is any node that has at least one child.
    Leaf nodes are not counted.
    """

    # An empty tree (or empty subtree) contains no internal nodes.
    if not root:
        return 0

    # If both children are missing, this node is a leaf.
    # Leaf nodes are not internal nodes, so return 0.
    if not root.left and not root.right:
        return 0

    # Otherwise, this node is an internal node.
    # Count the current node, then recursively count the
    # internal nodes in the left and right subtrees.
    return 1 + count_internal_node(root.left) + count_internal_node(root.right)


def main() -> None:
    root = build_example_tree()
    print("Total Internal Node Count:", count_internal_node(root))


if __name__ == "__main__":
    main()