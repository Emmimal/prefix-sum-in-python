# Prefix Sum in Python

Companion code for the EmiTechLogic tutorial **Prefix Sum in Python: Range Queries Made Simple**.
It is part of the *Data Structures & Algorithms with Python* series and builds on the
[Sliding Window in Python](https://emitechlogic.com/sliding-window-technique-in-python/) project.

Every fast function is tested against a slow brute-force version on random inputs.

## Project structure

```text
prefix-sum-in-python/
├── .github/
│   └── workflows/
│       └── tests.yml          # runs the tests on Python 3.12, 3.13 and 3.14
├── prefix_sum.py              # the toolkit: RangeSum, subarray sums, RegionSum (2D)
├── numpy_queries.py           # prefix sums and batch queries with NumPy
├── shortcuts.py               # one-liners with zip, pairwise, bisect and math.comb
├── brute_force.py             # slow, obviously correct versions (test oracles)
├── pitfalls.py                # deliberately buggy versions used in tests
├── practice.py                # solutions to the practice problems
├── sample_data.py             # repeatable fake request log
├── benchmark.py               # timing reports
├── demo.py                    # report on the request log
├── test_prefix_sum.py
├── test_numpy_queries.py
├── test_shortcuts.py
├── test_pitfalls.py
├── test_practice.py
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## What is inside

| File | What it does |
|---|---|
| `prefix_sum.py` | `build_prefix`, `RangeSum`, `longest_subarray_with_sum`, `count_subarrays_with_sum`, `RegionSum` (2D) |
| `numpy_queries.py` | Prefix sums and batch range queries with NumPy |
| `shortcuts.py` | One-liners with `zip`, `pairwise`, `bisect` and `math.comb` |
| `brute_force.py` | Slow, obviously correct versions used as test oracles |
| `pitfalls.py` | Deliberately buggy versions that the tests use to show common mistakes |
| `practice.py` | Solutions to the three practice problems |
| `sample_data.py` | Repeatable fake request log (same as the sliding window project) |
| `benchmark.py` | Timing reports |
| `demo.py` | Report on the request log |

## Requirements

Python 3.12 or later. Tested on Python 3.12, 3.13 and 3.14. NumPy is used by `numpy_queries.py` and `benchmark.py`.

## Run it

```console
$ python -m venv venv
$ source venv/bin/activate      # Windows: venv\Scripts\activate
(venv) $ python -m pip install -r requirements.txt
(venv) $ python -m pytest
(venv) $ python demo.py
(venv) $ python benchmark.py
```

With [uv](https://docs.astral.sh/uv/), no manual environment is needed:

```console
$ uv run --with pytest --with numpy python -m pytest
$ uv run --with numpy python demo.py
```

## Expected `demo.py` output

The log is seeded, so this output is repeatable:

```text
5,375 requests over 240 minutes
Hour 1: 1,227 requests, 25 errors
Hour 2: 1,788 requests, 39 errors
Hour 3: 1,194 requests, 77 errors
Hour 4: 1,166 requests, 21 errors
Error rate during the incident (minutes 150-159): 30.5%
Error rate during the spike (minutes 100-107): 1.7%
Net user change, minutes 0-239: 118
Stretches with a net change of exactly 25: 196
Longest stretch with a net change of 0: 109 minutes, from minute 1
/cart and /checkout requests in hours 2 and 3: 1037
```

Timings from `benchmark.py` depend on your machine.

## Quick example

```python
from prefix_sum import RangeSum, count_subarrays_with_sum

queries = RangeSum([3, 1, 4, 1, 5, 9, 2, 6])
queries.sum_range(2, 6)                      # 19, the range excludes index 6

count_subarrays_with_sum([1, -1, 1], 1)      # 3, works with negative numbers
```

## License

MIT
