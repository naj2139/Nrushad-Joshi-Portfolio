"""
LeetCode 1971 - Find if Path Exists in Graph
"""

from collections import deque
from typing import List

# =============================================================================
# My First Attempt
# =============================================================================
# class Solution:
#     def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
#         adjList = {}
#         for x in edges:
#             if x[0] not in adjList:        # BUG 1: only seeds keys that appear
#                 adjList[x[0]] = []          # in `edges` — an isolated node (no
#             if x[1] not in adjList:         # edges at all) has no key, so
#                 adjList[x[1]] = []          # adjList[node] below would KeyError.
#             adjList[x[0]].append(x[1])
#             adjList[x[1]].append(x[0])
#         queue = deque([source])
#         visited = set()
#         while queue:
#             node = queue.popleft()
#             if node not in visited:        # BUG 3: node not marked visited
#                 if node == destination:    # until AFTER this block — see below
#                     return True
#                 for edge in adjList[node]:
#                     queue.append(edge)     # BUG 2: no check before appending —
#                 visited.add(node)          # every neighbor gets pushed onto the
#         return False                       # queue even if already visited/queued
# ---------------------------------------------------------------------------


class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # Build adjacency list for O(1) neighbor lookups.
        # WHY (fixes BUG 1): pre-seed every index 0..n-1 with an empty list.
        # The first attempt only created keys for nodes that appeared in `edges`
        # (via the `if x[0] not in adjList` checks), so a fully isolated node
        # (0 edges, e.g. n=5 but only 3 nodes ever mentioned in `edges`) would
        # KeyError on adjList[node] the moment it was popped from the queue.
        adjList = {idx: [] for idx in range(n)}
        for u, v in edges:
            adjList[u].append(v)
            adjList[v].append(u)  # undirected graph — add both directions

        # WHY (new): handle source == destination up front. A single node with
        # no traversal at all is trivially "reachable from itself," and the
        # BFS loop below never checks this case on its own.
        if source == destination:
            return True

        queue = deque([source])
        visited = {source}  # WHY: set literal, not set(source) — set(int) crashes
                             # because set() tries to iterate its argument.

        while queue:
            node = queue.popleft()
            # WHY (fixes BUG 3, no "if node not in visited" guard here): the
            # first attempt marked a node visited on POP (`visited.add(node)`
            # at the end of the loop body), which meant the destination check
            # — nested inside `if node not in visited` — only ran the FIRST
            # time a node was popped. That's usually fine on its own, but it
            # also meant a node could sit in the queue multiple times (see
            # BUG 2 below) while still "unvisited," letting duplicate work
            # slip through. Once marking moves to enqueue-time (below), every
            # popped node is guaranteed to already be in `visited`, so this
            # guard becomes unnecessary — removed entirely.
            for edge in adjList[node]:
                # WHY (new): check for destination at discovery time, not pop
                # time. This pairs with the enqueue-time visited marking below
                # — since a popped node is always already "visited," a
                # post-pop destination check would be checking a condition
                # that's already been true for a while; checking at discovery
                # time catches it as early as possible.
                if edge == destination:
                    return True
                if edge not in visited:
                    queue.append(edge)
                    visited.add(edge)
                    # WHY (fixes BUG 2): mark visited AT
                    # enqueue time, not pop time. The first
                    # attempt did `queue.append(edge)` with
                    # no check at all — every neighbor got
                    # pushed onto the queue regardless of
                    # whether it was already visited or
                    # already sitting in the queue,
                    # allowing the same node to be enqueued
                    # many times over.

        return False


if __name__ == "__main__":
    sol = Solution()
    print(sol.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2))   # True
    print(sol.validPath(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5))  # False
    print(sol.validPath(1, [], 0, 0))  # True (isolated node, source == destination)