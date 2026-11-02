import pytest

from practice import longest_balanced_run, pivot_index, subarrays_divisible_by_k


def test_pivot_index() -> None:
    assert pivot_index([1, 7, 3, 6, 5, 6]) == 3
    assert pivot_index([1, 2, 3]) == -1
    assert pivot_index([2, 1, -1]) == 0


def test_subarrays_divisible_by_k() -> None:
    assert subarrays_divisible_by_k([4, 5, 0, -2, -3, 1], 5) == 7
    with pytest.raises(ValueError):
        subarrays_divisible_by_k([1], 0)


def test_longest_balanced_run() -> None:
    assert longest_balanced_run([0, 1, 0]) == 2
    assert longest_balanced_run([0, 1, 1, 0, 1, 1, 1, 0]) == 4
    assert longest_balanced_run([1, 1, 1]) == 0
