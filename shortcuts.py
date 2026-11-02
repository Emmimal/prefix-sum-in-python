"""Short, built-in ways to get common prefix sum results."""

from bisect import bisect_left
from collections import Counter
from collections.abc import Sequence
from itertools import pairwise
from math import comb

from prefix_sum import Span, build_prefix


def window_sums(values: Sequence[int], size: int) -> list[int]:
    """Return the sum of every window of `size` items, in one comprehension."""
    if size < 1:
        raise ValueError("size must be at least 1")
    prefix = build_prefix(values)
    return [stop - start for start, stop in zip(prefix, prefix[size:])]


def block_sums(values: Sequence[int], size: int) -> list[int]:
    """Return the sum of each consecutive block of `size` items.

    The last block is shorter if the length is not a multiple of `size`.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    prefix = build_prefix(values)
    edges = [*range(0, len(values), size), len(values)]
    return [prefix[stop] - prefix[start] for start, stop in pairwise(edges)]


def shortest_burst_bisect(counts: Sequence[int], target: int) -> Span | None:
    """Return (start, stop) of the shortest window with sum >= target.

    Counts must not be negative, so the prefix array only goes up and can
    be searched with bisect. Takes O(n log n) time.
    """
    if target < 1:
        raise ValueError("target must be at least 1")
    if any(count < 0 for count in counts):
        raise ValueError("counts must not be negative")

    prefix = build_prefix(counts)
    best: Span | None = None
    for start in range(len(counts)):
        stop = bisect_left(prefix, prefix[start] + target, lo=start + 1)
        if stop < len(prefix) and (best is None or stop - start < best[1] - best[0]):
            best = (start, stop)
    return best


def count_zero_sum_subarrays(values: Sequence[int]) -> int:
    """Count subarrays that sum to 0: every pair of equal prefix sums is one."""
    return sum(comb(count, 2) for count in Counter(build_prefix(values)).values())
