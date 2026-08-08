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
    """
    Construct a tree where the diameter does NOT pass through the root.

            A
           /
          B
         / \
        D   E
       /     \
      F       H
     /         \
    (F, G)      I

    (D has children F and G; E has child H; H has child I)
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

    res = [0]

    def diameter_of_tree_helper(root: TreeNode | None):
        global res

        if not root:
            return 0

        left = 1 + diameter_of_tree_helper(root.left)
        right = 1 + diameter_of_tree_helper(root.right)

        height = max(left, right)

        if left + right > res[0]:
            res[0] = left + right

        return height

    height = diameter_of_tree_helper(root)
    print(res[0])
    return height


def main() -> None:
    through_root = build_example_tree()
    off_root = build_off_root_example_tree()

    print("Through-root tree -> Diameter:", diameter_of_tree(through_root))
    print("Off-root tree      -> Diameter:", diameter_of_tree(off_root))


if __name__ == "__main__":
    main()