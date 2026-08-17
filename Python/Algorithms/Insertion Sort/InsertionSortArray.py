# LeetCode 912: Sort an Array (practicing with Insertion Sort)
#
# Note: insertion sort is O(n^2), so this won't pass LeetCode's judge at full
# scale (n up to 5*10^4) -- use this as local practice for the shifting logic.

from typing import List


class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        i = 1
        while i < len(nums):
            # Only trigger a shift if the current element is smaller than
            # the one before it. If nums[i-1] <= nums[i], the sorted prefix
            # nums[0:i] is already <= nums[i] (since it's sorted ascending),
            # so nums[i] is already in the correct spot -- no work needed.
            if nums[i - 1] > nums[i]:
                # Pull the out-of-order element out of the list so we can
                # walk the sorted prefix and find where it belongs.
                curr = nums.pop(i)
                j = 0
                # Walk the sorted prefix nums[0:i] looking for the first
                # element bigger than curr -- that's where curr gets
                # inserted, shifting everything from j onward one spot right.
                while j < i:
                    if nums[j] > curr:
                        # --- First attempt (works, but rebuilds the list) ---
                        # Slicing + concatenation creates two brand-new list
                        # objects every single insertion (nums[:j] copies the
                        # left half, nums[j:] copies the right half, and '+'
                        # allocates a third list to hold the combined result).
                        # That's O(n) extra allocation on top of the O(n)
                        # shift that insertion sort already requires -- so
                        # this version does roughly double the work.
                        #
                        # nums = nums[:j] + [curr] + nums[j:]
                        # list.insert(j, curr) does the conceptual shift
                        # in place: every element from index j onward is
                        # moved one slot to the right (still O(n) work,
                        # since that's inherent to array insertion sort),
                        # but there's no new list object created and no
                        # copying of the unaffected left portion (nums[:j]).
                        # Same result, less memory churn.
                        nums.insert(j, curr)
                        break
                    j += 1
            i += 1
        return nums


if __name__ == "__main__":
    nums = [4, 2, 1, 3]

    sol = Solution()
    result = sol.sortArray(nums)

    print(result)