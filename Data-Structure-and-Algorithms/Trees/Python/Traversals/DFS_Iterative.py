from TreeNode import TreeNode


# ==========================================================
# Iterative DFS Traversals
# ==========================================================
#
# Key iterative DFS concepts:
# ---------------------------
# - Recursive DFS uses the CALL STACK provided by Python.
#
# - Iterative DFS replaces the call stack with an explicit
#   STACK data structure (LIFO: Last-In, First-Out).
#
# - Every iteration:
#
#       1. Pop one node from the stack.
#       2. Visit the node.
#       3. Push its children onto the stack.
#
# - The order in which children are pushed determines the
#   traversal order.
#
# - Unlike recursion, there is no base case.
#   The traversal ends when the stack becomes empty.
#
# ==========================================================


class DFSIterative:

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
    # Data Structure:
    #
    #   Stack (LIFO)
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

    def preorder(self, root: TreeNode) -> None:
        # Start the traversal with the root node.
        stack = [root]

        # Continue until there are no more nodes to visit.
        while stack:
            # Remove the node on top of the stack.
            node = stack.pop()

            # Visit the current node.
            print(node.val)

            # Push the right child first so the left child
            # is processed first (LIFO stack behavior).
            if node.right:
                stack.append(node.right)

            # Push the left child after the right child.
            if node.left:
                stack.append(node.left)

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
    # Data Structure:
    #
    #   Stack (LIFO)
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

    def inorder(self, root: TreeNode) -> None:
        stack = [root]

        while stack:
            
            node = stack.pop()
            if node.right:
                stack.append(node.right)

            print(node.val)

            if node.left:
                stack.append(node.left)

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
    # Data Structure:
    #
    #   Stack (LIFO)
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

    def postorder(self, root: TreeNode) -> None:
        pass