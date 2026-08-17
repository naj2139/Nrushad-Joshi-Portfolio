from __future__ import annotations

from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        # Uses the `idx` (start-index) technique: recursing with idx + 1
        # instead of idx moves strictly forward through candidates, so no
        # index is ever revisited in the same branch. This avoids both
        # reuse (no [1,1,1,...]) and reordered duplicates (no [2,4] AND
        # [4,2] both appearing) in a single pass.
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int, path: List[int]) -> None:
            # Base case: remaining hits 0 exactly, current path sums to target
            if remaining == 0:
                result.append(path[:])
                return

            for idx in range(start, len(candidates)):
                # Prune: picking this candidate would overshoot target
                if remaining - candidates[idx] < 0:
                    continue

                # Choose: add candidates[idx] to the current path
                path.append(candidates[idx])

                # Explore: recurse with idx + 1 (not idx) so this index is
                # never picked again in this branch -- no reuse, no
                # reordered duplicates
                backtrack(idx + 1, remaining - candidates[idx], path)

                # Un-choose: backtrack by removing the last element
                path.pop()

        backtrack(0, target, path)
        return result


def main() -> None:
    sol = Solution()
    candidates = [2, 3, 6, 7, 5, 1, 4, 8, 9, 10]
    target = 10
    print(sol.combinationSum(candidates, target))


if __name__ == "__main__":
    main()