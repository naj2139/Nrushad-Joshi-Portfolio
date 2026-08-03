from typing import List, Tuple
import heapq


def dijkstra(locations: List[str], map_edges: List[Tuple[str, str, int]], start: str):
    """
    Compute the shortest distance from the start node to every other node
    using Dijkstra's algorithm.

    Key algorithm concept:
    ----------------------
    Dijkstra's algorithm always processes the node with the smallest known
    distance from the start. A min-heap (priority queue) efficiently keeps
    track of which node should be processed next.
    """

    graph = {}
    distance = {}
    priority_queue = []

    # Initialize the graph and distance table.
    #
    # Every node initially has an infinite distance because no path from
    # the start node has been discovered yet.
    for location in locations:
        graph[location] = []
        distance[location] = float("inf")

    # Build an undirected weighted graph.
    #
    # Each edge is stored in both directions because travel is allowed
    # from source -> destination and destination -> source.
    for source, destination, weight in map_edges:
        graph[source].append((destination, weight))
        graph[destination].append((source, weight))

    # The start node is zero distance away from itself.
    distance[start] = 0

    # A min-heap stores:
    #     (distance_from_start, node)
    #
    # Dijkstra always expands the closest discovered node first.
    # A min-heap guarantees that the smallest known distance is processed
    # before every other candidate.
    heapq.heappush(priority_queue, (0, start))

    while priority_queue:

        # Remove the node with the smallest known distance.
        #
        # Unlike a normal queue (FIFO), the priority queue always returns
        # the closest discovered node.
        curr_node_dist, node = heapq.heappop(priority_queue)

        # Skip outdated heap entries.
        #
        # The same node may appear multiple times in the heap because a
        # shorter path may be discovered after it has already been added.
        #
        # Example:
        #     (15, "Mine")
        #     (12, "Mine")
        #
        # Once the shorter distance (12) has been processed, the older
        # entry (15) is stale and can safely be ignored.
        if curr_node_dist > distance[node]:
            continue

        # Examine every neighboring node.
        for neighbor_node, edge_weight in graph[node]:

            # Compute the total distance from the start node to the
            # neighbor through the current node.
            #
            # Dijkstra compares TOTAL path distances, not individual
            # edge weights.
            new_dist = curr_node_dist + edge_weight

            # Relax the edge.
            #
            # If a shorter path is found, update the shortest known
            # distance and push the updated node into the priority queue.
            if new_dist < distance[neighbor_node]:
                distance[neighbor_node] = new_dist
                heapq.heappush(priority_queue, (new_dist, neighbor_node))

    return distance


if __name__ == "__main__":

    locations = [
        "Castle",
        "Village",
        "Forest",
        "River",
        "Cave",
        "Tower",
        "Dungeon",
        "Mine",
        "Temple",
        "Harbor",
    ]

    # Undirected weighted edges (travel cost)
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

    shortest_distances = dijkstra(
        locations,
        map_edges,
        start="Forest",
    )

    print(shortest_distances)