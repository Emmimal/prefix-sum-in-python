"""Buggy versions of the prefix sum tools, kept so tests can show how they fail."""

from collections import Counter
from collections.abc import Sequence
from itertools import accumulate


def sum_range_inclusive_mixup(values: Sequence[int], left: int, right: int) -> int:
    """Bug: treats `right` as included, but uses the half-open formula."""
    prefix = list(accumulate(values, initial=0))
    return prefix[right] - prefix[left]  # Should be prefix[right + 1].


def count_subarrays_no_seed(values: Sequence[int], target: int) -> int:
    """Bug: forgets that the empty prefix (sum 0) has been seen once."""
    seen: Counter[int] = Counter()  # Missing: Counter({0: 1})
    running = 0
    count = 0
    for value in values:
        running += value
        count += seen[running - target]
        seen[running] += 1
    return count


def count_subarrays_sliding_window(values: Sequence[int], target: int) -> int:
    """Bug: a sliding window that assumes the numbers are never negative."""
    left = 0
    window_total = 0
    count = 0
    for right, value in enumerate(values):
        window_total += value
        while window_total > target and left <= right:
            window_total -= values[left]
            left += 1
        if window_total == target:
            count += 1
    return count
