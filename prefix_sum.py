"""A small toolkit of prefix sum solutions."""

from collections import Counter
from collections.abc import Iterable, Sequence
from itertools import accumulate

type Span = tuple[int, int]  # (start, stop), stop excluded, like a slice


def build_prefix(values: Iterable[int]) -> list[int]:
    """Return the prefix sums of `values`, starting with a 0.

    The result is one item longer than the input:
    prefix[i] is the sum of the first i values.
    """
    return list(accumulate(values, initial=0))


class RangeSum:
    """Answer "what is the sum of values[start:stop]?" in O(1) time."""

    __slots__ = ("_prefix",)

    def __init__(self, values: Iterable[int]) -> None:
        self._prefix = build_prefix(values)

    def __len__(self) -> int:
        return len(self._prefix) - 1

    def sum_range(self, start: int, stop: int) -> int:
        """Return the sum of values[start:stop]. The stop index is excluded."""
        if not 0 <= start <= stop <= len(self):
            raise ValueError(f"need 0 <= start <= stop <= {len(self)}")
        return self._prefix[stop] - self._prefix[start]


def longest_subarray_with_sum(values: Sequence[int], target: int) -> Span | None:
    """Return (start, stop) of the longest subarray that sums to target.

    The stop index is excluded, like a slice. Returns None if there is none.
    On a tie, the earliest subarray wins. Negative numbers are fine.
    """
    first_seen = {0: 0}  # prefix sum -> earliest prefix index with that sum
    running = 0
    best: Span | None = None

    for stop, value in enumerate(values, start=1):
        running += value
        if (start := first_seen.get(running - target)) is not None and (
            best is None or stop - start > best[1] - best[0]
        ):
            best = (start, stop)
        first_seen.setdefault(running, stop)

    return best


def count_subarrays_with_sum(values: Iterable[int], target: int) -> int:
    """Return how many subarrays sum to target. Negative numbers are fine."""
    seen = Counter({0: 1})  # the empty prefix has sum 0
    running = 0
    count = 0

    for value in values:
        running += value
        count += seen[running - target]
        seen[running] += 1

    return count


class RegionSum:
    """Answer rectangle-sum queries on a grid in O(1) time."""

    __slots__ = ("rows", "cols", "_prefix")

    def __init__(self, grid: Sequence[Sequence[int]]) -> None:
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        if any(len(row) != cols for row in grid):
            raise ValueError("every row must have the same length")

        self.rows, self.cols = rows, cols
        self._prefix = [[0] * (cols + 1)]
        for row in grid:
            # Each prefix row is the one above it, plus this row's running totals.
            running = accumulate(row, initial=0)
            self._prefix.append(
                [above + here for above, here in zip(self._prefix[-1], running, strict=True)]
            )

    def sum_region(
        self, row_start: int, row_stop: int, col_start: int, col_stop: int
    ) -> int:
        """Return the sum of grid[row_start:row_stop][col_start:col_stop]."""
        if not (0 <= row_start <= row_stop <= self.rows):
            raise ValueError(f"need 0 <= row_start <= row_stop <= {self.rows}")
        if not (0 <= col_start <= col_stop <= self.cols):
            raise ValueError(f"need 0 <= col_start <= col_stop <= {self.cols}")
        p = self._prefix
        return (
            p[row_stop][col_stop]
            - p[row_start][col_stop]
            - p[row_stop][col_start]
            + p[row_start][col_start]
        )
