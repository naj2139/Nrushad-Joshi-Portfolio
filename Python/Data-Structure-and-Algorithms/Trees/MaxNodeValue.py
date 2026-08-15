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

    Maximum Node Value = 100
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


# =============================================================================
# Approach 1: Top-Down (Collect Every Value)
# =============================================================================
#
# Idea
# ----
# Traverse the tree from the root to every node.
# Store every node value in a list.
# After traversal is complete, return the maximum value in the list.
#
# Time Complexity : O(n)
# Space Complexity: O(n)
#
# =============================================================================

def max_node_value_top_down(root: TreeNode | None) -> int:
    if root is None:
        return 0

    values: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if node is None:
            return

        values.append(node.val)

        dfs(node.left)
        dfs(node.right)

    dfs(root)

    return max(values)


# =============================================================================
# My Original Attempt (Preserved)
# =============================================================================
#
# def max_node_value_top_down(root: TreeNode | None) -> int:
#
#     def helper(root, values=[]):
#         if not root:
#             values.append(0)
#             return
#
#         if not root.left and not root.right:
#             values.append(root.val)
#             return
#
#         if root.left and not root.right:
#             values.append(root.val)
#             return helper(root.left, values)
#
#         if root.right and not root.left:
#             values.append(root.val)
#             return helper(root.right, values)
#
#         values.append(root.val)
#         helper(root.left, values)
#         helper(root.right, values)
#
#         return values
#
#     values = helper(root)
#     return max(values)
#
# =============================================================================


def max_node_value_bottom_up(root: TreeNode | None) -> int:
    """
    Returns the maximum value stored in the binary tree.

    Bottom-Up Recursion

    Every recursive call computes the answer for its own subtree and
    returns that answer to its parent.

    The return statement below DOES NOT terminate the entire recursion.

    It only ends the CURRENT function call.

    Example:

            50
           /
         25
        /
      10
     /
    5
    /
    2
    /
    1

    Call Stack (before returning)

        max(50)
            max(25)
                max(10)
                    max(5)
                        max(2)
                            max(1)

    Node 1 returns 1.

    Execution resumes inside max(2).

    max(2) now has:
        left = 1
        right = -inf

    It computes

        max(2, 1, -inf) = 2

    and returns 2.

    Execution then resumes inside max(5), then max(10),
    then max(25), and finally max(50).

    This process is called "unwinding the recursion".
    """

    if root is None:
        return float("-inf")

    left = max_node_value_bottom_up(root.left)
    right = max_node_value_bottom_up(root.right)

    # At this point:
    #   left  = maximum value from the left subtree
    #   right = maximum value from the right subtree
    #
    # Compare those values with the current node's value and return
    # the largest one to the parent.
    #
    # IMPORTANT:
    #   This return exits ONLY the current recursive call.
    #   The caller (parent node) resumes execution immediately after
    #   the recursive function call that produced this value.
    return max(root.val, left, right)


def main() -> None:
    root = build_example_tree()

    print("Top-Down Result :", max_node_value_top_down(root))
    print("Bottom-Up Result:", max_node_value_bottom_up(root))


if __name__ == "__main__":
    main()