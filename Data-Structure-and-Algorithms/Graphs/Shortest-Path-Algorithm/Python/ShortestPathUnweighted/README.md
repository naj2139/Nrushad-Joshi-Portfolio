# Shortest Path Scheduler (Unweighted BFS)

A Python implementation of **Breadth-First Search (BFS)** for unweighted shortest-path computation, modeled around a real-world use case: finding the minimum number of layovers between airports and reconstructing the actual route.

## Problem

Given a set of airports and a list of direct flight routes `(airport_a, airport_b)`, find the minimum number of hops (layovers) from a starting airport to every other airport, and reconstruct the actual sequence of airports for each shortest path.

Since every flight route counts equally as "one hop" (no route is weighted more than another), this is a classic **unweighted shortest path** problem — solvable with BFS rather than a weighted algorithm like Dijkstra's.

## Approach

This implementation uses standard BFS with two supporting dictionaries:

1. Build an adjacency list where every route is added in **both directions**, since flights are undirected (a route A-B means you can fly A→B and B→A).
2. Starting from `start`, set its distance to 0, mark it visited, and enqueue it.
3. While the queue is not empty, dequeue the current airport and look at all its direct neighbors.
4. For each neighbor **not yet visited**: record its distance as `current distance + 1`, record its `parent` (the airport it was reached from), mark it visited, and enqueue it.
5. Repeat until the queue is empty — every reachable airport now has its shortest distance and predecessor recorded.
6. To reconstruct a path to any airport, walk backward through `parent` from that airport until reaching one with no predecessor (the start), then reverse the result.

A neighbor's distance and parent are only ever set the **first time** it's discovered. BFS explores level-by-level, so the first discovery of a node is always its shortest possible path — later discoveries of the same node can only be equal or longer, and are correctly ignored.

## Example

```python
airports = ["JFK", "LAX", "ORD", "ATL", "DFW", "SEA", "MIA", "DEN", "BOS", "SFO"]

airport_edges = [
    ("JFK", "ORD"), ("JFK", "ATL"), ("JFK", "BOS"),
    ("ORD", "DEN"), ("ORD", "DFW"),
    ("ATL", "MIA"), ("ATL", "DFW"),
    ("DFW", "LAX"),
    ("DEN", "SEA"), ("DEN", "LAX"),
    ("LAX", "SFO"),
    ("SEA", "SFO"),
    ("MIA", "DFW"),
]

distance, parent = shortest_path(airports, airport_edges, start="DEN")
print(distance)
print(parent)
```

## Usage

```bash
python ShortestPathUnweighted.py
```

## Complexity

| Aspect | Explanation |
|---|---|
| Time | **O(V + E)** — each airport is enqueued and dequeued at most once (guaranteed by the `visited` set), and each edge is examined at most twice (once from each endpoint). This gives linear time relative to the total size of the graph, rather than the O(V²) worst case seen in re-scanning approaches. |
| Space | **O(V + E)** — the `graph` dictionary has one entry per airport (V airports → O(V)), plus one entry per edge spread across all neighbor lists combined (E edges → O(E)). The `distance`, `parent`, and `visited` structures each add at most O(V) additional space. Adding these together gives **O(V + E)**. |