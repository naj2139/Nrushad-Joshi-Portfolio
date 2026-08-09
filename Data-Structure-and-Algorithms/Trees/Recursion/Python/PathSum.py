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
    r"""
    Construct an example tree.

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \       \
        7    2       0

    Root-to-leaf paths and their sums:
        5-4-11-7  = 27
        5-4-11-2  = 22
        5-8-13    = 26
        5-8-4-0   = 17
    """
    root = TreeNode(5)
    root.left, root.right = TreeNode(4), TreeNode(8)
    root.left.left = TreeNode(11)
    root.left.left.left, root.left.left.right = TreeNode(7), TreeNode(2)
    root.right.left, root.right.right = TreeNode(13), TreeNode(4)
    root.right.right.right = TreeNode(0)

    return root


def find_node(root: TreeNode | None, val: int) -> TreeNode | None:
    """
    Helper for main() only -- not part of the Path Sum algorithm.
    """
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    """
    Given the root of a binary tree and a target integer, return True
    if the tree has a ROOT-TO-LEAF path such that the values along
    that path add up exactly to target_sum, or False otherwise.

    A "path" here must start at the root and end at a leaf (a node
    with no children at all) -- it can't stop partway down, and it
    can't continue past a leaf. A single node with no children is
    itself a valid root-to-leaf path.

    Only one such path needs to exist for the answer to be True; the
    tree may contain other root-to-leaf paths that don't sum to the
    target.

    Approach:
        This is top-down, not bottom-up like balanced/diameter/LCA --
        instead of combining results on the way back UP the
        recursion, a running "remaining budget" is passed DOWN into
        each call: target_sum - root.val. By the time a leaf is
        reached, that remaining budget should be exactly 0 if the
        path sums to the original target.

    Time complexity:  O(n) -- each node is visited at most once.
    Space complexity: O(h) -- recursion stack depth equals tree height.
    """

    # My First Attempt
    #
    # def has_path_sum(root, target_sum):
    #     if not root:
    #         return False
    #     if (root.left or root.right) and (target_sum - root.val == 0):
    #         return False
    #     if (not root.left and not root.right) and (target_sum - root.val == 0):
    #         return True
    #     left = has_path_sum(root.left, target_sum - root.val)
    #     right = has_path_sum(root.right, target_sum - root.val)
    #     return left or right
    #
    # Why the removed `if` block was wrong:
    #   That block returned False early whenever a non-leaf node's
    #   remaining budget hit exactly 0, on the assumption that hitting
    #   0 before reaching a leaf could never lead to a valid path.
    #   That assumption breaks the moment a node further down has a
    #   value of 0 -- e.g. root=5 with a single leaf child of value 0,
    #   target_sum=5: the real path 5 -> 0 does sum to 5, but the
    #   early-exit fired at the root (budget hit 0 with children still
    #   present) and returned False before ever reaching that leaf.
    #   The leaf-check below already correctly identifies every valid
    #   stopping point on its own -- a non-leaf node with budget 0 is
    #   not a special case, it's just an ordinary node that should
    #   keep recursing like any other.

    if not root:
        return False

    # Reached a leaf -- this is the only place a path can validly end.
    # It's a match only if the running budget lands exactly on 0 here.
    if (not root.left and not root.right) and (target_sum - root.val == 0):
        return True

    # Not a leaf: keep going, carrying the reduced budget down into
    # whichever children exist. A path is valid if EITHER side finds
    # a match further down.
    left = has_path_sum(root.left, target_sum - root.val)
    right = has_path_sum(root.right, target_sum - root.val)

    return left or right


def main() -> None:
    root = build_example_tree()

    print("Path sum 27 exists:", has_path_sum(root, 27))  # True  (5-4-11-7)
    print("Path sum 28 exists:", has_path_sum(root, 28))  # False
    print("Path sum 17 exists:", has_path_sum(root, 17))  # True  (5-8-4-0)

if __name__ == "__main__":
    main()