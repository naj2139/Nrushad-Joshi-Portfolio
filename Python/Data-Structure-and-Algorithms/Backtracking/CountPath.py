from __future__ import annotations

# =============================================================================
# My First Attempt
# =============================================================================
# def count_paths_first_attempt(grid: list[list[int]]) -> None:
#     count = [0]
#     row = len(grid)
#     col = len(grid[0])
#     memo = set()

#     def backtrack(r: int, c: int, memo: set[tuple[int, int]]) -> None:
#         if r > row - 1 or r < 0 or c > col - 1 or c < 0 or (r, c) in memo:
#             return
#         memo.add((r, c))

#         if r == 2 and c == 2:
#             count[0] += 1
#             memo.remove((r, c))
#             return

#         if grid[r][c] == 1:
#             memo.remove((r, c))
#             return
#         backtrack(r + 1, c, memo)
#         backtrack(r - 1, c, memo)
#         backtrack(r, c + 1, memo)
#         backtrack(r, c - 1, memo)

#         memo.remove((r, c))

#     backtrack(0, 0, memo)
#     print(count)


# =============================================================================
# Final Version
# =============================================================================


def count_paths(grid: list[list[int]]) -> int:
    """Count distinct paths from top-left to bottom-right of a grid.

    Movement is 4-directional (up/down/left/right). A cell with value 1 is
    an obstacle and cannot be entered. A cell already used earlier in the
    CURRENT path cannot be reused, but becomes available again for other,
    later-explored paths once backtracking steps back past it.

    Args:
        grid: 2D grid of 0s (open) and 1s (obstacle).

    Returns:
        The number of distinct valid paths from (0, 0) to
        (rows - 1, cols - 1).
    """
    rows = len(grid)
    cols = len(grid[0])
    target = (rows - 1, cols - 1)
    visited: set[tuple[int, int]] = set()
    path_count = 0

    def backtrack(r: int, c: int) -> None:
        nonlocal path_count

        # Single guard clause covers every reason a cell is NOT enterable:
        # out of bounds, already on the current path, or an obstacle.
        # Folding grid[r][c] == 1 in here -- rather than checking it after
        # marking -- means an obstacle is rejected at the door and never
        # gets added to `visited` in the first place. That removes any
        # need to clean it back up: nothing was marked, so there's nothing
        # to unmark.
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or (r, c) in visited
            or grid[r][c] == 1
        ):
            return

        # Reaching the target completes one distinct path. Return
        # immediately -- don't mark this cell or keep exploring past it.
        # Continuing past the goal wastes recursive calls exploring
        # branches that can never increment path_count again (the target
        # would need to be revisited to count again, and it's never
        # marked visited, so nothing here relies on that anyway -- but
        # returning early keeps the traversal correct and inexpensive).
        if (r, c) == target:
            path_count += 1
            return

        # --- MARK: (r, c) is now part of the path currently being traced ---
        visited.add((r, c))

        # --- RECURSE: try extending the path in all 4 directions ---
        backtrack(r + 1, c)
        backtrack(r - 1, c)
        backtrack(r, c + 1)
        backtrack(r, c - 1)

        # --- UNMARK: stepping back, so (r, c) is free for OTHER paths ---
        # This is what keeps `visited` representing only "cells on the
        # path currently being traced," not "every cell ever touched."
        # Without this pairing, an earlier failed branch could
        # permanently block cells that a later, unrelated branch
        # legitimately needs -- producing a false negative.
        visited.remove((r, c))

    backtrack(0, 0)
    return path_count


def main() -> None:
    grid1 = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    print(count_paths(grid1))
    # Expected: 2 distinct paths from (0,0) to (2,2)

    # Obstacle NOT at (1,1) -- this is exactly the case that breaks the
    # hardcoded memo.remove((1,1)) from the first attempt but works fine
    # here since the final version never hardcodes a coordinate.
    grid2 = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 0],
    ]
    print(count_paths(grid2))
    # Expected: 4 distinct paths from (0,0) to (2,2)

    grid3 = [[0]]
    print(count_paths(grid3))
    # Expected: 1 (start == target)

if __name__ == "__main__":
    main()