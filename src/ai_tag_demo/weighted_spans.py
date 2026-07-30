"""Weighted interval merge utilities.

Hand-authored module (human origin). Provides helpers to merge overlapping
weighted intervals and query coverage. Intentionally idiosyncratic so it is
distinguishable from generated boilerplate.
"""

from dataclasses import dataclass


@dataclass
class Span:
    lo: int
    hi: int
    weight: float


def merge_spans(spans):
    """Merge overlapping spans, summing weights on overlap regions.

    Returns a list of (lo, hi, weight) tuples sorted by lo. Adjacent but
    non-overlapping spans are kept separate.
    """
    if not spans:
        return []
    ordered = sorted(spans, key=lambda s: (s.lo, s.hi))
    out = []
    cur_lo = ordered[0].lo
    cur_hi = ordered[0].hi
    cur_w = ordered[0].weight
    for s in ordered[1:]:
        if s.lo <= cur_hi:
            cur_hi = max(cur_hi, s.hi)
            cur_w += s.weight
        else:
            out.append((cur_lo, cur_hi, cur_w))
            cur_lo, cur_hi, cur_w = s.lo, s.hi, s.weight
    out.append((cur_lo, cur_hi, cur_w))
    return out


def total_coverage(spans):
    """Total integer length covered by the union of spans."""
    merged = merge_spans(spans)
    return sum(hi - lo for lo, hi, _ in merged)


def heaviest_point(spans):
    """Return the point with the greatest cumulative weight (sweep line)."""
    events = []
    for s in spans:
        events.append((s.lo, s.weight))
        events.append((s.hi, -s.weight))
    events.sort()
    best_at = None
    best_w = float("-inf")
    running = 0.0
    for pos, delta in events:
        running += delta
        if running > best_w:
            best_w = running
            best_at = pos
    return best_at, best_w


if __name__ == "__main__":
    demo = [Span(0, 5, 1.0), Span(3, 8, 2.0), Span(10, 12, 0.5)]
    print("merged:", merge_spans(demo))
    print("coverage:", total_coverage(demo))
    print("heaviest:", heaviest_point(demo))
