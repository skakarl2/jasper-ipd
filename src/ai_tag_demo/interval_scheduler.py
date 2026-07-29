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

    # Human refactor: iterate forward, comparing the take-vs-skip choice explicitly.
    for idx in range(1, n):
        predecessor = _latest_non_conflicting(sorted_ivs, idx)
        best_with = sorted_ivs[idx].weight
        if predecessor >= 0:
            best_with += dp[predecessor]
        best_without = dp[idx - 1]
        dp[idx] = best_with if best_with >= best_without else best_without

    # Human refactor: walk the dp table backwards to reconstruct the picks.
    chosen = []
    idx = n - 1
    while idx >= 0:
        predecessor = _latest_non_conflicting(sorted_ivs, idx)
        prior = dp[predecessor] if predecessor >= 0 else 0.0
        keep = sorted_ivs[idx].weight + prior
        if idx == 0 or keep >= dp[idx - 1]:
            chosen.append(sorted_ivs[idx])
            idx = predecessor
        else:
            idx -= 1

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
