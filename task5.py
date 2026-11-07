"""Завдання 5. Візуалізація обходів бінарного дерева: у глибину (DFS) та в ширину (BFS).

Обидва обходи ітеративні: DFS використовує стек, BFS - чергу (deque), без рекурсії.
Кожен відвіданий вузол отримує унікальний колір у форматі #RRGGBB:
від темного (перший відвіданий) до світлого (останній).

Запуск: python task5.py           (підсумкові картинки обох обходів)
        python task5.py --steps   (покрокова анімація кожного обходу)
"""
import heapq
import sys
from collections import deque

import matplotlib.pyplot as plt

from task4 import draw_tree, heap_to_tree

DARK = (0x0B, 0x1F, 0x3A)   # темно-синій
LIGHT = (0xCF, 0xE8, 0xFF)  # світло-блакитний
UNVISITED = "#D9D9D9"


def gradient(n):
    """Повертає n кольорів #RRGGBB від темного до світлого."""
    colors = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        rgb = (round(d + (l - d) * t) for d, l in zip(DARK, LIGHT))
        colors.append("#{:02X}{:02X}{:02X}".format(*rgb))
    return colors


def count_nodes(root):
    count, stack = 0, [root] if root else []
    while stack:
        node = stack.pop()
        count += 1
        stack.extend(child for child in (node.left, node.right) if child)
    return count


def dfs(root):
    """Прямий обхід (preorder) у глибину за допомогою стеку."""
    order, stack = [], [root]
    while stack:
        node = stack.pop()
        order.append(node)
        # правий кладемо першим, щоб лівий обробився раніше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs(root):
    """Обхід у ширину за допомогою черги."""
    order, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


def reset_colors(root):
    stack = [root]
    while stack:
        node = stack.pop()
        node.color = UNVISITED
        stack.extend(child for child in (node.left, node.right) if child)


def show_final(root, traversals):
    """Показує результат обох обходів поруч."""
    fig, axes = plt.subplots(1, len(traversals), figsize=(8 * len(traversals), 5))
    colors = gradient(count_nodes(root))
    for ax, (name, func) in zip(axes, traversals):
        order = func(root)
        for node, color in zip(order, colors):
            node.color = color
        sequence = " -> ".join(str(n.val) for n in order)
        draw_tree(root, title=f"{name}\n{sequence}", ax=ax)
        print(f"{name}: {sequence}")
    plt.tight_layout()
    plt.show()


def show_steps(root, name, func, delay=0.8):
    """Покроково зафарбовує вузли в порядку обходу."""
    order = func(root)
    colors = gradient(len(order))
    reset_colors(root)
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 5))
    for step, (node, color) in enumerate(zip(order, colors), start=1):
        node.color = color
        ax.clear()
        draw_tree(root, title=f"{name}: крок {step}/{len(order)}, вузол {node.val} ({color})", ax=ax)
        plt.pause(delay)
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    data = [15, 3, 17, 10, 84, 19, 6, 22, 9, 1, 30]
    heapq.heapify(data)
    root = heap_to_tree(data)

    traversals = [("Обхід у глибину (DFS, стек)", dfs), ("Обхід у ширину (BFS, черга)", bfs)]

    if "--steps" in sys.argv:
        for name, func in traversals:
            show_steps(root, name, func)
    else:
        show_final(root, traversals)
