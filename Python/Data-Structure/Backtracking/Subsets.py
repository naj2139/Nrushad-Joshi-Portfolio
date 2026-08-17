from __future__ import annotations

from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        # =============================================================================
        # My First Attempt
        # =============================================================================
        # result: List[List[int]] = []
        # path: List[int] = []
        #
        # def backtrack(start) -> None:
        #     for idx in range(start, len(nums)):
        #         path.append(nums[idx])
        #         backtrack(idx+1)
        #         result.append(path[:])
        #         path.pop()
        # backtrack(0)
        # result.append(path)
        # return result

        # =============================================================================
        # Optimized
        # =============================================================================
        # Record the subset once per call, unconditionally, before the for
        # loop even runs -- no need to special-case the empty subset.
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int) -> None:
            # Every call represents a valid subset the instant it starts,
            # so record it immediately -- no condition needed.
            result.append(path[:])

            for idx in range(start, len(nums)):
                # Choose: add nums[idx] to the current path
                path.append(nums[idx])

                # Explore: recurse forward only (start = idx + 1) so each
                # element is only picked once per branch, and order never
                # repeats in reverse (no [1,2] AND [2,1])
                backtrack(idx + 1)

                # Un-choose: backtrack by removing the last element
                path.pop()

        backtrack(0)
        return result


def main() -> None:
    sol = Solution()
    nums = [1, 2, 3]
    print(sol.subsets(nums))


if __name__ == "__main__":
    main()