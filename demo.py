"""Run the prefix sum tools on a fake request log and print a report."""

from prefix_sum import (
    RangeSum,
    RegionSum,
    count_subarrays_with_sum,
    longest_subarray_with_sum,
)
from sample_data import ENDPOINTS, endpoint_grid, make_net_changes, make_requests, per_minute

MINUTES = 240


def main() -> None:
    requests = make_requests(MINUTES)
    totals, errors = per_minute(requests, MINUTES)
    traffic = RangeSum(totals)
    failures = RangeSum(errors)
    print(f"{len(requests):,} requests over {MINUTES} minutes")

    for hour in range(MINUTES // 60):
        start, stop = hour * 60, (hour + 1) * 60
        print(f"Hour {hour + 1}: {traffic.sum_range(start, stop):,} requests, "
              f"{failures.sum_range(start, stop)} errors")

    incident = (150, 160)
    spike = (100, 108)
    rate = failures.sum_range(*incident) / traffic.sum_range(*incident)
    print(f"Error rate during the incident (minutes 150-159): {rate:.1%}")
    rate = failures.sum_range(*spike) / traffic.sum_range(*spike)
    print(f"Error rate during the spike (minutes 100-107): {rate:.1%}")

    net = make_net_changes(MINUTES)
    print(f"Net user change, minutes 0-239: {RangeSum(net).sum_range(0, MINUTES)}")
    print(f"Stretches with a net change of exactly 25: {count_subarrays_with_sum(net, 25)}")
    best = longest_subarray_with_sum(net, 0)
    if best is not None:
        start, stop = best
        print(f"Longest stretch with a net change of 0: {stop - start} minutes, from minute {start}")

    grid = endpoint_grid(requests, MINUTES)
    regions = RegionSum(grid)
    cart, checkout = ENDPOINTS.index("/cart"), ENDPOINTS.index("/checkout")
    total = regions.sum_region(cart, checkout + 1, 1, 3)
    print(f"/cart and /checkout requests in hours 2 and 3: {total}")


if __name__ == "__main__":
    main()
