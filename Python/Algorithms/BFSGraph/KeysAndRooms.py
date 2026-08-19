from collections import deque
from typing import List

# ---------------------------------------------------------------------------
# FIRST ATTEMPT 
# ---------------------------------------------------------------------------
# class Solution:
#     def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
#         adjList = {}
#         for idx, val in enumerate(rooms):
#             adjList[idx] = val
#
#         visited = set()
#         queue = deque([0])
#
#         while queue:
#             node = queue.popleft()
#             if node not in visited:
#                 visited.add(node)              # marked visited on POP, not enqueue
#                 for edge in adjList[node]:
#                     if edge not in visited:
#                         queue.append(edge)      # no visited.add here — a node can
#                                                  # be enqueued by several different
#                                                  # neighbors before it's ever popped
#         if len(visited) == len(rooms):
#             return True
#         return False
# ---------------------------------------------------------------------------


class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        # rooms[i] is already an adjacency list (keys found in room i),
        # so no separate build step is needed beyond indexing by room number.
        adjList = {}
        for idx, val in enumerate(rooms):
            adjList[idx] = val

        # WHY (diff from first attempt): mark room 0 visited immediately,
        # since it's the BFS seed and never goes through the "discover a
        # neighbor" path where visited-marking normally happens.
        visited = {0}
        queue = deque([0])

        while queue:
            node = queue.popleft()
            # WHY (diff from first attempt): no "if node not in visited"
            # guard here. Once visited-marking happens at enqueue time
            # (below), every node popped off the queue is already guaranteed
            # to be in `visited` — so a guard checking that on pop would just
            # block the neighbor-exploration loop from ever running past the
            # first node. (This was tried and reproduced exactly that bug —
            # only room 0's direct neighbors got explored.)
            for edge in adjList[node]:
                if edge not in visited:
                    visited.add(edge)   # WHY: mark visited AT enqueue time,
                    queue.append(edge)  # not pop time — prevents a node from
                                         # being pushed onto the queue more
                                         # than once by different neighbors.

        return len(visited) == len(rooms)

if __name__ == "__main__":
    sol = Solution()
    print(sol.canVisitAllRooms([[1], [2], [3], []]))            # True
    print(sol.canVisitAllRooms([[1, 3], [3, 0, 1], [2], [0]]))   # False
    print(sol.canVisitAllRooms([[]]))                            # True (single room, no keys needed)