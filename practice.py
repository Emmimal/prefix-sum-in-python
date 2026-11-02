"""Practice problems for the prefix sum technique."""

from collections import Counter
from collections.abc import Sequence

from prefix_sum import longest_subarray_with_sum


def pivot_index(values: Sequence[int]) -> int:
    """Return the first index where the sum on the left equals the sum on the right.

    Returns -1 if there is no such index.
    """
    total = sum(values)
    left_sum = 0
    for index, value in enumerate(values):
        if left_sum == total - left_sum - value:
            return index
        left_sum += value
    return -1


def subarrays_divisible_by_k(values: Sequence[int], k: int) -> int:
    """Return how many subarrays have a sum divisible by k."""
    if k < 1:
        raise ValueError("k must be at least 1")
    seen = Counter({0: 1})
    running = 0
    count = 0
    for value in values:
        running = (running + value) % k  # Python's % is never negative here.
        count += seen[running]
        seen[running] += 1
    return count


def longest_balanced_run(bits: Sequence[int]) -> int:
    """Return the length of the longest run with equally many 0s and 1s."""
    swapped = [1 if bit == 1 else -1 for bit in bits]
    result = longest_subarray_with_sum(swapped, 0)
    return 0 if result is None else result[1] - result[0]
