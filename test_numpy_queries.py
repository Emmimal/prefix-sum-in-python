import numpy as np

from numpy_queries import build_prefix_np, sum_ranges
from prefix_sum import build_prefix


def test_numpy_prefix_matches_the_pure_python_version() -> None:
    values = [3, 1, 4, 1, 5, 9, 2, 6]
    assert build_prefix_np(np.array(values)).tolist() == build_prefix(values)


def test_batch_queries_match_one_by_one() -> None:
    values = np.array([3, 1, 4, 1, 5, 9, 2, 6])
    prefix = build_prefix_np(values)
    starts, stops = np.array([2, 0, 3]), np.array([6, 8, 3])
    assert sum_ranges(prefix, starts, stops).tolist() == [19, 31, 0]
