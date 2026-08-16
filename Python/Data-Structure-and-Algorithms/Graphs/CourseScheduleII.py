from __future__ import annotations


class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        """Return a valid course order, or an empty list if impossible.

        Args:
            numCourses: Total number of courses, labeled 0 to
                numCourses - 1.
            prerequisites: List of [a, b] pairs meaning course b must
                be taken before course a.

        Returns:
            A list giving one valid order to complete all courses, or
            an empty list if no valid order exists (i.e. the
            prerequisite graph has a cycle).
        """
        
        visited = set()
        path = []

        


def main() -> None:
    sol = Solution()

    print(sol.findOrder(2, [[1, 0]]))
    # Expected: [0, 1] (or any valid order -- 0 must come before 1)

    print(sol.findOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))
    # Expected: some order where 0 is before 1 and 2, and both 1 and 2
    # are before 3, e.g. [0, 1, 2, 3] or [0, 2, 1, 3]

    print(sol.findOrder(1, []))
    # Expected: [0]

    print(sol.findOrder(2, [[1, 0], [0, 1]]))
    # Expected: []
    # (a cycle -- no valid order exists)

    print(sol.findOrder(3, [[1, 0], [2, 1]]))
    # Expected: [0, 1, 2]


if __name__ == "__main__":
    main()