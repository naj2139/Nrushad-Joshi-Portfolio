class TreeNode:
    """
    Basic binary tree node.
    """

    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None


def build_example_tree() -> TreeNode:
    """
    Construct the example binary tree used throughout the project.

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


class Algorithm:

    def traversal(self, root):
        if not root:
            return
        print(root.val)
        self.traversal(root.left)
        self.traversal(root.right)

def main():
    root = build_example_tree()
    solver = Algorithm()
    result = solver.traversal(root)
    print(result)


if __name__ == "__main__":
    main()