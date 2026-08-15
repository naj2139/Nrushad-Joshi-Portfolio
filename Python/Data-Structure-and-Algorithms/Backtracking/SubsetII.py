from __future__ import annotations


class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        # =============================================================================
        # My First Attempt
        # =============================================================================
        # def backtrack(start) -> None:
        #     result.append(path[:])
        #     idx = start
        #     while idx < len(nums):
        #         path.append(nums[idx])
        #         backtrack(idx + 1)
        #         path.pop()
        #
        #         tmp = idx + 1
        #         while tmp < len(nums) and nums[idx] == nums[tmp]:
        #             idx = tmp
        #             tmp += 1
        #
        #         idx += 1
        #
        # backtrack(0)
        # return result

        result: list[list[int]] = []
        path: list[int] = []
        nums = sorted(nums)  # duplicates must be adjacent for the skip logic to work

        def backtrack(start: int) -> None:
            # Every call represents a valid subset the instant it starts,
            # so record it immediately -- no condition needed.
            result.append(path[:])

            idx = start
            while idx < len(nums):
                # Choose: add nums[idx] to the current path
                path.append(nums[idx])

                # Explore: recurse forward only (idx + 1) so each
                # element is only picked once per branch
                backtrack(idx + 1)

                # Un-choose: backtrack by removing the last element
                path.pop()

                idx += 1
                # Skip duplicate values at this same depth -- we just
                # finished exploring every subset that includes nums[idx - 1]
                # here, so branching on an identical value again would
                # regenerate the same subsets. This only compares adjacent
                # picks at one level; it never looks into a deeper call's
                # own loop.
                while idx < len(nums) and nums[idx] == nums[idx - 1]:
                    idx += 1

        backtrack(0)
        return result


def main() -> None:
    sol = Solution()

    nums1 = [1, 2, 2]
    print(sol.subsetsWithDup(nums1))
    # Expected: [[], [1], [1,2], [1,2,2], [2], [2,2]]

    nums2 = [0]
    print(sol.subsetsWithDup(nums2))
    # Expected: [[], [0]]

    nums3 = [1, 2, 3]
    print(sol.subsetsWithDup(nums3))
    # Expected: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]


if __name__ == "__main__":
    main()