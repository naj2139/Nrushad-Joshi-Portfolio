"""
LeetCode 797 - All Paths From Source to Target
"""

from typing import List


# =============================================================================
# My First Attempt
# =============================================================================
# class Solution:
#     def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
#         adjList = {}
#         for idx, val in enumerate(graph):
#             if idx not in adjList:      # dead code — this branch sets
#                 adjList[idx] = None     # adjList[idx] = None, but the very
#             adjList[idx] = val          # next line unconditionally
#                                         # overwrites it with `val` regardless,
#                                         # so the `if` never changes the result
#
#         path, res = [0], []
#         dest = len(graph) - 1
#         def backtrack(idx):
#             if path and dest == path[-1]:
#                 res.append(path[:])
#                 return
#             for val in adjList[idx]:
#                 path.append(val)
#                 backtrack(val)
#                 path.pop()
#         backtrack(0)
#         return res
# ---------------------------------------------------------------------------


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        # WHY (diff from first attempt): `graph` is already an adjacency
        # list — graph[i] gives the neighbors of node i directly. Copying it
        # into a separate `adjList` dict cost an extra O(V + E) build pass
        # and doubled the memory for no benefit, since a dict lookup and a
        # list index are both O(1) anyway. Use `graph` directly instead.
        path, res = [0], []
        dest = len(graph) - 1

        def backtrack(idx):
            # WHY: base case — if the last node added to `path` is the
            # target, save a snapshot (path[:], not path itself, since path
            # keeps mutating) and stop exploring further from here.
            if path and dest == path[-1]:
                res.append(path[:])
                return

            # WHY: this is a DAG per problem constraints (no cycles), so no
            # `visited` set is needed here — every neighbor is safe to
            # explore without risk of infinite recursion.
            for val in graph[idx]:
                path.append(val)   # choose: add the neighbor to the path
                backtrack(val)     # explore: recurse deeper along this branch
                path.pop()         # un-choose: backtrack — remove it before
                                    # trying the next neighbor, so `path`
                                    # accurately reflects only the current
                                    # branch being explored at any moment

        backtrack(0)
        return res

if __name__ == "__main__":
    sol = Solution()
    print(sol.allPathsSourceTarget([[1, 2], [3], [3], []]))
    # [[0, 1, 3], [0, 2, 3]]

    print(sol.allPathsSourceTarget([[4, 3, 1], [3, 2, 4], [3], [4], []]))
    # [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]

    print(sol.allPathsSourceTarget([[1], []]))
    # [[0, 1]]