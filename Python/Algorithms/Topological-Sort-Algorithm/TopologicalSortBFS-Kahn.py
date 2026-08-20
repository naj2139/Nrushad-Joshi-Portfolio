from collections import deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # graph[course] = [list of courses this one unlocks, in-degree count]
        #
        # WHY prereq -> course (not course -> its prereqs):
        # BFS processes courses in the order you'd actually complete them.
        # When a course is popped off the queue, it means "just finished."
        # The next question is always "what does finishing THIS unlock?" -
        # that's an O(1) lookup only if the graph already points forward,
        # from prereq to the courses depending on it. The reverse mapping
        # (course -> its prereqs) is how you'd naturally read the input,
        # but it would force an O(V) scan over every course to find who
        # depends on the one you just finished - O(V^2) instead of O(V+E).
        graph = {course: [[], 0] for course in range(numCourses)}

        for course, prereq in prerequisites:
            graph[prereq][0].append(course)   # prereq unlocks course
            graph[course][1] += 1             # course has one more prereq now

        queue = deque()
        for course in graph:
            if not graph[course][1]:
                queue.append(course)

        order = []
        while queue:
            node = queue.popleft()
            order.append(node)

            # WHY no explicit "visited" set / removal here (unlike DFS):
            # the in-degree counter itself guarantees each node is queued
            # exactly once. In-degree only ever decreases, and a node is
            # only enqueued the instant it crosses to exactly 0. Since
            # each edge fires its decrement exactly once (when its source
            # node is popped), a node can't cross 0 a second time - so
            # there's nothing to "unmark" or protect against re-adding.
            # DFS needs an explicit visited/recursion-stack set instead,
            # because it re-enters neighbors directly via recursion and
            # has no counter tracking how many times a node's been reached.
            for neighbor in graph[node][0]:
                graph[neighbor][1] -= 1
                if graph[neighbor][1] == 0:
                    queue.append(neighbor)

        # WHY this check is required:
        # if a cycle exists, the courses inside it never reach in-degree 0,
        # so they never get queued and never make it into `order`. Without
        # this length check, the function would silently return a partial,
        # invalid ordering instead of signaling "impossible."
        return order if len(order) == numCourses else []


if __name__ == "__main__":
    sol = Solution()

    print(sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
    # expect a valid order, e.g. [0, 1, 2, 3] or [0, 2, 1, 3]

    print(sol.findOrder(2, [[1, 0], [0, 1]]))
    # expect [] - cycle between 0 and 1

    print(sol.findOrder(3, [[0, 1], [1, 2]]))
    # expect [2, 1, 0]