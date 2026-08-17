from __future__ import annotations


class TreeNode:
    """
    Basic binary tree node.
    """

    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


def build_tree_1() -> TreeNode:
    """
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
    Construct the second binary tree.

    Initially, this tree is identical to Tree 1.
    Modify one or more nodes to test different cases.
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

    # Uncomment one of these to test:
    #
    # root.right.left.right.val = 66            # Different value
    # root.left.right.left = None               # Missing node
    # root.right.right.left.left = TreeNode(81) # Extra node

    return root


# =============================================================================
# Approach 1: Full Traversal
# =============================================================================
#
# Idea
# ----
# Compare the corresponding nodes in both trees.
#
# If both nodes are None, they are identical.
# If one node is None or their values differ, the trees are not identical.
#
# Continue recursively comparing the left and right subtrees.
#
# =============================================================================

# My First Attempt
#
# def identical_trees(root1: TreeNode | None,
#                     root2: TreeNode | None) -> bool:
#
#     # Both hit None at the same time.
#     if not root1 and not root2:
#         return True
#     else:
#
#         if (root1 and root2) and (root1.val == root2.val):
#
#             left = identical_trees(root1.left, root2.left)
#             right = identical_trees(root1.right, root2.right)
#
#             return left and right
#
#         else:
#             return False


# My Second Attempt
#
# def identical_trees(root1: TreeNode | None,
#                     root2: TreeNode | None) -> bool:
#
#     if root1 or root2:
#
#         if (root1 and root2) and (root1.val == root2.val):
#
#             left = identical_trees(root1.left, root2.left)
#             right = identical_trees(root1.right, root2.right)
#
#             return left and right
#
#         else:
#             return False
#
#     else:
#         return True
#
# Improvements:
#   1. Remove redundant nesting.
#   2. Stop recursion as soon as a mismatch is found.
#   3. Avoid exploring the right subtree if the left subtree already differs.


# =============================================================================
# Approach 2: Early Termination (Recommended)
# =============================================================================
#
# Idea
# ----
# Traverse both trees simultaneously.
#
# At every recursive call:
#
#   1. If both nodes are None, they are identical.
#   2. If exactly one node is None, they differ.
#   3. If the node values differ, they are not identical.
#   4. Recursively compare the left subtrees.
#   5. If the left subtrees differ, return False immediately.
#   6. Otherwise, compare the right subtrees.
#
# Unlike the previous approach, this implementation stops searching
# as soon as the first mismatch is found.
#
# =============================================================================

def identical_trees(root1: TreeNode | None, root2: TreeNode | None) -> bool:
    """
    Returns True if both binary trees are structurally identical
    and contain the same values.

    Simultaneous Bottom-Up Recursion

    Each recursive call compares one node from Tree 1 with the
    corresponding node from Tree 2.

    The recursion terminates immediately when the first mismatch
    is encountered.
    """

    # Base Case:
    # Both trees reached the end of a branch simultaneously.
    if root1 is None and root2 is None:
        return True

    # Base Case:
    # One tree ended before the other.
    if root1 is None or root2 is None:
        return False

    # Base Case:
    # The node values differ.
    if root1.val != root2.val:
        return False

    # Compare the left subtrees first.
    # If they are not identical, stop immediately.
    if not identical_trees(root1.left, root2.left):
        return False

    # Compare the right subtrees.
    return identical_trees(root1.right, root2.right)


def main() -> None:
    tree1 = build_tree_1()
    tree2 = build_tree_2()

    if identical_trees(tree1, tree2):
        print("The two trees are identical.")
    else:
        print("The two trees are NOT identical.")

if __name__ == "__main__":
    main()