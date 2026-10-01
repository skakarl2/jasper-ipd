"""Merge overlapping integer intervals.

A small, dependency-free module providing an :class:`Interval` value type and
:func:`merge_intervals`, which collapses a collection of (possibly unsorted,
possibly overlapping) closed integer intervals into the minimal set of
non-overlapping intervals covering the same points.

Intervals are treated as closed on both ends, so ``(1, 3)`` and ``(3, 5)``
are considered overlapping and merge into ``(1, 5)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple, Union


@dataclass(frozen=True)
class Interval:
    """A closed integer interval ``[start, end]``."""

    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"start ({self.start}) must be <= end ({self.end})")

    def overlaps(self, other: "Interval") -> bool:
        """Return True if this interval touches or overlaps ``other``."""
        return self.start <= other.end and other.start <= self.end

    def as_tuple(self) -> Tuple[int, int]:
        """Return the interval as a plain ``(start, end)`` tuple."""
        return (self.start, self.end)


IntervalLike = Union[Interval, Sequence[int]]


def _coerce(item: IntervalLike) -> Interval:
    """Normalize an ``Interval`` or a 2-element sequence into an ``Interval``."""
    if isinstance(item, Interval):
        return item
    start, end = item  # raises ValueError for wrong-length sequences
    return Interval(int(start), int(end))


def merge_intervals(intervals: Iterable[IntervalLike]) -> List[Interval]:
    """Sort and merge overlapping or adjacent intervals.

    Args:
        intervals: Any iterable of :class:`Interval` instances or
            ``(start, end)`` pairs.

    Returns:
        A new list of non-overlapping :class:`Interval` objects sorted by
        ``start``. The input is not modified.

    Raises:
        ValueError: If any interval has ``start > end`` or is not a pair.
    """
    items = [_coerce(item) for item in intervals]
    if not items:
        return []

    items.sort(key=lambda iv: (iv.start, iv.end))

    merged: List[Interval] = [items[0]]
    for current in items[1:]:
        last = merged[-1]
        if current.start <= last.end:
            if current.end > last.end:
                merged[-1] = Interval(last.start, current.end)
        else:
            merged.append(current)

    return merged


if __name__ == "__main__":
    sample = [(1, 3), (2, 6), (8, 10), (15, 18)]
    result = merge_intervals(sample)

    print(f"input:  {sample}")
    print(f"merged: {[iv.as_tuple() for iv in result]}")
