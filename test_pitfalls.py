from brute_force import count_subarrays_brute
from pitfalls import (
    count_subarrays_no_seed,
    count_subarrays_sliding_window,
    sum_range_inclusive_mixup,
)
from prefix_sum import RangeSum, count_subarrays_with_sum


def test_inclusive_mixup_leaves_out_the_last_item() -> None:
    values = [3, 1, 4, 1, 5]
    assert sum(values[1:4]) == 6  # items at index 1, 2 and 3
    assert RangeSum(values).sum_range(1, 4) == 6
    assert sum_range_inclusive_mixup(values, 1, 3) == 5  # missed the item at index 3


def test_missing_seed_skips_subarrays_that_start_at_index_zero() -> None:
    values = [3, 4, 7]
    assert count_subarrays_brute(values, 7) == 2  # [3, 4] and [7]
    assert count_subarrays_with_sum(values, 7) == 2
    assert count_subarrays_no_seed(values, 7) == 1


def test_sliding_window_count_breaks_on_negative_numbers() -> None:
    values = [1, -1, 1]
    assert count_subarrays_brute(values, 1) == 3
    assert count_subarrays_with_sum(values, 1) == 3
    assert count_subarrays_sliding_window(values, 1) == 2


def test_sliding_window_count_is_fine_when_numbers_are_all_positive() -> None:
    values = [1, 2, 3, 4, 1, 2]
    assert count_subarrays_sliding_window(values, 3) == count_subarrays_brute(values, 3)
