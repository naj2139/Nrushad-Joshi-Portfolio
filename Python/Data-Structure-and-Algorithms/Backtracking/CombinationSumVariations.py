from __future__ import annotations

from typing import List


class Solution:
    def combinationSumWithRepetition(self, candidates: List[int], target: int) -> List[List[int]]:
        # NOTE: no `start` index and no `if val in path` check, so the same
        # value can be picked again on the very next call -- this allows
        # unlimited reuse of each candidate within a combination
        # (e.g. [1,1,1,1,1,1] is valid if target permits it).
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(path) -> None:
            # Prune: running sum already exceeds target, dead end
            if sum(path) > target:
                return
            # Base case: running sum hits target exactly, record it
            if sum(path) == target:
                result.append(path[:])
                return

            for val in candidates:
                # Choose: add val to the current path
                path.append(val)

                # Explore: recurse with the same candidate list (no start
                # index), so val itself remains eligible again next call
                backtrack(path)

                # Un-choose: backtrack by removing the last element
                path.pop()

        backtrack(path)
        return result

    def combinationSumNoRepetition(self, candidates: List[int], target: int) -> List[List[int]]:
        # NOTE: `if val in path` only blocks reusing the same value within
        # a combination -- it does NOT prevent reordered duplicates in the
        # result (e.g. [2,4] and [4,2] can both appear). Avoiding that
        # requires a `start` index to move forward only, which this
        # version intentionally does not use.
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(path) -> None:
            # Prune: running sum already exceeds target, dead end
            if sum(path) > target:
                return
            # Base case: running sum hits target exactly, record it
            if sum(path) == target:
                result.append(path[:])
                return

            for val in candidates:
                # Skip: val already used somewhere in the current path
                if val in path:
                    continue

                # Choose: add val to the current path
                path.append(val)

                # Explore: recurse over the same candidate list
                backtrack(path)

                # Un-choose: backtrack by removing the last element
                path.pop()

        backtrack(path)
        return result


def main() -> None:
    sol = Solution()
    candidates = [2, 3, 6, 7, 5, 1, 4]
    target = 6

    print("With repetition:", sol.combinationSumWithRepetition(candidates, target))
    print("No repetition:", sol.combinationSumNoRepetition(candidates, target))


if __name__ == "__main__":
    main()