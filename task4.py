"""Завдання 4. Візуалізація бінарної купи.

Купа зберігається як масив: для вузла з індексом i
лівий нащадок має індекс 2i+1, правий 2i+2.
Функція heap_to_tree перетворює такий масив на дерево з вузлів Node,
а draw_tree (з наданого коду) його малює.
"""
import heapq
import uuid

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # колір вузла
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title=None, ax=None):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    show = ax is None
    if show:
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
    nx.draw(tree, pos=pos, with_labels=False, arrows=False, node_size=2500,
            node_color=colors, ax=ax)
    # білий текст на темних вузлах, чорний на світлих
    for node_id, label in labels.items():
        r, g, b = mcolors.to_rgb(tree.nodes[node_id]["color"])
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        x, y = pos[node_id]
        ax.text(x, y, str(label), ha="center", va="center", fontsize=11,
                color="white" if luminance < 0.5 else "black")
    if title:
        ax.set_title(title)
    if show:
        plt.show()


def heap_to_tree(heap):
    """Будує дерево з масиву-купи за правилом індексів 2i+1 / 2i+2."""
    if not heap:
        return None
    nodes = [Node(value) for value in heap]
    for i, node in enumerate(nodes):
        left, right = 2 * i + 1, 2 * i + 2
        if left < len(nodes):
            node.left = nodes[left]
        if right < len(nodes):
            node.right = nodes[right]
    return nodes[0]


def draw_heap(heap, title="Бінарна купа"):
    root = heap_to_tree(heap)
    if root is None:
        print("Купа порожня")
        return
    draw_tree(root, title=title)


if __name__ == "__main__":
    data = [15, 3, 17, 10, 84, 19, 6, 22, 9]

    min_heap = data[:]
    heapq.heapify(min_heap)
    print("Min-купа (масив):", min_heap)
    draw_heap(min_heap, title=f"Min-купа: {min_heap}")

    # max-купа: heapq працює лише з min-купою, тому інвертуємо знаки
    max_heap = [-x for x in data]
    heapq.heapify(max_heap)
    max_heap = [-x for x in max_heap]
    print("Max-купа (масив):", max_heap)
    draw_heap(max_heap, title=f"Max-купа: {max_heap}")
