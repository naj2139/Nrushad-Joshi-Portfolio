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
    guaranteed to exist somewhere in the tree), this function should
    return the TreeNode that is their lowest common ancestor.
    """
    pass

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