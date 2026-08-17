# Trees — Python

Tree algorithm implementations, built as a structured self-study project
covering traversal, properties, comparisons, and path problems on trees.

## Structure

Every solution follows a consistent structure:

1. `from __future__ import annotations` at the top.
2. Type hints throughout (`Optional[TreeNode]`, `list[int]`, etc.).
3. A `TreeNode` class (or shared definition) representing a tree node.
4. `build_example_tree()` — constructs a sample tree for manual testing.
5. `main()` — entry point that builds the example tree and prints results.

Run any file directly to see it execute against the example tree:

```bash
python3 <filename>.py
```

## Problems

| File | Problem |
|---|---|
| **Traversal** | |
| `Traversal.py` | Preorder, inorder, postorder (and/or level-order) traversal |
| **Tree properties / counting** | |
| `CountNode.py` | Total number of nodes in the tree |
| `CountLeafNode.py` | Number of leaf nodes (no children) |
| `CountInternalNode.py` | Number of internal nodes (at least one child) |
| `CountFullNode.py` | Number of nodes where every child slot is filled |
| `CountSingleChildNode.py` | Number of nodes with only one child present |
| `SumNodeValues.py` | Sum of all node values |
| `MaxNodeValue.py` | Maximum value in the tree |
| `MinNodeValue.py` | Minimum value in the tree |
| `MaxDepth.py` | Maximum depth / height of the tree |
| `MinDepth.py` | Minimum depth (shortest path to a leaf) |
| `DiameterOfTree.py` | Longest path between any two nodes (in edges) |
| `IsBalanced.py` | Checks if the tree is height-balanced |
| **Search & lookup** | |
| `SearchNode.py` | Checks whether a given value exists in the tree |
| `LCA.py` | Lowest common ancestor of two nodes |
| **Comparisons** | |
| `IdenticalTree.py` | Checks if two trees are structurally identical with equal values |
| `AreMirrorTrees.py` | Checks if two trees are mirror images of each other |
| `IsSymmetric.py` | Checks if a single tree is a mirror of itself |
| **Transformations** | |
| `InvertTree.py` | Flips the tree (swaps child subtrees recursively) |
| **Path problems** | |
| `PathSum.py` | Checks if a root-to-leaf path sums to a target value |

## Approach

Nearly every solution here follows the same recursive skeleton:

```python
def solve(node: Optional[TreeNode]) -> ...:
    if node is None:
        return <base case>
    left = solve(node.left)
    right = solve(node.right)
    return <combine left, right, node.val>
```

Unlike backtracking's choose → explore → un-choose rhythm, tree recursion
here is typically choose-free — there's no "undo" step, since each call
simply computes a result from its subtrees and returns it upward rather
than mutating shared state along a path.

## Notes

- Solutions prioritize clarity over micro-optimization.
- `build_example_tree()` in each file is meant as a quick sanity check,
  not exhaustive test coverage.