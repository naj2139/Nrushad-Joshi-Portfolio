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
    root.left = TreeNode(25)
    root.right = TreeNode(75)

    # Level 3
    root.left.left = TreeNode(10)
    root.left.right = TreeNode(35)

    root.right.left = TreeNode(60)
    root.right.right = TreeNode(90)

    # Level 4
    root.left.left.left = TreeNode(5)
    root.left.left.right = TreeNode(15)

    root.left.right.left = TreeNode(30)
    root.left.right.right = TreeNode(40)

    root.right.left.left = TreeNode(55)
    root.right.left.right = TreeNode(65)

    root.right.right.left = TreeNode(80)
    root.right.right.right = TreeNode(95)

    # Level 5
    root.left.left.left.left = TreeNode(2)
    root.left.left.left.right = TreeNode(7)

    root.right.right.right.left = TreeNode(92)
    root.right.right.right.right = TreeNode(100)

    # Level 6
    root.left.left.left.left.left = TreeNode(1)

    return root


class Traversal:
    """
    Recursive binary tree traversal algorithms.
    """

    def preorder(self, root: TreeNode | None) -> None:
        """
        Traverse the tree in Root -> Left -> Right order.
        """

        # Base case: reached the end of a branch.
        if root is None:
            return

        # Process the current node.
        print(root.val)

        # Traverse the left subtree.
        self.preorder(root.left)

        # Traverse the right subtree.
        self.preorder(root.right)

    def inorder(self, root: TreeNode | None) -> None:
        """
        Traverse the tree in Left -> Root -> Right order.
        """

        # Base case: reached the end of a branch.
        if root is None:
            return

        # Traverse the left subtree.
        self.inorder(root.left)

        # Process the current node.
        print(root.val)

        # Traverse the right subtree.
        self.inorder(root.right)

    def postorder(self, root: TreeNode | None) -> None:
        """
        Traverse the tree in Left -> Right -> Root order.
        """

        # Base case: reached the end of a branch.
        if root is None:
            return

        # Traverse the left subtree.
        self.postorder(root.left)

        # Traverse the right subtree.
        self.postorder(root.right)

        # Process the current node.
        print(root.val)


def main() -> None:
    root = build_example_tree()
    traversal = Traversal()

    print("Preorder Traversal:")
    traversal.preorder(root)

    print("\nInorder Traversal:")
    traversal.inorder(root)

    print("\nPostorder Traversal:")
    traversal.postorder(root)


if __name__ == "__main__":
    main()