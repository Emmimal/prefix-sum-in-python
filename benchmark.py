"""Time prefix sums against recomputing every range."""

import random
from collections.abc import Callable
from itertools import accumulate
from time import perf_counter

from brute_force import sum_range_brute
import numpy as np

from numpy_queries import build_prefix_np, sum_ranges
from prefix_sum import RangeSum


def timed(func: Callable[[], object]) -> float:
    """Return how many seconds one call to func takes."""
    start = perf_counter()
    func()
    return perf_counter() - start


def make_queries(n: int, count: int, seed: int = 5) -> list[tuple[int, int]]:
    rng = random.Random(seed)
    queries = []
    for _ in range(count):
        start = rng.randint(0, n)
        queries.append((start, rng.randint(start, n)))
    return queries


def report_many_queries() -> None:
    n = 200_000
    values = list(range(n))
    print(f"Range sums over {n:,} values: recompute vs prefix sum")
    print(f"{'queries':>8}  {'recompute':>10}  {'prefix sum':>10}")
    for count in (10, 100, 1_000, 5_000):
        queries = make_queries(n, count)
        slow = timed(lambda: [sum_range_brute(values, a, b) for a, b in queries])

        def fast() -> None:
            ranges = RangeSum(values)
            for a, b in queries:
                ranges.sum_range(a, b)

        print(f"{count:>8,}  {slow:>9.4f}s  {timed(fast):>9.4f}s")


def report_build_cost() -> None:
    n = 1_000_000
    values = list(range(n))

    def loop() -> list[int]:
        prefix = [0]
        for value in values:
            prefix.append(prefix[-1] + value)
        return prefix

    print()
    print(f"Building a prefix array of {n:,} values")
    print(f"  manual loop:          {timed(loop):.4f}s")
    print(f"  itertools.accumulate: {timed(lambda: list(accumulate(values, initial=0))):.4f}s")


def report_numpy_batch() -> None:
    n, count = 1_000_000, 200_000
    rng = np.random.default_rng(1)
    values = rng.integers(0, 100, n)
    first = rng.integers(0, n + 1, count)
    second = rng.integers(0, n + 1, count)
    starts, stops = np.minimum(first, second), np.maximum(first, second)
    pairs = list(zip(starts.tolist(), stops.tolist()))
    as_list = values.tolist()

    def python_way() -> None:
        ranges = RangeSum(as_list)
        for a, b in pairs:
            ranges.sum_range(a, b)

    def numpy_way() -> None:
        sum_ranges(build_prefix_np(values), starts, stops)

    print()
    print(f"{count:,} range queries over {n:,} values (build included)")
    print(f"  RangeSum in a Python loop: {timed(python_way):.4f}s")
    print(f"  NumPy batch:               {timed(numpy_way):.4f}s")


if __name__ == "__main__":
    report_many_queries()
    report_build_cost()
    report_numpy_batch()
