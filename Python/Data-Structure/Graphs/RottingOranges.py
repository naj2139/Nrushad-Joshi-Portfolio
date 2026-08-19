from __future__ import annotations
from collections import deque


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        """Return the minimum minutes until no fresh orange remains.

        Args:
            grid: 2D grid of 0 (empty), 1 (fresh orange), or 2 (rotten
                orange).

        Returns:
            The minimum number of minutes until no cell has a fresh
            orange, or -1 if some fresh orange can never rot.
        """
        row = len(grid)
        col = len(grid[0])

        def stillFreshOrange(grid: list[list[int]]) -> bool:
            # True only if a fresh orange AND a rotten orange both
            # exist somewhere in the grid. Used after a BFS run: if
            # rot happened (a 2 exists) but a 1 is still left over,
            # that fresh orange was unreachable.
            one, two = False, False
            for line in grid:
                if 1 in line:
                    one = True
                if 2 in line:
                    two = True
                if one and two:
                    return True
            return False

        def findRottingOranges(r: int, c: int) -> int:
            # Multi-source in spirit: this starts from ONE rotten
            # orange, but every rotten orange found later during BFS
            # gets folded into the queue as new sources too, since any
            # of them can independently rot their own neighbors in the
            # same minute.
            queue = deque([[[r, c]]])
            memo = set((r, c))
            minute = 0

            while queue:
                # One popped `node` = everything rotting THIS minute.
                node = queue.popleft()
                isFreshOrange = False

                for cord in node:
                    x, y = cord
                    tracker = []

                    if grid[x][y] == 1:
                        grid[x][y] = 2

                    if x + 1 < row and (x + 1, y) not in memo:
                        if grid[x + 1][y] == 1:
                            isFreshOrange = True
                            tracker.append([x + 1, y])
                        memo.add((x + 1, y))

                    if x - 1 >= 0 and (x - 1, y) not in memo:
                        if grid[x - 1][y] == 1:
                            isFreshOrange = True
                            tracker.append([x - 1, y])
                        memo.add((x - 1, y))

                    if y + 1 < col and (x, y + 1) not in memo:
                        if grid[x][y + 1] == 1:
                            isFreshOrange = True
                            tracker.append([x, y + 1])
                        memo.add((x, y + 1))

                    if y - 1 >= 0 and (x, y - 1) not in memo:
                        if grid[x][y - 1] == 1:
                            isFreshOrange = True
                            tracker.append([x, y - 1])
                        memo.add((x, y - 1))

                    if tracker:
                        # Every newly-found fresh neighbor from this
                        # coordinate joins the queue -- not just the
                        # first one -- so nothing gets silently dropped
                        # from future exploration.
                        queue.append(tracker)

                # minute increments once per POPPED NODE (one full
                # minute / one full wave), not once per coordinate
                # inside it -- otherwise a wave that rots multiple
                # oranges at once would overcount the elapsed time.
                if isFreshOrange:
                    minute += 1

            if stillFreshOrange(grid):
                return -1
            return minute

        for r in range(row):
            for c in range(col):
                if grid[r][c] == 2:
                    return findRottingOranges(r, c)

        # No rotten orange existed anywhere in the grid to begin with,
        # so findRottingOranges was never called. stillFreshOrange
        # can't be reused here -- it requires a 1 AND a 2 to coexist,
        # but there was never a 2 at all in this branch. The only
        # question that matters is whether any fresh orange exists.
        for line in grid:
            if 1 in line:
                return -1
        return 0


def main() -> None:
    sol = Solution()

    grid1 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
    ]
    print(sol.orangesRotting(grid1))
    # Expected: 4

    grid2 = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1],
    ]
    print(sol.orangesRotting(grid2))
    # Expected: -1
    # (the orange at bottom-left is isolated by empty cells)

    grid3 = [[0, 2]]
    print(sol.orangesRotting(grid3))
    # Expected: 0
    # (no fresh oranges to begin with)

    grid4 = [[1]]
    print(sol.orangesRotting(grid4))
    # Expected: -1
    # (a fresh orange with no rotten orange anywhere)

    grid5 = [[2]]
    print(sol.orangesRotting(grid5))
    # Expected: 0


if __name__ == "__main__":
    main()