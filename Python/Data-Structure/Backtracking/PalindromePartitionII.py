"""Palindrome Partitioning II (LeetCode 132) — backtracking / DP.

Given a string s, partition s such that every substring of the
partition is a palindrome.

Return the minimum number of cuts needed for a palindrome
partitioning of s.
"""

from __future__ import annotations

# =============================================================================
# My First Attempt
# =============================================================================
# Works correctly, but relies on a common Python workaround: since a nested
# function can't reassign an outer variable directly (only `nonlocal`
# allows that, and even that still mutates shared state across the whole
# recursion tree), `minVal` is wrapped in a single-element list just so
# `backtrak` can mutate it in place. It gets the job done, but it's a
# side-effecting design -- see the Final Version below for a cleaner,
# purely functional alternative.
#
# class Solution:
#     def minCut(self, s: str) -> int:
#         def isPalindrome(string):
#             left, right = 0, len(string) - 1
#             while left < right:
#                 if string[left] != string[right]:
#                     return False
#                 left += 1
#                 right -= 1
#             return True
#
#         path = []
#         minVal = [len(s) - 1]
#
#         def backtrak(start, tracker):
#             # tracker counts PIECES committed so far, not cuts -- cuts is
#             # always one less than piece count (3 pieces = 2 cuts). That's
#             # why the base case returns tracker - 1 rather than tracker.
#             if start == len(s):
#                 return tracker - 1
#             for idx in range(start, len(s)):
#                 piece = s[start:idx + 1]
#                 if isPalindrome(piece):
#                     path.append([piece])
#                     val = backtrak(idx + 1, tracker + 1)
#                     if val is not None and val < minVal[0]:
#                         minVal[0] = val
#                     path.pop()
#
#         backtrak(0, 0)
#         return minVal[0]


# =============================================================================
# Final Version
# =============================================================================


class Solution:
    def minCut(self, s: str) -> int:
        """Return the minimum number of cuts to partition s into palindromes.

        Args:
            s: Input string to partition.

        Returns:
            The minimum number of cuts needed so that every resulting
            substring is a palindrome. A string that is already a
            palindrome requires 0 cuts.
        """

        def isPalindrome(piece: str) -> bool:
            return piece == piece[::-1]

        def backtrack(start: int) -> int:
            # Base case: nothing left to cut, so this branch contributes
            # zero additional pieces. Returning -1 (not 0) is deliberate --
            # it's what makes "1 + backtrack(...)" below work out correctly.
            # A single piece stretching to the end computes as
            # 1 + (-1) = 0 cuts, matching the fact that one whole-string
            # palindrome needs no cuts at all.
            if start == len(s):
                return -1

            best = float("inf")
            for idx in range(start, len(s)):
                piece = s[start:idx + 1]
                if isPalindrome(piece):
                    # 1 cut for committing to `piece`, plus however many
                    # cuts the remainder needs. No external state is
                    # mutated -- each call simply returns its own answer,
                    # and the caller combines results with min().
                    best = min(best, 1 + backtrack(idx + 1))
            return best

        return backtrack(0)


def main() -> None:
    sol = Solution()

    print(sol.minCut("aab"))
    # Expected: 1
    # ("aa" | "b")

    print(sol.minCut("a"))
    # Expected: 0

    print(sol.minCut("ab"))
    # Expected: 1
    # ("a" | "b")

    print(sol.minCut("aba"))
    # Expected: 0
    # ("aba" is already a palindrome)

    print(sol.minCut("abcde"))
    # Expected: 4
    # ("a" | "b" | "c" | "d" | "e")

if __name__ == "__main__":
    main()