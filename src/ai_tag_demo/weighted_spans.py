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


def subtract_span(spans, cut):
    """Remove the interval `cut` from every span in `spans`.

    Any span that fully contains `cut` is split into up to two pieces
    (the portions before and after the cut). Spans entirely inside the
    cut are dropped. Spans that partially overlap lose their overlapping
    portion. Weights are preserved on the surviving fragments.

    Returns a new list of Span objects; the originals are not mutated.
    """
    # Human rewrite: use a helper to classify each span against the cut.
    result = []
    for s in spans:
        no_overlap = s.hi <= cut.lo or s.lo >= cut.hi
        if no_overlap:
            result.append(Span(s.lo, s.hi, s.weight))
            continue
        left_piece = s.lo < cut.lo
        right_piece = s.hi > cut.hi
        if left_piece:
            result.append(Span(s.lo, cut.lo, s.weight))
        if right_piece:
            result.append(Span(cut.hi, s.hi, s.weight))
    return result


def weighted_gaps(spans, lo, hi):
    """Return the sub-intervals of [lo, hi) not covered by any span.

    Merges the spans first so overlaps don't produce false gaps. Each
    gap is returned as a plain (start, end) tuple, sorted by start.
    """
    if lo >= hi:
        return []
    merged = merge_spans(spans)
    covered = [(max(s_lo, lo), min(s_hi, hi))
               for s_lo, s_hi, _ in merged
               if s_lo < hi and s_hi > lo]
    covered.sort()
    gaps = []
    cursor = lo
    for c_lo, c_hi in covered:
        if c_lo > cursor:
            gaps.append((cursor, c_lo))
        cursor = max(cursor, c_hi)
    if cursor < hi:
        gaps.append((cursor, hi))
    return gaps


def intersect_spans(a, b):
    """Return overlapping regions between two span lists with combined weights.

    Uses a sweep-line over interval endpoints to find every sub-interval
    where at least one span from `a` and at least one from `b` are both
    active. The weight for each output region is the sum of all active
    weights from both lists at that point.

    Parameters
    ----------
    a, b : list of Span
        Two collections of weighted intervals.

    Returns
    -------
    list of (lo, hi, combined_weight) tuples, sorted by lo, covering
    exactly the portions of the number line where both lists contribute
    at least one span.
    """
    START, END = 0, 1

    events = []
    for s in a:
        events.append((s.lo, START, 0, s.weight))
        events.append((s.hi, END, 0, s.weight))
    for s in b:
        events.append((s.lo, START, 1, s.weight))
        events.append((s.hi, END, 1, s.weight))

    events.sort(key=lambda e: (e[0], e[1]))

    result = []
    depth = [0, 0]
    weight = [0.0, 0.0]
    prev_pos = None

    for pos, kind, side, w in events:
        if prev_pos is not None and pos > prev_pos and depth[0] > 0 and depth[1] > 0:
            combined = weight[0] + weight[1]
            if result and result[-1][1] == prev_pos and result[-1][2] == combined:
                result[-1] = (result[-1][0], pos, combined)
            else:
                result.append((prev_pos, pos, combined))

        if kind == START:
            depth[side] += 1
            weight[side] += w
        else:
            depth[side] -= 1
            weight[side] -= w

        prev_pos = pos

    return result


if __name__ == "__main__":
    demo = [Span(0, 5, 1.0), Span(3, 8, 2.0), Span(10, 12, 0.5)]
    print("merged:", merge_spans(demo))
    print("coverage:", total_coverage(demo))
    print("heaviest:", heaviest_point(demo))
