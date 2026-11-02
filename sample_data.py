"""Make a small, repeatable request log to run the prefix sum tools on."""

import random
from dataclasses import dataclass

ENDPOINTS = ["/home", "/search", "/cart", "/checkout", "/login", "/api/items"]


@dataclass(frozen=True, slots=True)
class Request:
    """One line of the request log."""

    timestamp: float  # seconds since the log started
    user: int
    endpoint: str
    status: int


def make_requests(minutes: int = 240, seed: int = 42) -> list[Request]:
    """Return a fake request log, sorted by timestamp."""
    rng = random.Random(seed)
    requests: list[Request] = []

    for minute in range(minutes):
        rate = 90 if 100 <= minute < 108 else 20
        error_chance = 0.35 if 150 <= minute < 160 else 0.02

        for _ in range(rng.randint(rate - 5, rate + 5)):
            requests.append(
                Request(
                    timestamp=minute * 60 + rng.random() * 60,
                    user=rng.randint(1, 400),
                    endpoint=rng.choice(ENDPOINTS),
                    status=500 if rng.random() < error_chance else 200,
                )
            )

    requests.sort(key=lambda request: request.timestamp)
    return requests


def per_minute(requests: list[Request], minutes: int = 240) -> tuple[list[int], list[int]]:
    """Return (requests per minute, errors per minute) as two lists."""
    totals = [0] * minutes
    errors = [0] * minutes
    for request in requests:
        minute = int(request.timestamp // 60)
        totals[minute] += 1
        if request.status >= 500:
            errors[minute] += 1
    return totals, errors


def endpoint_grid(
    requests: list[Request], minutes: int = 240, bucket: int = 60
) -> list[list[int]]:
    """Return a grid of request counts: one row per endpoint, one column per hour."""
    columns = minutes // bucket
    grid = [[0] * columns for _ in ENDPOINTS]
    for request in requests:
        row = ENDPOINTS.index(request.endpoint)
        grid[row][int(request.timestamp // 60) // bucket] += 1
    return grid


def make_net_changes(minutes: int = 240, seed: int = 7) -> list[int]:
    """Return net user change per minute (signups minus cancellations).

    Unlike request counts, these numbers can be negative.
    """
    rng = random.Random(seed)
    return [rng.randint(-6, 8) for _ in range(minutes)]
