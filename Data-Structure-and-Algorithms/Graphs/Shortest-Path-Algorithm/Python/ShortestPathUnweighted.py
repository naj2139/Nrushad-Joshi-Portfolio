"""
Unweighted Shortest Path (BFS)

Given a graph where every edge has equal "weight" (e.g., one flight = one hop),
finds the minimum number of hops from a starting node to every other node,
and reconstructs the actual shortest path to each node.

Real-world example: minimum layovers between airports.
"""

# Pseudo Code — Unweighted Shortest Path (BFS)
# 1. Choose a starting airport S (e.g., "JFK") and set its distance to 0
# 2. Create a queue and add S to it; mark S as known/visited
# 3. While the queue is not empty:
#      a. Dequeue the current airport (currAirport)
#      b. Look at all of currAirport's direct flight routes (adjacent vertices)
#      c. For each connected airport not yet visited, set its distance to currDistance + 1
#      d. Mark that airport as known/visited and enqueue it
# 4. Repeat step 3 until every reachable airport has been processed
# 5. Each airport's final recorded distance is the minimum number of layovers from S

from typing import List, Tuple
from collections import deque


def shortest_path(vertices: List[str], edges: List[Tuple[str, str]], start: str):
    """
    Runs BFS from `start` and returns:
      - distance: dict mapping each airport -> minimum number of hops from start
      - parent:   dict mapping each airport -> the airport it was reached from
                  (used later to reconstruct the actual path)
    """
    queue = deque([])

    # graph[airport]   -> list of directly connected airports
    # distance[airport] -> minimum hops from start (None = not yet reached)
    # parent[airport]   -> the airport we came from when we first reached this one
    #
    # NOTE: these must be created as separate dict literals.
    # Writing `graph, distance, parent = {}, {}, {}` creates three distinct
    # dictionaries. Writing `graph = distance = parent = {}` would instead
    # make all three names point to the SAME dictionary, so writing to one
    # would silently overwrite the others.
    graph, distance, parent = {}, {}, {}

    # visited must be a set(), not {} (which creates an empty dict) and not
    # a list. A set gives O(1) membership checks ("is this already visited?"),
    # which matters since this check runs once per edge traversed. A list
    # would require scanning every element each time, getting slower as it grows.
    visited = set()

    # Initialize every airport with an empty neighbor list and unknown distance
    for airport in vertices:
        graph[airport] = []
        distance[airport] = None

    # Build the adjacency list in BOTH directions, since flight routes are
    # undirected (a connection A-B means you can fly A->B and B->A).
    # Only adding graph[airport_a].append(airport_b) would make this a
    # directed graph, which breaks BFS starting from any airport that only
    # ever appears as the second element of an edge pair.
    for airport_a, airport_b in edges:
        graph[airport_a].append(airport_b)
        graph[airport_b].append(airport_a)

    distance[start] = 0      # the start is 0 hops from itself
    visited.add(start)       # mark start as visited so it's never re-processed
    queue.append(start)      # seed the queue with the start node
    # note: `start` is intentionally never given an entry in `parent` --
    # it has no predecessor, and this absence is what lets the path-building
    # loop below know when to stop walking backward.

    while queue:
        curr_airport = queue.popleft()          # process one airport at a time
        curr_dist = distance[curr_airport]        # its known shortest distance

        for neighbor in graph[curr_airport]:
            # Only process a neighbor the FIRST time it's discovered.
            # BFS explores level-by-level, so the first time a node is
            # reached is guaranteed to be via the shortest possible path --
            # later discoveries of the same node would only be equal or
            # longer, so they must be ignored rather than overwriting
            # distance/parent.
            if neighbor not in visited:
                parent[neighbor] = curr_airport       # record how we got here
                visited.add(neighbor)                 # mark visited immediately
                queue.append(neighbor)                # queue it for processing
                distance[neighbor] = curr_dist + 1    # one hop farther than curr

    return distance, parent


if __name__ == "__main__":

    # Airports (vertices)
    airports = ["JFK", "LAX", "ORD", "ATL", "DFW", "SEA", "MIA", "DEN", "BOS", "SFO"]

    # Undirected edges (direct flight routes) — connections work both ways
    airport_edges = [
        ("JFK", "ORD"),
        ("JFK", "ATL"),
        ("JFK", "BOS"),
        ("ORD", "DEN"),
        ("ORD", "DFW"),
        ("ATL", "MIA"),
        ("ATL", "DFW"),
        ("DFW", "LAX"),
        ("DEN", "SEA"),
        ("DEN", "LAX"),
        ("LAX", "SFO"),
        ("SEA", "SFO"),
        ("MIA", "DFW"),
    ]

    start = "DEN"
    distance, parent = shortest_path(airports, airport_edges, start)

    # Reconstruct and print the shortest path from `start` to every airport.
    for airport in airports:
        path = [airport]  # begin the path with the destination itself

        # Walk backward through `parent` one step at a time: path[-1] is
        # "where we currently are" in the backward walk. As long as that
        # airport has a recorded predecessor, keep stepping back toward
        # the start. The loop stops naturally once path[-1] is `start`,
        # since `start` was never given an entry in `parent`.
        while path[-1] in parent:
            path.append(parent[path[-1]])

        # The walk above builds the path destination -> start, so reverse
        # it to get the natural travel order: start -> destination.
        path.reverse()

        print(f"{airport}: {' -> '.join(path)}")