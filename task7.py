"""Завдання 7. Метод Монте-Карло: імовірності сум при киданні двох кубиків.

Запуск: python task7.py              (1 000 000 кидків, seed=42)
        python task7.py 100000       (власна кількість кидків)
        python task7.py 100000 7     (власна кількість кидків і seed)
"""
import random
import sys
from collections import Counter

import matplotlib.pyplot as plt

SUMS = range(2, 13)


def simulate(num_rolls, seed=None):
    """Кидає два кубики num_rolls разів і повертає частоту кожної суми."""
    rng = random.Random(seed)
    counts = Counter(rng.randint(1, 6) + rng.randint(1, 6) for _ in range(num_rolls))
    return {s: counts[s] / num_rolls for s in SUMS}


def analytical():
    """Точні ймовірності: кількість комбінацій із сумою s серед 36 можливих."""
    return {s: (6 - abs(s - 7)) / 36 for s in SUMS}


def print_table(mc, exact):
    print(f"{'Сума':>4} | {'Монте-Карло':>11} | {'Аналітично':>10} | {'Різниця':>8}")
    print("-" * 44)
    for s in SUMS:
        diff = (mc[s] - exact[s]) * 100
        print(f"{s:>4} | {mc[s]:>10.2%} | {exact[s]:>9.2%} | {diff:>+7.3f}%")
    max_diff = max(abs(mc[s] - exact[s]) for s in SUMS) * 100
    print("-" * 44)
    print(f"Максимальне абсолютне відхилення: {max_diff:.3f} в. п.")


def plot(mc, exact, num_rolls):
    sums = list(SUMS)
    width = 0.4
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([s - width / 2 for s in sums], [mc[s] * 100 for s in sums],
           width, label="Монте-Карло", color="#1296F0")
    ax.bar([s + width / 2 for s in sums], [exact[s] * 100 for s in sums],
           width, label="Аналітично", color="#F0A012")
    for s in sums:
        ax.text(s - width / 2, mc[s] * 100 + 0.2, f"{mc[s]:.2%}",
                ha="center", fontsize=7, rotation=90)
    ax.set_ylim(0, max(mc.values()) * 100 * 1.15)
    ax.set_xticks(sums)
    ax.set_xlabel("Сума на двох кубиках")
    ax.set_ylabel("Імовірність, %")
    ax.set_title(f"Імовірності сум двох кубиків ({num_rolls:,} кидків)".replace(",", " "))
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    num_rolls = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42  # фіксований seed = відтворюваний результат
    mc = simulate(num_rolls, seed)
    exact = analytical()
    print(f"Кількість кидків: {num_rolls}, seed: {seed}\n")
    print_table(mc, exact)
    plot(mc, exact, num_rolls)
