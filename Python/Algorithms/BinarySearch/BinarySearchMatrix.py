from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # Binary search over the FIRST COLUMN to find which row target
        # would belong to. This reuses the exact same "low converges to
        # the insertion index" idea from LC 35 (Search Insert Position) --
        # if target isn't the first element of any row, the base case
        # returns `low`, which is the index of the first row whose
        # starting value is greater than target.
        def searchRow(low, high):
            if high >= low:
                half = (low + high) // 2
                if matrix[half][0] == target:
                    return True
                elif matrix[half][0] > target:
                    return searchRow(low, half - 1)
                else:
                    return searchRow(half + 1, high)
            else:
                return low

        # Standard binary search within a single row.
        def searchCol(low, high, row):
            if high >= low:
                half = (low + high) // 2
                if row[half] == target:
                    return True
                elif row[half] > target:
                    return searchCol(low, half - 1, row)
                else:
                    return searchCol(half + 1, high, row)
            else:
                return False

        row_idx = searchRow(0, len(matrix) - 1)
        if row_idx is True:
            return True

        # row_idx is the first row whose starting value EXCEEDS target,
        # so target (if present) must live in the PREVIOUS row instead --
        # step back one, unless we're already at row 0. `if row_idx > 0`
        # (not `>=`) matters here: row_idx is already guaranteed to be
        # >= 0 (searchRow's `low` starts at 0 and never goes negative),
        # so `> 0` correctly leaves row_idx untouched when target is
        # smaller than every row's starting value -- row 0 is still the
        # only row worth checking in that case. Using `>= 0` would
        # trigger on row_idx == 0 too and push it to -1, wrapping around
        # to the LAST row in Python and searching completely the wrong
        # place.
        if row_idx > 0:
            row_idx -= 1

        return searchCol(0, len(matrix[0]) - 1, matrix[row_idx])


if __name__ == "__main__":
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target = 3

    sol = Solution()
    result = sol.searchMatrix(matrix, target)

    print(result)