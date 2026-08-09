# Trees — Python

Tree algorithm implementations, built as a structured self-study project covering traversal, properties, comparisons, and path problems on trees.

## Conventions

Each script follows a consistent structure:
- `from __future__ import annotations` at the top
- Type hints throughout (`Optional[TreeNode]`, `list[int]`, etc.)
- A `TreeNode` class (or shared definition) representing a tree node
- `build_example_tree()` — constructs a sample tree for manual testing
- `main()` — entry point that builds the example tree and prints results

## Contents

### Traversal
- **Traversal.py** — preorder, inorder, postorder (and/or level-order) traversal implementations

### Tree properties / counting
- **CountNode.py** — total number of nodes in the tree
- **CountLeafNode.py** — number of leaf nodes (no children)
- **CountInternalNode.py** — number of internal nodes (at least one child)
- **CountFullNode.py** — number of nodes where every child slot is filled
- **CountSingleChildNode.py** — number of nodes with only one child present
- **SumNodeValues.py** — sum of all node values
- **MaxNodeValue.py** — maximum value in the tree
- **MinNodeValue.py** — minimum value in the tree
- **MaxDepth.py** — maximum depth / height of the tree
- **MinDepth.py** — minimum depth (shortest path to a leaf)
- **DiameterOfTree.py** — longest path between any two nodes (in edges)
- **IsBalanced.py** — checks if the tree is height-balanced

### Search & lookup
- **SearchNode.py** — checks whether a given value exists in the tree
- **LCA.py** — lowest common ancestor of two nodes

### Comparisons
- **IdenticalTree.py** — checks if two trees are structurally identical with equal values
- **AreMirrorTrees.py** — checks if two trees are mirror images of each other
- **IsSymmetric.py** — checks if a single tree is a mirror of itself

### Transformations
- **InvertTree.py** — flips the tree (swaps child subtrees recursively)

### Path problems
- **PathSum.py** — checks if a root-to-leaf path sums to a target value

## Core pattern

Nearly every solution here follows the same recursive shape:

```python
def solve(node: Optional[TreeNode]) -> ...:
    if node is None:
        return <base case>
    left = solve(node.left)
    right = solve(node.right)
    return <combine left, right, node.val>
```
