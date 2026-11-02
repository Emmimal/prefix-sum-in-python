import random
from itertools import batched

import pytest

from brute_force import count_subarrays_brute
from prefix_sum import count_subarrays_with_sum
from shortcuts import (
    block_sums,
    count_zero_sum_subarrays,
    shortest_burst_bisect,
    window_sums,
)


def test_window_sums_example() -> None:
    assert window_sums([2, 1, 5, 1, 3, 2], 3) == [8, 7, 9, 6]
    assert window_sums([1, 2], 3) == []


def test_block_sums_example() -> None:
    assert block_sums([1, 2, 3, 4, 5], 2) == [3, 7, 5]
    assert block_sums([], 3) == []


def test_block_sums_match_itertools_batched() -> None:
    rng = random.Random(1)
    for _ in range(200):
        values = [rng.randint(-9, 9) for _ in range(rng.randint(0, 40))]
        size = rng.randint(1, 8)
        assert block_sums(values, size) == [sum(batch) for batch in batched(values, size)]


def test_window_sums_match_slicing() -> None:
    rng = random.Random(2)
    for _ in range(200):
        values = [rng.randint(-9, 9) for _ in range(rng.randint(1, 30))]
        size = rng.randint(1, len(values))
        expected = [sum(values[i : i + size]) for i in range(len(values) - size + 1)]
        assert window_sums(values, size) == expected


@pytest.mark.parametrize("size", [0, -1])
def test_bad_sizes_are_rejected(size: int) -> None:
    with pytest.raises(ValueError):
        window_sums([1, 2, 3], size)
    with pytest.raises(ValueError):
        block_sums([1, 2, 3], size)


def test_shortest_burst_bisect_example() -> None:
    assert shortest_burst_bisect([2, 3, 1, 2, 4, 3], 7) == (4, 6)
    assert shortest_burst_bisect([1, 1], 5) is None


def test_shortest_burst_bisect_rejects_negative_counts() -> None:
    with pytest.raises(ValueError):
        shortest_burst_bisect([2, -1, 2, 3], 5)


def test_shortest_burst_bisect_agrees_with_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(500):
        counts = [rng.randint(0, 6) for _ in range(rng.randint(0, 15))]
        target = rng.randint(1, 12)
        best = None
        for start in range(len(counts)):
            for stop in range(start + 1, len(counts) + 1):
                if sum(counts[start:stop]) >= target and (
                    best is None or stop - start < best[1] - best[0]
                ):
                    best = (start, stop)
                    break
        assert shortest_burst_bisect(counts, target) == best


def test_zero_sum_count_agrees_with_the_general_counter() -> None:
    assert count_zero_sum_subarrays([1, -1, 1, -1]) == 4
    rng = random.Random(5)
    for _ in range(500):
        values = [rng.randint(-3, 3) for _ in range(rng.randint(0, 14))]
        assert count_zero_sum_subarrays(values) == count_subarrays_with_sum(values, 0)
        assert count_zero_sum_subarrays(values) == count_subarrays_brute(values, 0)
