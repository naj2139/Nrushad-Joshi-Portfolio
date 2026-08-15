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

            A
           / \
          B   C
         / \   \
        D   E   F
           / \
          G   H
    """
    root = TreeNode("A")
    root.left, root.right = TreeNode("B"), TreeNode("C")
    root.left.left, root.left.right = TreeNode("D"), TreeNode("E")
    root.right.right = TreeNode("F")
    root.left.right.left, root.left.right.right = TreeNode("G"), TreeNode("H")

    return root


def find_node(root: TreeNode | None, val: str) -> TreeNode | None:
    """
    Helper for main() only -- given a value, returns the TreeNode with
    that value so it can be passed into lowest_common_ancestor() as
    one of the two targets. Not part of the LCA algorithm itself.
    """
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def lowest_common_ancestor(
    root: TreeNode | None, p: TreeNode, q: TreeNode
) -> TreeNode | None:
    """
    The lowest common ancestor (LCA) of two nodes p and q in a tree is
    the deepest node that is an ancestor of BOTH p and q.

    "Lowest" here means deepest in the tree (farthest from the root),
    not smallest value.

    If one of the two target nodes is itself an ancestor of the
    other, that ancestor node IS the LCA.

    Given the root of a tree and two target nodes p and q (both
    guaranteed to exist somewhere in the tree), returns the TreeNode
    that is their lowest common ancestor.

    Approach:
        Each recursive call reports upward whether p or q was found
        anywhere in its subtree (True/False). Landing on p or q
        directly reports True immediately, without needing to search
        further down -- this correctly handles the case where one
        target is itself an ancestor of the other.

        At any node, if BOTH its left and right recursive calls
        report True, one target was found on each side -- this node
        is the fork point where their paths diverge, so it's the LCA.
        That signal is then passed further up unchanged, so ancestors
        above the fork don't mistake themselves for the answer too.

    Time complexity:  O(n) -- each node is visited at most once.
    Space complexity: O(h) -- recursion stack depth equals tree height.
    """

# =============================================================================
# My First Attempt
# =============================================================================
    # def lowest_common_ancestor(root, p, q):
    #     track = []
    #     res = []
    #     def lca_helper(root):
    #         if not root:
    #             return None
    #         if root.val == p.val or root.val == q.val:
    #             return True
    #         track.append(root.val)
    #         left = lca_helper(root.left)
    #         right = lca_helper(root.right)
    #         if left and right:
    #             res.append(root)
    #         if left or right:
    #             track.pop(-1)
    #             return True
    #         else:
    #             track.pop(-1)
    #             return None
    #     lca_helper(root)
    #     return res[0]
    #
    # Cleanup below: `track` was built up and popped but never
    # actually read anywhere, so it's dropped entirely. Comparing
    # `node is p or node is q` (identity) is used instead of
    # `root.val == p.val or root.val == q.val` (value equality) --
    # p and q are already the exact TreeNode objects being searched
    # for, so checking identity is both more direct and avoids any
    # ambiguity if two different nodes happened to share a value.

    lca: list[TreeNode | None] = [None]

    def lca_helper(node: TreeNode | None) -> bool:
        if not node:
            return False

        # Landing directly on a target reports "found" immediately,
        # without needing to search that node's own children -- this
        # correctly handles "one target is an ancestor of the other."
        if node is p or node is q:
            return True

        found_left = lca_helper(node.left)
        found_right = lca_helper(node.right)

        # Both sides reported a target found -- this is the fork
        # point where p and q's paths diverge, so it's the LCA.
        if found_left and found_right:
            lca[0] = node

        # Pass the "found something" signal upward either way.
        return found_left or found_right

    lca_helper(root)
    return lca[0]


def main() -> None:
    root = build_example_tree()

    g = find_node(root, "G")
    h = find_node(root, "H")
    d = find_node(root, "D")
    f = find_node(root, "F")

    print("LCA of G, H:", lowest_common_ancestor(root, g, h).val)
    print("LCA of D, H:", lowest_common_ancestor(root, d, h).val)
    print("LCA of D, F:", lowest_common_ancestor(root, d, f).val)

if __name__ == "__main__":
    main()