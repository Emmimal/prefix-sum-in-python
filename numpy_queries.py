"""Answer many range queries at once with NumPy."""

import numpy as np


def build_prefix_np(values: np.ndarray) -> np.ndarray:
    """Return the prefix sums of `values`, starting with a 0."""
    prefix = np.zeros(len(values) + 1, dtype=np.int64)
    np.cumsum(values, out=prefix[1:])
    return prefix


def sum_ranges(prefix: np.ndarray, starts: np.ndarray, stops: np.ndarray) -> np.ndarray:
    """Return the sum of values[start:stop] for every pair, in one subtraction."""
    return prefix[stops] - prefix[starts]
