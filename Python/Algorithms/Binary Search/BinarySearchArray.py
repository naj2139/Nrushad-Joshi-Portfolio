from typing import List


class Solution:
    # =============================================================================
    # My First Attempt
    # =============================================================================
    # Worked correctly, but the two guard clauses below (checking
    # target against nums[0] and nums[-1] before recursing) turned out
    # to be unnecessary -- the base case of `search` already produces
    # the right answer for both boundary conditions on its own. Kept
    # here to show the reasoning process, not because it's wrong.
    #
    # def searchInsert(self, nums: List[int], target: int) -> int:
    #
    #     if nums[0] > target:
    #         return 0
    #
    #     if nums[-1] < target:
    #         return len(nums)
    #
    #     def search(low, high, nums):
    #         if high >= low:
    #             half = (high + low) // 2
    #             print(low, high, half, nums)
    #
    #             if nums[half] == target:
    #                 return half
    #
    #             if nums[half] > target:
    #                 return search(low, half-1, nums)
    #             else:
    #                 return search(half+1, high, nums)
    #
    #         else:
    #             if nums[high] > target:
    #                 return high - 1
    #             if nums[high] < target:
    #                 return high + 1
    #     return search(0, len(nums)-1, nums)

    def searchInsert(self, nums: List[int], target: int) -> int:
        def search(low, high):
            if high >= low:
                half = (high + low) // 2
                if nums[half] == target:
                    return half
                if nums[half] > target:
                    return search(low, half - 1)
                else:
                    return search(half + 1, high)
            else:
                # Base case: the search range has crossed itself
                # (high < low), meaning target isn't in nums. `low`
                # is what we return, and it's not arbitrary -- by this
                # point `low` has been pushed to exactly the index
                # target would need to occupy to keep nums sorted:
                #
                #   - If target is smaller than every remaining
                #     candidate, every branch taken was `search(low, half-1)`.
                #     `low` never moves in that branch, so it stays
                #     pinned at the left edge of the current range --
                #     which converges to the correct insertion index.
                #   - If target is larger than every remaining
                #     candidate, every branch taken was
                #     `search(half+1, high)`. `low` keeps climbing to
                #     `half + 1` each time, and ends up exactly one
                #     past the last element smaller than target.
                #
                # Either way, `low` lands precisely where target
                # belongs -- which is why the two upfront guard
                # clauses in the first attempt were redundant: this
                # base case already handles both edges.
                return low

        return search(0, len(nums) - 1)

if __name__ == "__main__":
    nums = [1, 3, 5, 6]
    target = 5
 
    sol = Solution()
    result = sol.searchInsert(nums, target)
 
    print(result)