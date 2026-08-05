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

    Sum of all node values = 932
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


def sum_node_values(root: TreeNode | None) -> int:
    """
    Return the sum of all node values in a binary tree.

    Each recursive call returns the sum of the subtree rooted
    at the current node. The final result is computed by adding:
        1. The current node's value.
        2. The sum of the left subtree.
        3. The sum of the right subtree.
    """

    # An empty tree (or empty subtree) contributes 0
    # to the total sum.
    if not root:
        return 0

    # Add the current node's value to the sums returned
    # by the left and right subtrees.
    return root.val + sum_node_values(root.left) + sum_node_values(root.right)


def main() -> None:
    root = build_example_tree()
    print("Total Node Sum:", sum_node_values(root))


if __name__ == "__main__":
    main()