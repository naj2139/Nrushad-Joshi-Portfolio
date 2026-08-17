"""
LeetCode 733. Flood Fill
https://leetcode.com/problems/flood-fill/

Given an image (2D grid of colors) and a starting pixel (sr, sc), replace
the color of every pixel connected to the start (4-directionally, same
color) with a new color.
"""
from __future__ import annotations


class Solution:
    def floodFill(
        self, image: list[list[int]], sr: int, sc: int, color: int
    ) -> list[list[int]]:
        row = len(image)
        col = len(image[0])
        visited: set[tuple[int, int]] = set()

        # start_color is the color we're replacing. It is NOT a fixed
        # constant like 0 or 1 -- the grid could use any integers as
        # colors, and the region we flood-fill is defined by whatever
        # color happens to be sitting at (sr, sc) BEFORE we start
        # painting. We capture it once, up front, because image[sr][sc]
        # itself gets overwritten with `color` during the very first
        # step of the recursion -- if we checked image[sr][sc] again
        # later instead of this saved value, we'd be comparing against
        # the new color instead of the original one.
        start_color = image[sr][sc]

        def backtrack(r: int, c: int, visited: set[tuple[int, int]]) -> None:
            visited.add((r, c))

            # Stop if this cell isn't part of the original region.
            if image[r][c] != start_color:
                return

            image[r][c] = color

            if r + 1 < row and (r + 1, c) not in visited:
                backtrack(r + 1, c, visited)
            if r - 1 >= 0 and (r - 1, c) not in visited:
                backtrack(r - 1, c, visited)
            if c + 1 < col and (r, c + 1) not in visited:
                backtrack(r, c + 1, visited)
            if c - 1 >= 0 and (r, c - 1) not in visited:
                backtrack(r, c - 1, visited)

        backtrack(sr, sc, visited)
        return image


def main() -> None:
    sol = Solution()

    image1 = [[1, 1, 1],
              [1, 1, 0],
              [1, 0, 1]]
    print(sol.floodFill(image1, 1, 1, 2))
    # Expected: [[2, 2, 2], [2, 2, 0], [2, 0, 1]]

    # new color == old color -> no change needed
    image2 = [[0, 0, 0],
              [0, 0, 0]]
    print(sol.floodFill(image2, 0, 0, 0))
    # Expected: [[0, 0, 0], [0, 0, 0]]

    image3 = [[1, 1, 1],
              [1, 1, 1],
              [1, 1, 1]]
    print(sol.floodFill(image3, 1, 1, 5))
    # Expected: [[5, 5, 5], [5, 5, 5], [5, 5, 5]]


if __name__ == "__main__":
    main()