import random

import pytest

from brute_force import (
    count_subarrays_brute,
    longest_subarray_brute,
    region_sum_brute,
    sum_range_brute,
)
from prefix_sum import (
    RangeSum,
    RegionSum,
    build_prefix,
    count_subarrays_with_sum,
    longest_subarray_with_sum,
)


def test_build_prefix_starts_with_zero() -> None:
    assert build_prefix([3, 1, 4, 1, 5]) == [0, 3, 4, 8, 9, 14]
    assert build_prefix([]) == [0]


def test_range_sum_example() -> None:
    queries = RangeSum([3, 1, 4, 1, 5, 9, 2, 6])
    assert queries.sum_range(2, 6) == 19
    assert queries.sum_range(0, 8) == 31
    assert queries.sum_range(3, 3) == 0  # an empty range


@pytest.mark.parametrize(("start", "stop"), [(-1, 2), (3, 2), (0, 9)])
def test_range_sum_rejects_bad_ranges(start: int, stop: int) -> None:
    with pytest.raises(ValueError):
        RangeSum([1, 2, 3]).sum_range(start, stop)


def test_range_sum_does_not_follow_later_changes_to_the_list() -> None:
    values = [1, 2, 3]
    queries = RangeSum(values)
    values[0] = 100
    assert queries.sum_range(0, 3) == 6


def test_range_sum_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(42)
    for _ in range(500):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
        queries = RangeSum(values)
        for _ in range(10):
            start = rng.randint(0, len(values))
            stop = rng.randint(start, len(values))
            assert queries.sum_range(start, stop) == sum_range_brute(values, start, stop)


def test_subarray_examples_with_negative_numbers() -> None:
    assert longest_subarray_with_sum([1, -1, 5, -2, 3], 3) == (0, 4)
    assert count_subarrays_with_sum([1, -1, 1], 1) == 3
    assert longest_subarray_with_sum([1, 2, 3], 100) is None


def test_subarray_tools_agree_with_brute_force_on_random_input() -> None:
    rng = random.Random(7)
    for _ in range(1_000):
        values = [rng.randint(-5, 5) for _ in range(rng.randint(0, 14))]
        target = rng.randint(-6, 6)
        assert longest_subarray_with_sum(values, target) == longest_subarray_brute(values, target)
        assert count_subarrays_with_sum(values, target) == count_subarrays_brute(values, target)


def test_region_sum_example() -> None:
    grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    regions = RegionSum(grid)
    assert regions.sum_region(1, 3, 1, 3) == 28  # 5 + 6 + 8 + 9
    assert regions.sum_region(0, 3, 0, 3) == 45


def test_region_sum_rejects_ragged_grid() -> None:
    with pytest.raises(ValueError):
        RegionSum([[1, 2], [3]])


def test_region_sum_agrees_with_brute_force_on_random_input() -> None:
    rng = random.Random(3)
    for _ in range(300):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        grid = [[rng.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]
        regions = RegionSum(grid)
        r1 = rng.randint(0, rows)
        r2 = rng.randint(r1, rows)
        c1 = rng.randint(0, cols)
        c2 = rng.randint(c1, cols)
        assert regions.sum_region(r1, r2, c1, c2) == region_sum_brute(grid, r1, r2, c1, c2)
