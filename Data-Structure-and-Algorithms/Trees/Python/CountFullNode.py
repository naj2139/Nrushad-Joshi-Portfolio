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

    Full nodes = 9
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


def count_full_node(root: TreeNode | None) -> int:
    """
    Return the total number of full nodes in a binary tree.

    A full node is a node with exactly two children.
    Nodes with one child or no children (leaf nodes) are not counted.
    """

    # ------------------------------------------------------------------
    # Initial approach (expanded logic)
    #
    # This version explicitly handles every possible case:
    #
    # 1. Empty tree
    # 2. Leaf node
    # 3. Node with only a left child
    # 4. Node with only a right child
    # 5. Node with both children
    #
    # Although correct, it requires several conditional statements.
    #
    # def count_full_node(root: TreeNode | None) -> int:
    #     if not root or (not root.left and not root.right):
    #         return 0
    #
    #     if root.right and not root.left:
    #         return count_full_node(root.right)
    #
    #     if root.left and not root.right:
    #         return count_full_node(root.left)
    #
    #     if root.left and root.right:
    #         return (
    #             1
    #             + count_full_node(root.left)
    #             + count_full_node(root.right)
    #         )
    # ------------------------------------------------------------------

    # An empty tree (or empty subtree) contains no full nodes.
    if not root:
        return 0

    # Count the current node if it has both a left and a right child.
    # Otherwise, contribute 0 to the total count.
    current = 1 if root.left and root.right else 0

    # Recursively count the full nodes in the left and right subtrees,
    # then combine the results with the current node.
    return current + count_full_node(root.left) + count_full_node(root.right)

def main() -> None:
    root = build_example_tree()
    print("Total Full Node Count:", count_full_node(root))


if __name__ == "__main__":
    main()