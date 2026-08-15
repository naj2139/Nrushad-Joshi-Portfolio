"""Word Search (LeetCode 79) — backtracking solution.

Given an m x n grid of characters and a string word, return True if word
exists in the grid via a path of horizontally/vertically adjacent cells,
using each cell at most once.
"""

from __future__ import annotations


class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        """Return True if word can be constructed from adjacent cells in board.

        Args:
            board: 2D grid of characters.
            word: Target string to find.

        Returns:
            True if word exists in the grid via a sequential path of
            adjacent cells, False otherwise.
        """
        row = len(board)
        col = len(board[0])

        def backtrack(r: int, c: int, idx: int, memo: set[tuple[int, int]]) -> bool:
            """Try to match word[idx:] starting at cell (r, c).

            Returns True the moment a full match is found along this path,
            False if this path is a dead end.
            """
            # --- Guard clause: bounds, revisit, and letter-mismatch checks ---
            # These three conditions are unrelated failure modes, but they all
            # mean the same thing for this call: "this path is dead, stop here
            # and let the caller try its OTHER directions." Returning False
            # here does NOT mean the whole search failed — `found` below
            # combines four such calls with `or`, so one False branch just
            # gets ignored as long as another branch succeeds.
            #
            # NOTE: order matters. We check bounds/visited BEFORE indexing
            # into board[r][c], otherwise an out-of-bounds (r, c) would raise
            # an IndexError. Short-circuit evaluation of `or` guarantees the
            # board lookup only happens once r, c are known to be valid.
            if (
                r < 0
                or r > row - 1
                or c < 0
                or c > col - 1
                or (r, c) in memo
                or board[r][c] != word[idx]
            ):
                return False

            # --- Base case: last character of word matched ---
            # This check happens BEFORE any recursive call with idx + 1, so
            # idx never exceeds len(word) - 1. The moment idx reaches the
            # final valid index, we return True immediately instead of
            # recursing further — this is what prevents an IndexError on
            # word[idx] in future calls.
            if idx == len(word) - 1:
                return True

            # --- Mark this cell as used for the current path ---
            # memo is a single shared set threaded through every recursive
            # call (unlike idx, which is a plain int copied by value into
            # each call). Because it's shared and mutable, we must add it
            # here and explicitly remove it below on the way back out —
            # otherwise sibling branches that never actually visited (r, c)
            # would incorrectly treat it as visited.
            memo.add((r, c))

            # Explore all 4 directions looking for word[idx + 1]. `or`
            # short-circuits, but even without that, four False/True values
            # OR'd together correctly yield True iff at least one direction
            # leads to a full match.
            found = (
                backtrack(r + 1, c, idx + 1, memo)
                or backtrack(r - 1, c, idx + 1, memo)
                or backtrack(r, c + 1, idx + 1, memo)
                or backtrack(r, c - 1, idx + 1, memo)
            )

            # --- Unmask: undo the visit so other paths can reuse this cell ---
            # Backtracking requires this cleanup on every return path, not
            # just the failing ones, since (r, c) may be part of a valid
            # path starting from a different neighbor.
            memo.remove((r, c))
            return found

        # Try every cell as a possible starting point. A separate cell (e.g.
        # a standalone "EE" not adjacent to any "S") can never be reached by
        # backtrack() from an unrelated "S" cell, because backtrack only ever
        # steps to geometric neighbors — there's no global "seen this letter
        # somewhere" tracking. So each starting cell gets its own fresh
        # attempt with idx=0 and an empty memo.
        #
        # This double loop is unavoidable in principle: the word could start
        # anywhere, and nothing short of checking (or pruning) every cell can
        # know that in advance. It could be written with itertools.product or
        # any(...) for style, but it's still fundamentally "consider every
        # cell as a candidate start."
        for r in range(row):
            for c in range(col):
                if backtrack(r, c, 0, set()):
                    return True

        return False


def main() -> None:
    sol = Solution()

    board1 = [["A", "B", "C", "E"],
              ["S", "F", "C", "S"],
              ["A", "D", "E", "E"]]
    print(sol.exist(board1, "ABCCED"))
    # Expected: True

    board2 = [["A", "B", "C", "E"],
              ["S", "F", "C", "S"],
              ["A", "D", "E", "E"]]
    print(sol.exist(board2, "SEE"))
    # Expected: True

    board3 = [["A", "B", "C", "E"],
              ["S", "F", "C", "S"],
              ["A", "D", "E", "E"]]
    print(sol.exist(board3, "ABCB"))
    # Expected: False (reuses the 'B' cell, not allowed)

    board4 = [["A"]]
    print(sol.exist(board4, "A"))
    # Expected: True

    board5 = [["A"]]
    print(sol.exist(board5, "AB"))
    # Expected: False (word longer than available unique path)


if __name__ == "__main__":
    main()