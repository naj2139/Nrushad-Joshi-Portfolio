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
    Construct a symmetric binary tree.

                    1
                 /     \
                2       2
              /   \   /   \
             3     4 4     3
            /               \
           5                 5
    """

    root = TreeNode(1)

    # Level 2
    root.left, root.right = TreeNode(2), TreeNode(2)

    # Level 3
    root.left.left, root.left.right = TreeNode(3), TreeNode(4)
    root.right.left, root.right.right = TreeNode(4), TreeNode(3)

    # Level 4
    root.left.left.left = TreeNode(5)
    root.right.right.right = TreeNode(5)

    # Uncomment one of these to test:
    #
    # root.right.right.right.val = 6      # Different value
    # root.right.left = None              # Missing node
    # root.left.right.left = TreeNode(8)  # Extra node

    return root

# =============================================================================
# My First Attempt
# =============================================================================
#
# def is_symmetric(root: TreeNode | None) -> bool:
#     """
#     Returns True if the binary tree is symmetric.
#
#     Simultaneous Bottom-Up Recursion
#     """
#
#     def symmetric_helper(root1: TreeNode | None, root2: TreeNode | None) -> bool:
#         # Both hit None together
#         if not root1 and not root2:
#             return True
#         if (not root1 and root2) or (not root2 and root1):
#             return False
#         if root1.val != root2.val:
#             return False
#
#         if root1.val == root2.val:
#             left =  symmetric_helper(root1.left, root2.right)
#             right = symmetric_helper(root1.right, root2.left)
#             return left and right
#
#     if root:
#         return symmetric_helper(root.left, root.right)


def is_symmetric(root: TreeNode | None) -> bool:
    """
    Returns True if the binary tree is symmetric.

    Recursive idea:
        - An empty tree is trivially symmetric.
        - Two subtrees are mirrors of each other when:
            1. They're both empty, or
            2. They're both non-empty, their values match, AND
               the outer pair (left1, right2) and inner pair
               (right1, left2) are themselves mirrors.
        - Each recursive call returns whether its pair of nodes mirrors;
          results are combined with `and` on the way back up.
    """

    def symmetric_helper(root1: TreeNode | None, root2: TreeNode | None) -> bool:
        # Base case: both sides hit None together -> symmetric at this branch.
        if not root1 and not root2:
            return True

        # Only one side is None -> shapes don't match.
        if not root1 or not root2:
            return False

        # Values differ -> not symmetric.
        if root1.val != root2.val:
            return False

        # Recurse to the bottom first (outer pair, then inner pair),
        # then combine results going back up.
        return symmetric_helper(root1.left, root2.right) and symmetric_helper(root1.right, root2.left)

    # Base case: empty tree is trivially symmetric.
    if not root:
        return True

    # Kick off comparison between the left and right subtrees.
    return symmetric_helper(root.left, root.right)

def main() -> None:
    root = build_tree()

    if is_symmetric(root):
        print("The tree is symmetric.")
    else:
        print("The tree is NOT symmetric.")


if __name__ == "__main__":
    main()