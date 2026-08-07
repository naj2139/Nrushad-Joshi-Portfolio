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


# =============================================================================
# Approach 1: Full Traversal
# =============================================================================
#
# Idea
# ----
# Visit every node in the tree, regardless of whether the target has
# already been found.
#
# Each recursive call returns whether the target exists in its subtree.
# The parent combines the results from:
#
#   - Current node
#   - Left subtree
#   - Right subtree
#
# Time Complexity : O(n)
# Space Complexity: O(h)
#
# =============================================================================

# My Original Solution
#
# def search_node(root: TreeNode | None, target: int) -> bool:
#     if not root:
#         return False
#
#     curr = False if root.val != target else True
#
#     left = search_node(root.left, target)
#     right = search_node(root.right, target)
#
#     return left or right or curr
#
# Drawbacks:
#   1. Continues traversing the tree even after finding the target.
#   2. Visits every node unnecessarily in many cases.
#   3. Uses an extra variable (curr) that isn't needed.


# =============================================================================
# Approach 2: Early Termination (Recommended)
# =============================================================================
#
# Idea
# ----
# Search the current node first.
#
# If the current node contains the target, immediately return True.
# Otherwise, recursively search the left and right subtrees.
#
# This avoids unnecessary recursive calls once the target is found.
#
# Time Complexity:
#     Best Case : O(1)
#     Worst Case: O(n)
#
# Space Complexity: O(h)
#
# =============================================================================

def search_node(root: TreeNode | None, target: int) -> bool:
    """
    Returns True if the target value exists in the binary tree.

    Bottom-Up Recursion

    Every recursive call searches its own subtree and returns whether
    the target was found.

    Unlike the full traversal approach, this implementation stops
    searching immediately after finding the target.
    """

    # Base Case:
    # An empty subtree cannot contain the target.
    if root is None:
        return False

    # Base Case:
    # The target has been found.
    # Return immediately without searching the remaining tree.
    if root.val == target:
        return True

    # Search the left subtree first.
    # If found, stop immediately.
    if search_node(root.left, target):
        return True

    # Otherwise, search the right subtree.
    return search_node(root.right, target)

def main() -> None:
    root = build_example_tree()

    target = 65

    if search_node(root, target):
        print(f"{target} was found in the tree.")
    else:
        print(f"{target} was not found in the tree.")

if __name__ == "__main__":
    main()