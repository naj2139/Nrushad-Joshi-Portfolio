from __future__ import annotations

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        """Return whether all courses can be finished given prerequisites.

        Args:
            numCourses: Total number of courses, labeled 0 to
                numCourses - 1.
            prerequisites: List of [a, b] pairs meaning course b must
                be taken before course a.

        Returns:
            True if there is a valid order to complete all courses
            (i.e. the prerequisite graph has no cycle), False
            otherwise.
        """
        # `visited` is PERMANENT: once a course is fully explored and
        # found safe, it never needs re-exploring, even when reached
        # again from a different starting point.
        visited: set[int] = set()
        currPath: list[int] = []

        def traversal(start: int, visited: set[int], path: list[int]) -> bool:
            visited.add(start)
            path.append(start)

            for edge in prerequisites:
                if edge[1] == start:
                    # edge[0] still on the CURRENT active path means
                    # we've walked back into something we're still in
                    # the middle of exploring -- that's a cycle.
                    if edge[0] in path:
                        return False

                    # edge[0] already fully explored (safe) via some
                    # earlier, unrelated path -- no need to redo work.
                    # This is normal in a DAG (e.g. a diamond
                    # dependency), not a cycle.
                    if edge[0] in visited:
                        continue

                    if not traversal(edge[0], visited, path):
                        return False

            # Backtrack: this course is no longer on the ACTIVE path,
            # even though it stays in `visited` permanently.
            path.pop()
            return True

        # A single starting point can only discover the piece of the
        # graph connected to it. Looping over every course and only
        # starting a fresh traversal from unvisited ones ensures
        # disconnected components (and any cycles hiding in them) are
        # never silently skipped.
        for edge in prerequisites:
            if edge[1] not in visited:
                if not traversal(edge[1], visited, currPath):
                    return False
        return True


def main() -> None:
    sol = Solution()

    print(sol.canFinish(2, [[1, 0]]))
    # Expected: True
    # (take course 0, then course 1)

    print(sol.canFinish(2, [[1, 0], [0, 1]]))
    # Expected: False
    # (course 1 needs 0, course 0 needs 1 -- a cycle)

    print(sol.canFinish(3, [[1, 0], [2, 1]]))
    # Expected: True
    # (0 -> 1 -> 2, a straight chain)

    print(sol.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
    # Expected: True

    print(sol.canFinish(1, []))
    # Expected: True
    # (a single course with no prerequisites)

    print(sol.canFinish(4, [[0, 1], [2, 3], [3, 2]]))
    # Expected: False
    # (courses 2 and 3 form a cycle, disconnected from courses 0/1 --
    # this is the case that breaks a single-starting-point traversal)

    print(sol.canFinish(4, [[1, 0], [3, 2]]))
    # Expected: True
    # (two separate, disconnected chains, no cycle in either)


if __name__ == "__main__":
    main()