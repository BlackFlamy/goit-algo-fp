"""Завдання 2. Рекурсивний фрактал "дерево Піфагора".

Запуск: python task2.py            (рівень запитується з клавіатури)
        python task2.py 8          (рівень передається аргументом)
"""
import math
import sys

import matplotlib.pyplot as plt


def draw_branch(ax, x, y, angle, length, level, max_level):
    """Малює гілку і рекурсивно дві дочірні під кутом +/-45 градусів."""
    if level == 0:
        return
    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)

    # товщина і колір залежать від глибини: стовбур коричневий, кінчики зелені
    depth = max_level - level
    t = depth / max(max_level - 1, 1)
    color = (0.45 * (1 - t), 0.3 + 0.4 * t, 0.1)
    ax.plot([x, x2], [y, y2], color=color, linewidth=max(level * 0.8, 0.5))

    new_length = length * math.sqrt(2) / 2  # як у класичному дереві Піфагора
    draw_branch(ax, x2, y2, angle + math.pi / 4, new_length, level - 1, max_level)
    draw_branch(ax, x2, y2, angle - math.pi / 4, new_length, level - 1, max_level)


def draw_pythagoras_tree(level):
    fig, ax = plt.subplots(figsize=(9, 8))
    draw_branch(ax, 0, 0, math.pi / 2, 1.0, level, level)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Дерево Піфагора, рівень рекурсії: {level}")
    plt.show()


def read_level():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = input("Введіть рівень рекурсії (1-16, рекомендовано 8-12): ")
    try:
        level = int(raw)
    except ValueError:
        sys.exit("Рівень має бути цілим числом")
    if not 1 <= level <= 16:
        sys.exit("Рівень має бути в межах від 1 до 16")
    return level


if __name__ == "__main__":
    draw_pythagoras_tree(read_level())
