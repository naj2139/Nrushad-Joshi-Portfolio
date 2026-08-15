from __future__ import annotations

from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # Sort first: duplicate values must sit next to each other for the
        # "jump past duplicates" logic below to work -- it only ever
        # compares a candidate to its immediate neighbor.
        candidates.sort()
        result: List[List[int]] = []
        path: List[int] = []

        def backtrack(start: int, remaining: int, path: List[int]) -> None:
            # Base case: remaining hits 0 exactly, current path sums to target
            if remaining == 0:
                result.append(path[:])
                return

            idx = start
            while idx < len(candidates):
                # Prune: since candidates is sorted, once one value
                # overshoots remaining, every value after it (larger) will
                # overshoot too -- stop this loop entirely, don't just skip
                if remaining - candidates[idx] < 0:
                    break

                # Choose: add candidates[idx] to the current path
                path.append(candidates[idx])

                # Explore: recurse with idx + 1 (not idx), so this exact
                # array position can never be picked again in this branch
                # -- this is what prevents REUSE of a single element.
                backtrack(idx + 1, remaining - candidates[idx], path)

                # Un-choose: backtrack by removing the last element
                path.pop()

                # ---- Duplicate-VALUE handling (what makes this "II") ----
                # KEY IDEA: this jump only ever fires within ONE loop, at
                # ONE depth -- comparing two ADJACENT iterations of THIS
                # SAME while loop that would otherwise pick the same value
                # as two separate, redundant branches.
                #
                # It never reaches into a deeper recursive call's own loop
                # (different start, different scope) -- so combinations
                # built by going DEEPER with a repeated value, like
                # [1,1,1] or [1,2,2], are completely unaffected. Only
                # picking the SAME value again as a fresh branch at the
                # SAME level (which would just re-derive what the previous
                # iteration already fully explored) gets skipped.
                #
                # Uses a plain while-loop counter (not for-idx-in-range)
                # because reassigning a for-range loop variable mid-loop
                # does not change what that loop does next in Python.
                
                idx += 1
                while idx < len(candidates) and candidates[idx] == candidates[idx - 1]:
                    idx += 1

        backtrack(0, target, path)
        return result


def main() -> None:
    sol = Solution()
    candidates = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]
    target = 3
    print(sol.combinationSum2(candidates, target))


if __name__ == "__main__":
    main()