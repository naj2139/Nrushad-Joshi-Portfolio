# Backtracking Practice

A collection of backtracking problems solved in Python, worked through in
roughly the order they appear in common algorithm study roadmaps (e.g.
NeetCode's Backtracking section). Each file is self-contained, runnable on
its own, and includes a `main()` with sample inputs and expected outputs
for quick verification.

## Structure

Every solution follows the same general pattern:

1. A `Solution` class with the method matching the problem's expected
   signature (as it would appear on LeetCode).
2. A nested `backtrack` (or similarly named) helper implementing the
   choose → explore → un-choose recursion.
3. A `main()` function at the bottom exercising the solution against a
   handful of test cases with their expected results noted inline.

Run any file directly to see its test cases execute:

```bash
python3 <filename>.py
```

## Problems

| File | Problem |
|---|---|
| `Subsets.py` | Generate all subsets of a list of unique elements |
| `SubsetII.py` | Generate all subsets of a list that may contain duplicates, without duplicate subsets in the result |
| `CombinationSum.py` | Find combinations of numbers summing to a target, with unlimited reuse |
| `CombinationSumII.py` | Same as above, but each number may be used at most once |
| `CombinationSumVariations...py` | Additional variations on the combination sum family |
| `Permutations.py` | Generate all permutations of a list of unique elements |
| `WordSearch.py` | Determine if a word can be constructed from adjacent cells in a grid |
| `FloodFILL.py` | Flood fill a region of a grid starting from a given cell |
| `CountPath.py` | Count paths through a grid under given movement rules |
| `UniquePathIII.py` | Count paths that visit every walkable square in a grid exactly once |
| `PalindromePartition.py` | Return all ways to split a string into palindromic substrings |
| `PalindromePartitionII.py` | Return the minimum number of cuts needed to split a string into palindromic substrings |
| `BinaryString.py` | Backtracking over binary string generation |

## Approach

Most solutions here follow the same recursive skeleton:

```python
def backtrack(state):
    if base_case_reached(state):
        record_result(state)
        return
    for choice in available_choices(state):
        if is_valid(choice, state):
            make_choice(choice, state)
            backtrack(next_state)
            undo_choice(choice, state)
```

The exact shape of `state` varies by problem — a string index, a grid
coordinate pair, a used-elements set, or a combination of these — but the
mark → recurse → unmark rhythm stays consistent throughout.

## Notes

- Solutions prioritize clarity over micro-optimization; some problems
  (e.g. `PalindromePartitionII.py`) have DP-based optimizations not
  implemented here.
- Test cases in each `main()` are meant as quick sanity checks, not
  exhaustive coverage.