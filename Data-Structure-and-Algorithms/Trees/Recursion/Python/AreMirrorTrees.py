"""
mirror_trees.py

Check whether two binary trees are mirror images of one another.

A tree `root2` is the mirror of `root1` if, at every level, the
left/right children are swapped: root1.left mirrors root2.right,
and root1.right mirrors root2.left.

Author: Nrushad Joshi
"""

from __future__ import annotations


class TreeNode:
    """Basic binary tree node."""

    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_tree_1() -> TreeNode:
    r"""
    Construct the first binary tree.

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


def build_tree_2() -> TreeNode:
    """
    Construct the second binary tree as the exact mirror image of Tree 1.

    Modify one or more nodes below (see the commented-out lines at the
    bottom) to test the "not a mirror" cases.
    """
    root = TreeNode(50)

    # Level 2
    root.left, root.right = TreeNode(75), TreeNode(25)

    # Level 3
    root.left.left, root.left.right = TreeNode(90), TreeNode(60)
    root.right.left, root.right.right = TreeNode(35), TreeNode(10)

    # Level 4
    root.left.left.left, root.left.left.right = TreeNode(95), TreeNode(80)
    root.left.right.left, root.left.right.right = TreeNode(65), TreeNode(55)
    root.right.left.left, root.right.left.right = TreeNode(40), TreeNode(30)
    root.right.right.left, root.right.right.right = TreeNode(15), TreeNode(5)

    # Level 5
    root.left.left.left.left, root.left.left.left.right = TreeNode(100), TreeNode(92)
    root.right.right.right.left, root.right.right.right.right = TreeNode(7), TreeNode(2)

    # Level 6
    root.right.right.right.right.right = TreeNode(1)

    # Uncomment one of these to test a mismatch:
    #
    # root.left.right.left.val = 66             # Different value
    # root.right.left.right = None              # Missing node
    # root.left.left.right.left = TreeNode(81)  # Extra node

    return root


# =============================================================================
# My First Attempt
# =============================================================================
#
# def are_mirror_trees(root1: TreeNode | None,
#                      root2: TreeNode | None) -> bool:
#
#     if not root1 and not root2:
#         return True
#
#     if (not root1 and root2) or (root1 and not root2):
#         return False
#
#     if root1.val == root2.val:
#
#         x = are_mirror_trees(root1.left, root2.right)
#         y = are_mirror_trees(root1.right, root2.left)
#
#         return x and y
#
#     return False

def are_mirror_trees(root1: TreeNode | None, root2: TreeNode | None) -> bool:
    """
    Return True if two binary trees are mirror images of each other.

    Uses simultaneous bottom-up recursion: at each pair of nodes,
    root1's left subtree is compared against root2's right subtree,
    and root1's right subtree against root2's left subtree.
    """
    # Both sides bottomed out at the same time -> this branch matches.
    if root1 is None and root2 is None:
        return True

    # Only one side is None -> the shapes diverge here, can't be mirrors.
    if root1 is None or root2 is None:
        return False

    # Values at this mirrored position must match.
    if root1.val != root2.val:
        return False

    # Recurse on the swapped pairs: root1's left must mirror root2's
    # right, and root1's right must mirror root2's left. Short-circuits
    # on the first False, so we don't walk the rest of the tree once a
    # mismatch is found.
    return are_mirror_trees(root1.left, root2.right) and are_mirror_trees(
        root1.right, root2.left
    )


def main() -> None:
    tree1 = build_tree_1()
    tree2 = build_tree_2()

    if are_mirror_trees(tree1, tree2):
        print("The two trees are mirrors of each other.")
    else:
        print("The two trees are NOT mirrors of each other.")


if __name__ == "__main__":
    main()