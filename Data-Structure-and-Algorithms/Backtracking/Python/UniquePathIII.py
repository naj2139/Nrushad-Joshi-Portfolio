from __future__ import annotations


class Solution:
    def uniquePathsIII(self, grid: list[list[int]]) -> int:
        """Return the count of paths visiting every walkable square exactly once.

        Args:
            grid: 2D grid containing 1 (start), 2 (end), 0 (empty), -1 (obstacle).

        Returns:
            Number of distinct paths from start to end covering all
            non-obstacle squares exactly once.
        """
        row, col = len(grid), len(grid[0])
        count = [0]

        # `total` tracks how many empty (0) squares still need to be visited
        # before the path is allowed to finish at the end square. Only 0
        # cells ever increment/decrement it -- the start (1) and end (2)
        # squares deliberately never touch it, since they aren't part of
        # the "must visit" 0-count this variable represents.
        total = [sum(row_.count(0) for row_ in grid)]

        def backtrack(r: int, c: int, memo: set[tuple[int, int]]) -> None:
            # --- Guard clause: every reason this cell can't be entered ---
            # Bounds, already-on-this-path, and obstacles are all "dead end,
            # no side effects" cases -- they return before any mutation.
            # The final condition additionally rejects landing on the end
            # square *early* (before all 0s are visited): reaching (r, c)
            # with total[0] != 0 means squares are still unvisited, so this
            # is an incomplete path, not a valid finish.
            if (
                r >= row
                or r < 0
                or c >= col
                or c < 0
                or (r, c) in memo
                or total[0] < 0
                or grid[r][c] == -1
                or (total[0] != 0 and grid[r][c] == 2)
            ):
                return

            # --- Success: reached the end with every 0 square visited ---
            if total[0] == 0 and grid[r][c] == 2:
                count[0] += 1
                return

            # --- Mark: only 0 cells count against the "must visit" total ---
            # The start cell (1) intentionally skips this -- it was never
            # part of the 0-count total represents, so it must not
            # decrement it (doing so would throw off the total[0] == 0
            # check at the finish line).
            if grid[r][c] == 0:
                total[0] -= 1

            memo.add((r, c))
            backtrack(r + 1, c, memo)
            backtrack(r - 1, c, memo)
            backtrack(r, c + 1, memo)
            backtrack(r, c - 1, memo)
            memo.remove((r, c))

            # --- Unmark: mirror the mark step exactly ---
            # Must use the same `grid[r][c] == 0` condition as the
            # decrement above. Mismatched mark/unmark conditions (e.g.
            # conditional decrement paired with an unconditional increment)
            # silently corrupt `total[0]` for every path explored afterward,
            # since it's shared, mutable state threaded through the whole
            # recursion tree -- not scoped per-path the way `memo` is.
            if grid[r][c] == 0:
                total[0] += 1

        # The word "start" can be anywhere in the grid, so every cell must
        # be checked as a candidate. Only the single cell marked 1 actually
        # begins a search.
        for r in range(row):
            for c in range(col):
                if grid[r][c] == 1:
                    backtrack(r, c, set())

        return count[0]


def main() -> None:
    sol = Solution()

    grid1 = [[1, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 2, -1]]
    print(sol.uniquePathsIII(grid1))
    # Expected: 2

    grid2 = [[1, 0, 0, 0],
             [0, -1, 0, 0],
             [0, 0, 0, 2]]
    print(sol.uniquePathsIII(grid2))
    # Expected: 0
    # (0,1)'s only neighbors are the start and (0,2); (1,0)'s only
    # reachable neighbor -- once the start is used up -- is (2,0). That
    # makes (1,0) a dead end that can only ever be a path's LAST cell, but
    # the path must end at (2,3), not (1,0). No full-coverage path exists.

    grid3 = [[0, 1],
             [2, 0]]
    print(sol.uniquePathsIII(grid3))
    # Expected: 0
    # Both possible 3-cell routes from start to end skip one of the four
    # walkable squares, so neither achieves full coverage.

if __name__ == "__main__":
    main()