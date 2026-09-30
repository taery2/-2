"""Общие функции генерации данных и измерения времени для лабораторных работ."""

import random
import statistics
import time


def generate_data(n, kind="random", lo=-500, hi=500, seed=42):
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
    return data


def measure(sort_func, data, repeats=5):
    times = []
    expected = sorted(data)
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data)
        times.append(time.perf_counter() - start)
        assert result == expected
    return statistics.median(times)
