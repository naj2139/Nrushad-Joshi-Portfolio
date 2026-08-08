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
    Construct an unbalanced binary tree.

            1
           / \
          2   3
         /
        4
       /
      5
    """
    root = TreeNode(1)
    root.left, root.right = TreeNode(2), TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.left.left = TreeNode(5)

    return root


def build_balanced_example_tree() -> TreeNode:
    """
    Construct a balanced binary tree.

              50
             /  \
           25    75
          / \    / \
        10  35  60  90
    """
    root = TreeNode(50)
    root.left, root.right = TreeNode(25), TreeNode(75)
    root.left.left, root.left.right = TreeNode(10), TreeNode(35)
    root.right.left, root.right.right = TreeNode(60), TreeNode(90)

    return root

# =============================================================================
# My First Attempt
# =============================================================================
# def is_balanced_helper(root: TreeNode):
#     if not root:
#         return (0, None)     
#     left = is_balanced_helper(root.left)
#     right = is_balanced_helper(root.right)
#     left_height, left_val = left[0]+1, left[1]
#     right_height, right_val = right[0]+1, right[1]
#     print(left_height, right_height)
#     print(left_val, right_val)
#     height = max(left_height, right_height)
#     if left_val is False or right_val is False:
#         return (height, False)  
#     if abs(left_height-right_height)>1:
#         return (height,False)
#     else:
#         return(height, True) 
# return is_balanced_helper(root)[1]


def is_balanced(root: TreeNode | None) -> bool:
    """
    A binary tree is "height-balanced" if, for every node in the tree,
    the height of its left subtree and the height of its right subtree
    differ by no more than 1.
 
    This must hold true at EVERY node, not just the root. A tree can
    look fine at the top level while having a lopsided cluster of
    nodes hidden deep in some subtree -- and that alone makes the
    whole tree unbalanced, even if everything above it looks okay.
 
    Given the root of a tree, returns True if the tree is balanced
    everywhere, or False if there is at least one node where the
    left/right height difference exceeds 1.
 
    This keeps the original (height, is_balanced) tuple approach,
    with two cleanups:
        1. The base case returns (0, True) instead of (0, None).
           An empty subtree IS trivially balanced, so True is the
           semantically correct value -- no None-handling required
           anywhere else in the function.
        2. Once either child already reports False, the height
           comparison at the current node is skipped entirely via
           short-circuit evaluation ("or" stops at the first True
           operand), since the tree is already known unbalanced
           regardless of what this node's own heights look like.
 
    Time complexity:  O(n) -- each node is visited exactly once.
    Space complexity: O(h) -- recursion stack depth equals tree height.
    """
 
    def is_balanced_helper(node: TreeNode | None) -> tuple[int, bool]:
        # Base case: an empty subtree has height 0 and is trivially balanced.
        if not node:
            return (0, True)
 
        left_height, left_balanced = is_balanced_helper(node.left)
        right_height, right_balanced = is_balanced_helper(node.right)
 
        height = 1 + max(left_height, right_height)
        
        # A subtree is unbalanced if ANY ONE of these is true:
        #   1. the left side already had a problem somewhere inside it
        #   2. the right side already had a problem somewhere inside it
        #   3. right here, at this node, the two sides' heights are
        #      too far apart (more than 1)
        #
        # Check each condition one at a time, in plain if/else form.
        # As soon as one of them is true, we know the answer -- False --
        # so we stop and return right away instead of checking the rest.
 
        if left_balanced == False:
            return (height, False)
 
        if right_balanced == False:
            return (height, False)
 
        if abs(left_height - right_height) > 1:
            return (height, False)
 
        # None of the three problems above happened, so this subtree
        # is balanced.
        return (height, True)
 
    return is_balanced_helper(root)[1]

def main() -> None:
    unbalanced_root = build_example_tree()
    balanced_root = build_balanced_example_tree()

    print("Unbalanced tree -> Is Balanced:", is_balanced(unbalanced_root))

    print("Balanced tree   -> Is Balanced:", is_balanced(balanced_root))


if __name__ == "__main__":
    main()