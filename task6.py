"""Завдання 6. Вибір їжі з максимальною калорійністю в межах бюджету.

Жадібний алгоритм: беремо страви за спаданням співвідношення calories/cost.
Динамічне програмування: класична задача рюкзака 0/1 (кожну страву можна взяти один раз).
"""

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items, budget):
    """Жадібно додає страви з найкращим співвідношенням калорій до вартості.

    Швидко (O(n log n)), але не гарантує оптимального результату.
    """
    ranked = sorted(items.items(),
                    key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
                    reverse=True)
    chosen, total_cost, total_calories = [], 0, 0
    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]
    return {"items": chosen, "total_cost": total_cost, "total_calories": total_calories}


def dynamic_programming(items, budget):
    """Рюкзак 0/1: dp[i][b] - максимум калорій з перших i страв при бюджеті b.

    Складність O(n * budget), результат завжди оптимальний.
    """
    names = list(items)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо страву
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)

    # відновлюємо набір страв, рухаючись назад по таблиці
    chosen, b = [], budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]
    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    return {"items": chosen, "total_cost": total_cost, "total_calories": dp[n][budget]}


def print_result(title, result):
    print(f"  {title:<24} {', '.join(result['items']) or '-'}")
    print(f"  {'':<24} вартість: {result['total_cost']}, калорії: {result['total_calories']}")


if __name__ == "__main__":
    for budget in (40, 100, 120):
        print(f"Бюджет: {budget}")
        print_result("Жадібний алгоритм:", greedy_algorithm(items, budget))
        print_result("Динамічне програмування:", dynamic_programming(items, budget))
        print()
