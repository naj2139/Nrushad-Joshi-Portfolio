# LeetCode 215: Kth Largest Element in an Array (Quickselect)
#
# Same partition step as Quicksort -- pick a pivot, rearrange so smaller
# elements land left and larger elements land right, pivot ends up in its
# final sorted position. The difference: only recurse into the ONE side
# that contains the answer, instead of both. That's what drops the
# average time from O(n log n) down to O(n).

from typing import List
import random


class Solution:
    def sort(self, nums: List[int], k: int):
        idx = random.randint(0, len(nums) - 1)
        pivot = nums.pop(idx)   # remove pivot so the scan only touches
                                  # the other elements
        i, j = 0, 0
        while j < len(nums):
            if nums[j] <= pivot:
                tmp = nums[i]
                nums[i] = nums[j]
                nums[j] = tmp
                i += 1
            j += 1
        nums.insert(i, pivot)   # i is the pivot's REAL final sorted index

        # --- Debugging history ---
        # Attempt 1: compared against `idx` (where the pivot started,
        # before partitioning) instead of `i` (where it actually landed
        # after partitioning). idx is essentially a random, meaningless
        # number here -- it tells you nothing about the pivot's final
        # position, so almost every comparison against it was wrong.
        #
        # Attempt 2: fixed idx -> i, but applied the same k-adjustment
        # formula to ALL three branches unconditionally. That broke the
        # right-partition case, producing a negative k (and downstream
        # "list index out of range" errors), because the adjustment was
        # only ever valid for the left branch -- see reasoning below.

        # RIGHT partition (nums[i+1:]) contains only elements greater
        # than the pivot -- the "top" of the array. Nothing bigger than
        # what's in this subarray got removed, so "kth largest" still
        # means the same thing here. k stays unchanged.
        if len(nums) - k > i:
            return nums[i + 1:], k

        # LEFT partition (nums[:i]) contains only elements smaller than
        # the pivot. But len(nums) - i elements (the pivot + everything
        # in the right partition, all BIGGER than this subarray) just
        # got excluded. If you were looking for, say, the 7th largest
        # overall and 4 elements bigger than this subarray are gone,
        # you're now looking for the 3rd largest WITHIN this subarray
        # (7 - 4) -- those 4 already "used up" their rank from the top.
        elif len(nums) - k < i:
            k -= len(nums) - i
            return nums[:i], k

        # len(nums) - k == i means the pivot itself sits exactly at the
        # target position -- it IS the answer.
        else:
            return [nums[i]], k

    def findKthLargest(self, nums: List[int], k: int) -> int:
        if len(nums) <= 1:
            return nums[0]
        tmp, k = self.sort(nums, k)
        return self.findKthLargest(tmp, k)


if __name__ == "__main__":
    nums = [3, 2, 1, 5, 6, 4]
    k = 2

    sol = Solution()
    result = sol.findKthLargest(nums, k)

    print(result)