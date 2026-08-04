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
        stack = []
        curr = root

        while curr or stack:
            # Go as far left as possible, pushing each node we pass
            # onto the stack so we can come back to it later.
            while curr:
                stack.append(curr)
                curr = curr.left

            # No more left children to explore — pop the most recent
            # node we stacked. This is the next node in sorted/inorder order.
            node = stack.pop()
            print(node.val)

            # Now explore that node's right subtree the same way.
            # If there's no right child, curr becomes None, the inner
            # while loop is skipped, and we just pop the next parent
            # off the stack instead.
            curr = node.right


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
        stack = []
        curr = root
        last_visited = None

        while curr or stack:
            # Same as inorder: go all the way left, pushing as we go.
            while curr:
                stack.append(curr)
                curr = curr.left

            # Peek (don't pop yet) at the top of the stack.
            peek = stack[-1]

            # If there's an unvisited right child, we have to go explore
            # it before we're allowed to print this node — that's the
            # key difference from inorder.
            if peek.right and last_visited != peek.right:
                curr = peek.right
            else:
                # Right subtree is done (or doesn't exist), so NOW
                # we can finally print this node and pop it for real.
                print(peek.val)
                last_visited = stack.pop()            