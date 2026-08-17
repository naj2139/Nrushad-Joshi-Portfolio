# Course Prerequisite Scheduler (Topological Sort)

A Python implementation of **Kahn's Algorithm** for topological sorting, modeled around a real-world use case: determining a valid order to take courses given their prerequisite relationships.

## Problem

Given a set of courses and a list of prerequisite pairs `(prereq, course)`, find an order in which all courses can be completed such that every prerequisite is taken before the course that depends on it.

This is a classic **Directed Acyclic Graph (DAG)** problem.

## Approach

This implementation uses a **layer-by-layer variant of Kahn's Algorithm**:

1. Build an adjacency list and compute the indegree (number of incoming edges) for every node.
2. Each pass, find **all** nodes currently at indegree 0 — these have no unmet prerequisites and form one "layer."
3. Decrement the indegree of each layer's neighbors, since those prerequisites are now satisfied.
4. Remove the processed layer and repeat until no nodes remain.
5. The order in which layers were removed is a valid topological sort.

Unlike a strict single-node-at-a-time queue implementation, this version processes an entire batch of ready nodes per pass — useful for visualizing which courses could be taken **in parallel** during the same term.

## Example

```python
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
print(result)
```

## Usage

```bash
python topological_sort.py
```

## Complexity
| Aspect | Explanation |
|---|---|
| Worst-case Time | **O(V²)** — occurs when the graph is a long, narrow chain (e.g., `A → B → C → D → ...`) where only **one** node becomes ready (indegree 0) per pass. Since the `while vertex:` loop scans every remaining node each pass just to find the ready ones, and only one node is removed per pass, the work done is `V + (V-1) + (V-2) + ... + 1 + 0`, which sums to `V(V+1)/2` → simplified to **O(V²)**. |
| Space | **O(V + E)** — the `graph` dictionary has one entry per vertex (V courses → V dictionary entries → O(V)), plus one entry per edge spread across all the neighbor lists combined (E edges → E total items stored across all lists → O(E)). Adding these together gives O(V) + O(E) = **O(V + E)**. |