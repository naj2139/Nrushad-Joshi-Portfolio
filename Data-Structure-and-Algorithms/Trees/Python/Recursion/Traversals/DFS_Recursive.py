from TreeNode import TreeNode


# ==========================================================
# Recursive DFS Traversals
# ==========================================================
#
# Key recursion concepts:
# -----------------------
# - A recursive call PAUSES the current function; it does NOT
#   terminate it.
#
# - Once the recursive call reaches the base case and returns,
#   execution resumes at the next line after the recursive call.
#
# - Unlike linear recursion, every tree node creates TWO
#   smaller subproblems:
#
#       Left Subtree
#       Right Subtree
#
# - The base case checks whether the CURRENT node exists,
#   not whether it is a leaf.
#
#       if root is None:
#           return
#
# - A leaf node executes normally:
#
#       visit(root)
#       dfs(None)
#       dfs(None)
#
# - There is no need to check:
#
#       if root.left:
#       if root.right:
#
#   because dfs(None) immediately reaches the base case.
#
# - Returning only ends the CURRENT recursive call.
#   The caller resumes execution immediately after the
#   recursive call returns.
#
# ==========================================================


class DFSRecursive:

    # ----------------------------------------------------------
    # Preorder Traversal
    # ----------------------------------------------------------
    #
    # Traversal order:
    #
    #   Current Node
    #   Left Subtree
    #   Right Subtree
    #
    # Example:
    #
    #       2
    #      / \
    #     1   3
    #
    # Output:
    # 2
    # 1
    # 3
    #
    # Concept:
    # Visit the current node BEFORE traversing either subtree.

    def preorder(self, root: TreeNode) -> None:

        # Base case: an empty subtree has nothing to traverse.
        if root is None:
            return

        # Visit the current node.
        print(root.val)

        # Traverse the left subtree.
        self.preorder(root.left)

        # Traverse the right subtree.
        self.preorder(root.right)

    # ----------------------------------------------------------
    # Inorder Traversal
    # ----------------------------------------------------------
    #
    # Traversal order:
    #
    #   Left Subtree
    #   Current Node
    #   Right Subtree
    #
    # Example:
    #
    #       2
    #      / \
    #     1   3
    #
    # Output:
    # 1
    # 2
    # 3
    #
    # Concept:
    # Visit the current node AFTER the left subtree has been
    # completely traversed and BEFORE traversing the right subtree.

    def inorder(self, root: TreeNode) -> None:

        # Base case: an empty subtree has nothing to traverse.
        if root is None:
            return

        # Traverse the left subtree.
        self.inorder(root.left)

        # Visit the current node.
        print(root.val)

        # Traverse the right subtree.
        self.inorder(root.right)

    # ----------------------------------------------------------
    # Postorder Traversal
    # ----------------------------------------------------------
    #
    # Traversal order:
    #
    #   Left Subtree
    #   Right Subtree
    #   Current Node
    #
    # Example:
    #
    #       2
    #      / \
    #     1   3
    #
    # Output:
    # 1
    # 3
    # 2
    #
    # Concept:
    # Visit the current node AFTER both subtrees have been
    # completely traversed.

    def postorder(self, root: TreeNode) -> None:

        # Base case: an empty subtree has nothing to traverse.
        if root is None:
            return

        # Traverse the left subtree.
        self.postorder(root.left)

        # Traverse the right subtree.
        self.postorder(root.right)

        # Visit the current node.
        print(root.val)