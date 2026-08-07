from __future__ import annotations


class TreeNode:
    """
    Basic binary tree node.
    """

    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_tree() -> TreeNode:
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


def print_preorder(root: TreeNode | None) -> None:
    """
    Print the tree using preorder traversal.
    """

    if root is None:
        return

    print(root.val, end=" ")
    print_preorder(root.left)
    print_preorder(root.right)


# =============================================================================
# Approach 1: Top-Down Recursion (Recommended)
# =============================================================================
#
# Time Complexity : O(n)
# Space Complexity: O(h)
#
# =============================================================================

def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """
    Inverts (mirrors) a binary tree.

    Top-Down Recursion
    """

    if root is None:
        return None

    # Swap the children.
    root.left, root.right = root.right, root.left

    # Recursively invert both subtrees.
    invert_tree(root.left)
    invert_tree(root.right)

    return root


def main() -> None:
    root = build_tree()

    print("Original Tree (Preorder):")
    print_preorder(root)
    print()

    invert_tree(root)

    print("Inverted Tree (Preorder):")
    print_preorder(root)
    print()


if __name__ == "__main__":
    main()