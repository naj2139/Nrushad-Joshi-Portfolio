from __future__ import annotations


class Solution:
    def partition(self, s: str) -> list[list[str]]:
        """Return all ways to split s into substrings that are all palindromes.

        Args:
            s: Input string to partition.

        Returns:
            A list of partitions, where each partition is a list of
            palindromic substrings whose concatenation equals s.
        """

        def isPalindrome(piece: str) -> bool:
            # A string is a palindrome if it reads the same forwards and
            # backwards -- direct comparison against its own reverse,
            # no stack or auxiliary structure needed.
            return piece == piece[::-1]

        path, res = [], []

        def backtrack(start: int) -> None:
            # Done: the whole string has been consumed, so whatever pieces
            # are currently in path form one complete, valid partition.
            # This is a position-based finish line, not based on any
            # property of path's length or contents.
            if start == len(s):
                res.append(path[:])
                return

            # The decision at every step is "how long is the NEXT piece?" --
            # not "include this character or not." Try every possible
            # end-point idx for the next piece, starting right after the
            # previous one left off.
            for idx in range(start, len(s)):
                piece = s[start:idx + 1]

                # Only continue down this branch if the candidate piece is
                # itself a palindrome. An invalid piece is a dead end --
                # nothing later in the string can retroactively fix it.
                if isPalindrome(piece):
                    path.append(piece)      # commit to this piece
                    backtrack(idx + 1)      # recurse on the remainder
                    path.pop()              # undo, try the next length

        backtrack(0)
        return res


def main() -> None:
    sol = Solution()

    print(sol.partition("aab"))
    # Expected: [["a","a","b"],["aa","b"]]

    print(sol.partition("a"))
    # Expected: [["a"]]

    print(sol.partition("aba"))
    # Expected: [["a","b","a"],["aba"]]

    print(sol.partition("abc"))
    # Expected: [["a","b","c"]]

    print(sol.partition(""))
    # Expected: [[]]

if __name__ == "__main__":
    main()