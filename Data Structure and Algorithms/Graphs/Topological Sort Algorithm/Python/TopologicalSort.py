"""
Topological Sort (Kahn's Algorithm — layer-by-layer variant)

Models a course-prerequisite DAG and returns a valid course order such
that every prerequisite appears before the course that depends on it.
"""

# Pseudo Code
# 1. Find all nodes with indegree 0, i.e., vertices with no incoming edges
# Indegree = the number of incoming edges (arrows pointing into) a node.
# 2. Remove each such node from the graph and decrease the indegree of its adjacent vertices by 1
# 3. If any adjacent vertex's indegree becomes 0, add it to the queue/list of nodes to process
# 4. Repeat steps 1–3 until every node has been processed (indegree reduced to 0)
# 5. The order in which nodes were removed (added to the result) is the topologically sorted order

from typing import List, Tuple, Dict


def topological_sort(vertex: List[str], edges: List[Tuple[str, str]]) -> List[str]:
    """
    Returns a topologically sorted list of vertices.

    Args:
        vertex: list of node names (e.g., course codes)
        edges: list of (prereq, course) pairs, meaning prereq -> course

    Returns:
        A list of vertices in valid topological order.
    """
    # graph = {}
    # for course in vertex
    #   graph[course] = [[], 0]
    graph = {course: [[], 0] for course in vertex}

    for prereq, course in edges:
        graph[prereq][0].append(course)   # record that prereq unlocks course
        graph[course][1] += 1             # course has one more prerequisite now

    order = []

    while vertex:
        ready_courses = []  # courses found to have indegree 0 in this pass

        for course_name, course_data in graph.items():
            course = course_name
            neighbors = course_data[0]
            indeg = course_data[1]

            if not indeg:
                ready_courses.append(course)
                for neighbor in neighbors:
                    graph[neighbor][1] -= 1  # remove one prerequisite from each neighbor

        for finished_course in ready_courses:
            vertex.remove(finished_course)
            graph.pop(finished_course)
            order.append(finished_course)

    return order


if __name__ == "__main__":
    courses = [
        "W1004", "W1007",
        "W3134", "W3137", "W3157", "W3203", "W3261",
        "W4111", "W4115", "W4156", "W4701"
    ]

    prereq_edges = [
        ("W1004", "W3134"), ("W1004", "W3203"), ("W1004", "W3157"),
        ("W1007", "W3134"), ("W1007", "W3203"), ("W1007", "W3157"),
        ("W3134", "W3261"), ("W3134", "W4111"), ("W3134", "W4701"),
        ("W3137", "W3261"), ("W3137", "W4111"), ("W3137", "W4701"),
        ("W3261", "W4115"), ("W4115", "W4156"),
    ]

    result = topological_sort(courses, prereq_edges)
    print("Topological order:", result)