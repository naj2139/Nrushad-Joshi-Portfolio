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
    Construct a tree where the diameter passes through the root.

            A
           / \
          B   C
         /     \
        D       E
       /         \
      F           G
    """
    root = TreeNode("A")
    root.left, root.right = TreeNode("B"), TreeNode("C")
    root.left.left, root.right.right = TreeNode("D"), TreeNode("E")
    root.left.left.left, root.right.right.right = TreeNode("F"), TreeNode("G")

    return root


def build_off_root_example_tree() -> TreeNode:
    r"""
    Construct a tree where the diameter does NOT pass through the root.

            A
           /
          B
         / \
        D   E
       / \   \
      F   G   H
               \
                I
    """
    root = TreeNode("A")
    root.left = TreeNode("B")
    root.left.left, root.left.right = TreeNode("D"), TreeNode("E")
    root.left.left.left, root.left.left.right = TreeNode("F"), TreeNode("G")
    root.left.right.right = TreeNode("H")
    root.left.right.right.right = TreeNode("I")

    return root


def diameter_of_tree(root: TreeNode | None) -> int:
    """
    The diameter of a binary tree is the length (in edges) of the
    longest path between any two nodes in the tree. That path may or
    may not pass through the root.

    For any given node, there are three candidates for where the
    longest path in ITS subtree could be:
        1. the longest path that passes through this node itself
        2. the longest path found entirely within its left subtree
        3. the longest path found entirely within its right subtree

    A node doesn't know in advance which of these three is largest --
    it has to check all three and take the max. This must happen at
    EVERY node, not just the root, because the true longest path in
    the whole tree could be buried anywhere -- entirely inside some
    subtree that never touches the root at all.

    Given the root of a tree, this function should return the length
    of the longest path anywhere in the tree, as a number of edges.
    """

    # Approach:
    #   A single post-order traversal computes both a height and a
    #   running "best diameter so far" at the same time, so the tree
    #   only needs to be walked once (O(n)), instead of recomputing
    #   height from scratch at every node (which would be O(n^2)).
    #
    #   `res` is a running maximum shared across every recursive call.
    #   A one-element list (`res = [0]`) is used instead of a plain
    #   int because the nested helper needs to MUTATE it on every
    #   improvement -- Python closures can freely READ an outer
    #   variable, but reassigning a plain int from inside a nested
    #   function requires declaring it `nonlocal` first. Mutating
    #   res[0] in place sidesteps that entirely, since the list
    #   object itself is never reassigned, only the value at index 0.

    res = [0]
    def diameter_of_tree_helper(node: TreeNode | None) -> int:
        # Base case: an empty subtree has height 0 and contributes
        # no path.
        if not node:
            return 0
        # Recurse on both children first (post-order / bottom-up) --
        # each call already folds in every candidate found deeper in
        # that subtree, via its own recursive calls to res[0].
        left = diameter_of_tree_helper(node.left)
        right = diameter_of_tree_helper(node.right)
        # This node's height: one more than the taller of its two
        # children. This is the only thing returned up to the
        # parent -- diameter itself never gets returned, only
        # accumulated in res.
        height = 1 + max(left, right)
        # The longest path THROUGH this node = left + right.
        # left/right already represent how many edges each side
        # reaches down, so summing them gives the total edge count
        # of the path that enters this node from one side and exits
        # out the other. Update the running best if this beats it.
        if left + right > res[0]:
            res[0] = left + right
        return height
    diameter_of_tree_helper(root)
    return res[0]


def main() -> None:
    through_root = build_example_tree()
    off_root = build_off_root_example_tree()

    print("Through-root tree -> Diameter:", diameter_of_tree(through_root))
    print("Off-root tree      -> Diameter:", diameter_of_tree(off_root))


if __name__ == "__main__":
    main()