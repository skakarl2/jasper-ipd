"""Weighted interval scheduling optimizer using dynamic programming."""

from bisect import bisect_right
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Interval:
    """A weighted interval defined by start time, end time, and value."""
    start: float
    end: float
    weight: float


def _latest_non_conflicting(intervals: list[Interval], i: int) -> int:
    """Return the index of the latest interval that ends before intervals[i] starts.

    Uses binary search on the sorted-by-end list for O(log n) lookup.
    Returns -1 if no compatible predecessor exists.
    """
    target = intervals[i].start
    ends = [iv.end for iv in intervals[:i]]
    j = bisect_right(ends, target) - 1
    return j


def schedule_max_weight(intervals: list[Interval]) -> tuple[float, list[Interval]]:
    """Find a maximum-weight subset of non-overlapping intervals.

    Sorts intervals by end time, then applies DP recurrence:
        dp[i] = max(weight_i + dp[latest_non_conflicting(i)], dp[i-1])

    Returns (total_weight, chosen_intervals).
    """
    if not intervals:
        return 0.0, []

    sorted_ivs = sorted(intervals, key=lambda iv: iv.end)
    n = len(sorted_ivs)

    # dp[i] stores the max weight achievable using intervals 0..i
    dp = [0.0] * n
    dp[0] = sorted_ivs[0].weight

    for i in range(1, n):
        include = sorted_ivs[i].weight
        j = _latest_non_conflicting(sorted_ivs, i)
        if j >= 0:
            include += dp[j]
        dp[i] = max(include, dp[i - 1])

    # Backtrack to recover the chosen intervals
    chosen = []
    i = n - 1
    while i >= 0:
        j = _latest_non_conflicting(sorted_ivs, i)
        include = sorted_ivs[i].weight + (dp[j] if j >= 0 else 0)
        if i == 0 or include >= dp[i - 1]:
            chosen.append(sorted_ivs[i])
            i = j
        else:
            i -= 1

    chosen.reverse()
    return dp[-1], chosen


if __name__ == "__main__":
    sample = [
        Interval(start=1, end=4, weight=3),
        Interval(start=3, end=5, weight=4),
        Interval(start=0, end=6, weight=7),
        Interval(start=5, end=7, weight=2),
        Interval(start=6, end=9, weight=5),
        Interval(start=8, end=10, weight=1),
    ]

    total, chosen = schedule_max_weight(sample)

    print("All intervals:")
    for iv in sample:
        print(f"  [{iv.start:g}, {iv.end:g})  weight={iv.weight:g}")

    print(f"\nOptimal non-overlapping subset (total weight = {total:g}):")
    for iv in chosen:
        print(f"  [{iv.start:g}, {iv.end:g})  weight={iv.weight:g}")
