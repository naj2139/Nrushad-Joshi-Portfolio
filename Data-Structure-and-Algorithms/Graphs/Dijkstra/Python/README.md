# Shortest Path Scheduler (Weighted Dijkstra)

A Python implementation of **Dijkstra's algorithm** for weighted shortest-path
computation, modeled around a real-world use case: finding the minimum travel cost
between locations on a map where each route has a different weighted "distance."

## Problem

Given a set of locations and a list of direct routes `(location_a, location_b, weight)`,
find the minimum total travel cost from a starting location to every other location.

Since routes carry different weights (unlike a simple hop-count problem), this is a
classic **weighted shortest path** problem — solvable with Dijkstra's algorithm rather
than plain BFS, which only works when every edge counts equally.

## Approach

This implementation uses standard Dijkstra's algorithm with a binary heap
(`heapq`) as the priority queue:

1. Build an adjacency list where every route is added in **both directions**, since
   travel is undirected (a route A-B means you can travel A→B and B→A).
2. Initialize every location's distance to `infinity`, except the start location,
   which is set to `0` and pushed onto the heap as `(0, start)`.
3. While the heap is not empty, pop the entry with the smallest known distance.
4. Skip the entry if it's **stale** — i.e., a shorter distance to that node has
   already been finalized since this entry was pushed.
5. For each neighbor, compute the total distance through the current node. If this
   is shorter than the neighbor's current known distance, update it (**relax the
   edge**) and push the neighbor back onto the heap.
6. Repeat until the heap is empty — every reachable location now holds its true
   shortest distance from `start`.

Unlike BFS, a node's distance can be updated **more than once** before it's
finalized, because a shorter path through a different route may be discovered
later. The heap always pops the smallest known distance first, which guarantees
that once a node is popped, its distance can never be improved again — this is
what makes the greedy strategy correct.

## Example

```python
locations = [
    "Castle", "Village", "Forest", "River", "Cave",
    "Tower", "Dungeon", "Mine", "Temple", "Harbor",
]

map_edges = [
    ("Castle", "Village", 4),
    ("Castle", "Forest", 7),
    ("Village", "River", 3),
    ("Village", "Mine", 8),
    ("Forest", "Cave", 5),
    ("Forest", "Temple", 6),
    ("River", "Dungeon", 7),
    ("River", "Temple", 4),
    ("Cave", "Tower", 6),
    ("Mine", "Dungeon", 3),
    ("Dungeon", "Harbor", 5),
    ("Tower", "Harbor", 4),
    ("Temple", "Harbor", 8),
]

shortest_distances = dijkstra(locations, map_edges, start="Forest")
print(shortest_distances)
```

Output:

```
Castle: 7
Village: 11
Forest: 0
River: 10
Cave: 5
Tower: 11
Dungeon: 17
Mine: 19
Temple: 6
Harbor: 14
```

## Usage

```bash
python Dijkstra.py
```

## Complexity

| Aspect | Explanation |
|---|---|
| Time | **O((V + E) log V)** — every edge can trigger at most one heap push (a relaxation), and every push/pop on a heap costs O(log n) where n is the heap size. Since the heap can hold at most O(E) entries, each push/pop costs O(log E), which is O(log V) because E ≤ V². Building the adjacency list takes O(V + E), and processing every push/pop across all edges gives O(E log V) total for the heap operations, plus O(V) for initialization — combined, this is **O((V + E) log V)**. This is more expensive than BFS's O(V + E) because BFS only ever needs to check "have I seen this node," while Dijkstra must repeatedly re-compare and re-rank distances as shorter paths are discovered, which is exactly what the heap is for. |
| Space | **O(V + E)** — the `graph` dictionary has one entry per location (V locations → O(V)), plus one entry per edge spread across all neighbor lists combined (E edges → O(E)). The `distance` dictionary adds O(V), and the `priority_queue` can hold at most one entry per relaxation, which is bounded by O(E) in the worst case (each edge can trigger one push). Adding these together gives **O(V + E)**. |