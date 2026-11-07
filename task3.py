"""Завдання 3. Алгоритм Дейкстри з бінарною купою (heapq)."""
import heapq


class Graph:
    """Неорієнтований зважений граф у вигляді списків суміжності."""

    def __init__(self):
        self.adjacency = {}

    def add_vertex(self, v):
        self.adjacency.setdefault(v, [])

    def add_edge(self, u, v, weight):
        if weight < 0:
            raise ValueError("Дейкстра не працює з від'ємними вагами")
        self.add_vertex(u)
        self.add_vertex(v)
        self.adjacency[u].append((v, weight))
        self.adjacency[v].append((u, weight))


def dijkstra(graph, start):
    """Повертає (distances, previous) від start до всіх вершин.

    Купа зберігає пари (відстань, вершина), тож heappop завжди дає
    найближчу необроблену вершину за O(log V).
    Загальна складність: O((V + E) log V).
    """
    distances = {v: float("inf") for v in graph.adjacency}
    previous = {v: None for v in graph.adjacency}
    distances[start] = 0

    heap = [(0, start)]
    visited = set()

    while heap:
        current_dist, u = heapq.heappop(heap)
        if u in visited:
            continue  # застарілий запис у купі
        visited.add(u)

        for v, weight in graph.adjacency[u]:
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, previous


def build_path(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return path[::-1]


if __name__ == "__main__":
    g = Graph()
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10),
        ("C", "E", 3), ("E", "D", 4), ("D", "F", 11), ("E", "F", 8),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)

    start = "A"
    distances, previous = dijkstra(g, start)

    print(f"Найкоротші шляхи від вершини {start}:")
    for vertex in sorted(distances):
        path = " -> ".join(build_path(previous, vertex))
        print(f"  до {vertex}: {distances[vertex]:>3}   шлях: {path}")
