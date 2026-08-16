from __future__ import annotations


class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        """Return the count of islands in the grid using recursive DFS.

        Args:
            grid: 2D grid of '1' (land) and '0' (water) characters.

        Returns:
            The number of distinct islands, where an island is a
            group of horizontally/vertically connected '1' cells.
        """
        memo: set[tuple[int, int]] = set()
        row, col = len(grid), len(grid[0])

        def traversal(r: int, c: int, memo: set[tuple[int, int]]) -> None:
            # traversal has exactly ONE job: flood-fill outward from
            # (r, c), marking every connected land cell as visited. It
            # does not count anything and does not return a value --
            # counting is a separate responsibility that belongs to the
            # outer loop below. Mixing the two (e.g. returning a size or
            # a boolean from here) is what causes fragile, coincidental
            # results -- see the debugging history in this problem's
            # conversation for a concrete example of that going wrong.
            if (
                r > row - 1
                or r < 0
                or c > col - 1
                or c < 0
                or (r, c) in memo
            ):
                return

            memo.add((r, c))

            # grid holds the STRING "0"/"1", not the integer 0/1.
            # Comparing against the wrong type (grid[r][c] == 0) silently
            # never matches, which breaks the "water cells are already
            # accounted for" guarantee the outer loop relies on.
            if grid[r][c] == "0":
                return

            traversal(r + 1, c, memo)
            traversal(r - 1, c, memo)
            traversal(r, c + 1, memo)
            traversal(r, c - 1, memo)

        count = 0
        for r in range(row):
            for c in range(col):
                # Pre-mark water cells so the flood-fill and this loop
                # never have to re-examine them.
                if grid[r][c] == "0":
                    memo.add((r, c))
                    continue

                # A cell not yet in memo means it's land that hasn't been
                # claimed by any previous flood-fill -- i.e. the FIRST
                # time we're seeing a brand new island. That's exactly
                # the moment to increment the counter -- once per island
                # discovered, not once per cell visited.
                if (r, c) not in memo:
                    traversal(r, c, memo)
                    count += 1

        return count


def main() -> None:
    sol = Solution()

    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    print(sol.numIslands(grid1))
    # Expected: 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print(sol.numIslands(grid2))
    # Expected: 3

    grid3 = [["0"]]
    print(sol.numIslands(grid3))
    # Expected: 0

    grid4 = [["1"]]
    print(sol.numIslands(grid4))
    # Expected: 1
    # A single land cell is still its own island -- an island just
    # means "a maximal group of connected land," and a group can have
    # exactly one member.


if __name__ == "__main__":
    main()