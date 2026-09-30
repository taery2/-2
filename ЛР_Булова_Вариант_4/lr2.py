"""
Лабораторная работа № 2
Предмет: Основы алгоритмизации и программирование
Студент: Булова Екатерина
Группа: БИ 2-1
Вариант: 4

Эмпирический анализ временной сложности сортировки пузырьком
и сортировки вставками.
Дополнительное задание М4:
сравнение типов данных R, S, V, N при n = 3000.
"""

import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt


SIZES = [200, 400, 800, 1600, 3200]
REPEATS = 5
LO, HI = -500, 500
SEED = 42


def bubble_sort(arr):
    """Сортировка пузырьком с флагом досрочного выхода.
    Исходный массив не изменяется.
    """
    a = arr.copy()
    n = len(a)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break

    return a


def insertion_sort(arr):
    """Сортировка вставками.
    Исходный массив не изменяется.
    """
    a = arr.copy()

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1

        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1

        a[j + 1] = key

    return a


def generate_data(n, kind="random", lo=LO, hi=HI, seed=SEED):
    """Генерирует воспроизводимый массив заданного типа.

    R — случайный;
    S — упорядоченный;
    V — обратно упорядоченный;
    N — почти упорядоченный (около 5% перестановок).
    """
    rng = random.Random(seed + n)
    data = [rng.randint(lo, hi) for _ in range(n)]

    if kind == "sorted":
        data.sort()
    elif kind == "reversed":
        data.sort(reverse=True)
    elif kind == "nearly_sorted":
        data.sort()
        for _ in range(max(1, n // 20)):
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
    elif kind != "random":
        raise ValueError(f"Неизвестный тип данных: {kind}")

    return data


def measure(sort_func, data, repeats=REPEATS):
    """Возвращает медианное время работы алгоритма в секундах."""
    times = []
    expected = sorted(data)

    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data)
        elapsed = time.perf_counter() - start

        if result != expected:
            raise AssertionError(f"Ошибка сортировки: {sort_func.__name__}")

        times.append(elapsed)

    return statistics.median(times)


def run_main_experiment():
    """Эксперимент для размеров варианта 4."""
    algorithms = {
        "Пузырьком": bubble_sort,
        "Вставками": insertion_sort,
    }
    results = {name: [] for name in algorithms}

    for n in SIZES:
        data = generate_data(n, "random")
        for name, func in algorithms.items():
            results[name].append(measure(func, data))

    return results


def run_m4_experiment():
    """М4: все типы R/S/V/N при n=3000."""
    kinds = {
        "R": "random",
        "S": "sorted",
        "V": "reversed",
        "N": "nearly_sorted",
    }
    algorithms = {
        "Пузырьком": bubble_sort,
        "Вставками": insertion_sort,
    }
    results = {name: {} for name in algorithms}

    for code, kind in kinds.items():
        data = generate_data(3000, kind)
        for name, func in algorithms.items():
            results[name][code] = measure(func, data)

    return results


def save_time_plot(results):
    """Сохраняет график T(n)."""
    plt.figure(figsize=(9, 5.5))
    for name, times in results.items():
        plt.plot(SIZES, times, marker="o", label=name)

    plt.xlabel("Размер массива n")
    plt.ylabel("Медианное время, с")
    plt.title("ЛР №2, вариант 4: время сортировки")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr2_time_plot.png", dpi=160)
    plt.close()


def save_m4_plot(results):
    """Сохраняет столбчатую диаграмму дополнительного задания М4."""
    codes = ["R", "S", "V", "N"]
    x = list(range(len(codes)))
    width = 0.36

    bubble = [results["Пузырьком"][code] for code in codes]
    insertion = [results["Вставками"][code] for code in codes]

    plt.figure(figsize=(9, 5.5))
    plt.bar([i - width / 2 for i in x], bubble, width, label="Пузырьком")
    plt.bar([i + width / 2 for i in x], insertion, width, label="Вставками")
    plt.xticks(x, codes)
    plt.xlabel("Тип данных")
    plt.ylabel("Медианное время, с")
    plt.title("М4: сравнение типов данных при n = 3000")
    plt.grid(axis="y")
    plt.legend()
    plt.tight_layout()
    plt.savefig("m4_bar_plot.png", dpi=160)
    plt.close()


def print_results(results, m4):
    print("\nОсновной эксперимент:")
    print(f"{'n':>8}{'Пузырьком':>16}{'Вставками':>16}")
    for i, n in enumerate(SIZES):
        print(f"{n:>8}{results['Пузырьком'][i]:>16.6f}{results['Вставками'][i]:>16.6f}")

    print("\nМ4: n = 3000")
    print(f"{'Тип':>8}{'Пузырьком':>16}{'Вставками':>16}")
    for code in ["R", "S", "V", "N"]:
        print(f"{code:>8}{m4['Пузырьком'][code]:>16.6f}{m4['Вставками'][code]:>16.6f}")


if __name__ == "__main__":
    main_results = run_main_experiment()
    m4_results = run_m4_experiment()
    print_results(main_results, m4_results)
    save_time_plot(main_results)
    save_m4_plot(m4_results)
    print("\nГрафики сохранены в lr2_time_plot.png и m4_bar_plot.png")
