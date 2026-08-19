from typing import List
from random import randint


class Solution:
    def sort(self, nums: List[int]):
        # Always picking the LAST element as the pivot works fine on
        # random data, but on already-sorted (or reverse-sorted) input,
        # the largest (or smallest) element is always at the end -- so
        # every partition puts ALL other elements on one side and NONE
        # on the other. Instead of splitting the problem roughly in
        # half each call, it only shrinks by ONE element per call. That
        # turns O(n log n) into O(n^2), and on a large sorted input it's
        # bad enough to blow Python's recursion limit entirely, since
        # you get n levels of recursion instead of log(n).
        #
        # pivot = nums.pop()

        # Picking a RANDOM index as the pivot instead breaks that
        # pattern. It doesn't make O(n^2) impossible -- an unlucky
        # sequence of random picks can still produce it -- but it makes
        # the bad case a statistical fluke instead of something
        # guaranteed by common, everyday inputs like sorted data. In
        # practice this is enough to make Quicksort reliably fast.
        idx = randint(0, len(nums) - 1)
        pivot = nums.pop(idx)   # remove pivot from nums entirely so the
                                 # scan below only touches the OTHER elements

        i, j = 0, 0
        while j < len(nums):
            if nums[j] < pivot:
                tmp = nums[i]
                nums[i] = nums[j]
                nums[j] = tmp
                i += 1
            j += 1

        nums.insert(i, pivot)  # pivot's final sorted position
        return nums[:i], [nums[i]], nums[i + 1:]

    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums

        left, pivot, right = self.sort(nums)
        left = self.sortArray(left)
        right = self.sortArray(right)

        return left + pivot + right


if __name__ == "__main__":
    nums = [4, 2, 1, -1, 8, 5, 13, 3]

    sol = Solution()
    result = sol.sortArray(nums)

    print(result)