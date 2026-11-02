"""Slow but obviously correct solutions, used as a baseline and as a test oracle."""

from collections.abc import Sequence

from prefix_sum import Span


def sum_range_brute(values: Sequence[int], start: int, stop: int) -> int:
    """Add up values[start:stop] from scratch."""
    return sum(values[start:stop])


def longest_subarray_brute(values: Sequence[int], target: int) -> Span | None:
    """Return (start, stop) of the longest subarray summing to target."""
    best: Span | None = None
    for start in range(len(values)):
        total = 0
        for stop in range(start + 1, len(values) + 1):
            total += values[stop - 1]
            if total == target and (best is None or stop - start > best[1] - best[0]):
                best = (start, stop)
    return best


def count_subarrays_brute(values: Sequence[int], target: int) -> int:
    """Count the subarrays that sum to target."""
    count = 0
    for start in range(len(values)):
        total = 0
        for stop in range(start + 1, len(values) + 1):
            total += values[stop - 1]
            if total == target:
                count += 1
    return count


def region_sum_brute(
    grid: Sequence[Sequence[int]],
    row_start: int,
    row_stop: int,
    col_start: int,
    col_stop: int,
) -> int:
    """Add up every cell in the rectangle from scratch."""
    return sum(
        grid[r][c] for r in range(row_start, row_stop) for c in range(col_start, col_stop)
    )
