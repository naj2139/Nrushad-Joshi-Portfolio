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

    Minimum depth = 4
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
    root.right.right.right.left, root.right.right.right = TreeNode(92), TreeNode(100)

    # Level 6
    root.left.left.left.left.left = TreeNode(1)

    return root


def min_depth(root: TreeNode | None) -> int:
    """
    Return the minimum depth of a binary tree.

    The minimum depth is the number of nodes along the shortest
    path from the root to the nearest leaf node.

    """

    # Empty tree has depth 0.
    if not root:
        return 0

    # If one subtree is missing, the shortest path must go
    # through the existing subtree.
    if not root.left:
        return 1 + min_depth(root.right)

    if not root.right:
        return 1 + min_depth(root.left)

    # Both children exist, so choose the shorter path.
    return 1 + min(min_depth(root.left), min_depth(root.right))


def main() -> None:
    root = build_example_tree()
    print("Minimum Depth:", min_depth(root))


if __name__ == "__main__":
    main()

# Why can't we simply write?
    #
    #     return 1 + min(min_depth(root.left), min_depth(root.right))
    #
    # like we do for maximum depth?
    #
    # Because an empty subtree returns 0. For maximum depth, this is fine:
    # max() naturally ignores the missing child and chooses the deeper path.
    #
    # Example:
    #       A
    #      /
    #     B
    #
    # max_depth(A) = 1 + max(1, 0) = 2  ✓
    #
    # For minimum depth, however, 0 does NOT represent a valid path from
    # the root to a leaf. If we used min(), the missing child would always
    # be chosen because 0 is smaller than any real depth.
    #
    # Using the same example:
    #
    # min_depth(A) = 1 + min(1, 0) = 1  ✗
    #
    # This incorrectly claims that A itself is the nearest leaf, even
    # though we must continue through B to reach one.
    #
    # Therefore, if exactly one child is missing, we are forced to recurse
    # into the existing child. Only when BOTH children exist is it valid
    # to compare their depths using min().