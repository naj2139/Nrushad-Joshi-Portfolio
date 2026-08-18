# LeetCode 912: Sort an Array (Merge Sort)
#
# Divide and conquer: split the array in half, recursively sort each half,
# then merge the two sorted halves back together.
# Recurrence: T(n) = 2T(n/2) + O(n)  ->  O(n log n)  (Master theorem)

from typing import List


class Solution:
    def merge(self, left: List[int], right: List[int]) -> List[int]:
        # left and right are already sorted (from the recursive calls
        # below). In a sorted list, the smallest REMAINING element is
        # always whatever the pointer (l or r) currently points to --
        # everything before it has already been taken, everything after
        # it is guaranteed to be >= it. So the smallest value across both
        # lists has to be one of the two front elements -- nothing else
        # is even a candidate, which is why only l and r ever get compared.
        out = []
        leftLen = len(left)
        rightLen = len(right)
        l, r = 0, 0

        while l < leftLen and r < rightLen:
            if left[l] < right[r]:
                out.append(left[l])
                l += 1
            else:
                out.append(right[r])
                r += 1

        # One list may still have leftover elements once the other runs
        # out. left[l:] / right[r:] on an exhausted list just gives [],
        # and looping over [] does nothing -- so no "if left:" / "if right:"
        # guard is needed before these; they're already safe no-ops.
        for val in left[l:]:
            out.append(val)
        for val in right[r:]:
            out.append(val)

        return out

    def sortArray(self, nums: List[int]) -> List[int]:
        # Base case: length 0 or 1 is already sorted. Both must return
        # an actual list -- returning bare `return` (i.e. None) for the
        # empty case breaks merge() the moment it calls len(None), and
        # also means half = len(nums)//2 never changes on [], causing
        # infinite recursion instead of a clean stop.
        if len(nums) == 0:
            return []
        if len(nums) == 1:
            return nums

        half = len(nums) // 2
        left = self.sortArray(nums[:half])
        right = self.sortArray(nums[half:])

        return self.merge(left, right)


if __name__ == "__main__":
    nums = [4, 2, 1, 3]

    sol = Solution()
    result = sol.sortArray(nums)

    print(result)