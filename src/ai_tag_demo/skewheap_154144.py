"""
Skew Heap — a self-adjusting leftist heap.

A skew heap is a heap-ordered binary tree that maintains balance
probabilistically by unconditionally swapping children after every
merge step.  This gives O(log n) amortized complexity for merge,
push, and pop_min without storing any rank or balance metadata.

Reference: Sleator & Tarjan, "Self-Adjusting Heaps", SIAM J. Computing, 1986.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Iterable, Iterator, Optional


@dataclasses.dataclass(slots=True)
class _Node:
    """Internal node carrying a key and optional satellite data."""

    key: float
    value: Any
    left: Optional[_Node] = None
    right: Optional[_Node] = None


def _merge_nodes(a: Optional[_Node], b: Optional[_Node]) -> Optional[_Node]:
    """Merge two skew-heap subtrees rooted at *a* and *b*.

    The merge follows the right spine of each tree, always choosing the
    smaller root, then unconditionally swaps the left and right children
    of every visited node on the way back up.  This swap is what
    distinguishes a skew heap from a plain leftist heap and is the
    source of its self-adjusting property.

    Returns the root of the merged tree.
    """
    if a is None:
        return b
    if b is None:
        return a

    if a.key > b.key:
        a, b = b, a

    a.right = _merge_nodes(a.right, b)

    a.left, a.right = a.right, a.left

    return a


class SkewHeap:
    """A min-oriented self-adjusting skew heap.

    Supports the standard priority-queue interface plus efficient
    ``merge`` of two heaps and a ``heapify`` classmethod for bulk
    construction.

    All mutating operations (push, pop_min, merge) run in O(log n)
    amortized time.  ``peek_min`` and ``__len__`` are O(1).

    Example
    -------
    >>> h = SkewHeap()
    >>> for k in [5, 3, 8, 1, 4]:
    ...     h.push(k)
    >>> [h.pop_min() for _ in range(len(h))]
    [(1, None), (3, None), (4, None), (5, None), (8, None)]
    """

    __slots__ = ("_root", "_size")

    def __init__(self) -> None:
        self._root: Optional[_Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __repr__(self) -> str:
        return f"SkewHeap(size={self._size})"

    def __iter__(self) -> Iterator[tuple[float, Any]]:
        """Yield (key, value) pairs in ascending key order.

        This is a destructive iteration — it drains the heap via
        repeated ``pop_min`` calls.  Use it when you want a sorted
        traversal and no longer need the heap afterwards.
        """
        while self._root is not None:
            yield self.pop_min()

    def push(self, key: float, value: Any = None) -> None:
        """Insert a new element with the given *key* and optional *value*.

        Internally this creates a one-node heap and merges it with the
        existing tree, preserving the heap-order invariant via the
        standard skew-heap merge.

        Amortized time: O(log n).
        """
        singleton = _Node(key=key, value=value)
        self._root = _merge_nodes(self._root, singleton)
        self._size += 1

    def pop_min(self) -> tuple[float, Any]:
        """Remove and return the (key, value) pair with the smallest key.

        Raises ``IndexError`` if the heap is empty.

        The minimum is always at the root.  Removing it leaves two
        subtrees that are merged together to form the new heap.

        Amortized time: O(log n).
        """
        if self._root is None:
            raise IndexError("pop from an empty SkewHeap")
        root = self._root
        self._root = _merge_nodes(root.left, root.right)
        self._size -= 1
        return (root.key, root.value)

    def peek_min(self) -> tuple[float, Any]:
        """Return the (key, value) pair with the smallest key without removal.

        Raises ``IndexError`` if the heap is empty.

        Worst-case time: O(1).
        """
        if self._root is None:
            raise IndexError("peek at an empty SkewHeap")
        return (self._root.key, self._root.value)

    def merge(self, other: SkewHeap) -> None:
        """Destructively merge *other* into this heap.

        After the call, *other* is empty and all its elements live in
        ``self``.  This is the fundamental operation of the skew heap
        — both ``push`` and ``pop_min`` are implemented in terms of it.

        Amortized time: O(log(n + m)) where n and m are the sizes of
        the two heaps.
        """
        self._root = _merge_nodes(self._root, other._root)
        self._size += other._size
        other._root = None
        other._size = 0

    @classmethod
    def heapify(cls, items: Iterable[tuple[float, Any] | float]) -> SkewHeap:
        """Build a ``SkewHeap`` from an iterable of keys or (key, value) pairs.

        Each element may be either a bare numeric key (in which case
        ``value`` defaults to ``None``) or a ``(key, value)`` tuple.

        Rather than inserting one by one — which would give O(n log n)
        — this uses the tournament-style bottom-up pairing strategy:
        wrap each element in a singleton heap, then pair-merge adjacent
        heaps repeatedly until one remains.  This runs in O(n) amortized
        time by the same potential argument used for leftist heaps.
        """
        singletons: list[_Node] = []
        for item in items:
            if isinstance(item, (int, float)):
                singletons.append(_Node(key=item, value=None))
            else:
                k, v = item
                singletons.append(_Node(key=k, value=v))

        if not singletons:
            return cls()

        while len(singletons) > 1:
            next_round: list[_Node] = []
            idx = 0
            while idx + 1 < len(singletons):
                merged = _merge_nodes(singletons[idx], singletons[idx + 1])
                next_round.append(merged)  # type: ignore[arg-type]
                idx += 2
            if idx < len(singletons):
                next_round.append(singletons[idx])
            singletons = next_round

        heap = cls()
        heap._root = singletons[0]
        heap._size = _count_nodes(singletons[0])
        return heap


def _count_nodes(node: Optional[_Node]) -> int:
    """Count the number of nodes reachable from *node*."""
    if node is None:
        return 0
    return 1 + _count_nodes(node.left) + _count_nodes(node.right)


def merge_all(heaps: Iterable[SkewHeap]) -> SkewHeap:
    """Fold an iterable of ``SkewHeap`` instances into one heap.

    Uses the same bottom-up pairing strategy as ``heapify`` to avoid
    the pathological case of merging a long sequence left-to-right,
    which would repeatedly traverse the largest accumulated tree.

    Every input heap is consumed (emptied) by this operation.

    Returns a fresh ``SkewHeap`` containing all elements.
    """
    pending: list[SkewHeap] = [h for h in heaps if h]
    if not pending:
        return SkewHeap()

    while len(pending) > 1:
        next_round: list[SkewHeap] = []
        idx = 0
        while idx + 1 < len(pending):
            pending[idx].merge(pending[idx + 1])
            next_round.append(pending[idx])
            idx += 2
        if idx < len(pending):
            next_round.append(pending[idx])
        pending = next_round

    return pending[0]


if __name__ == "__main__":
    import random
    import textwrap

    print(textwrap.dedent("""\
        ╔══════════════════════════════════════════════════════╗
        ║   Skew Heap Demo — Priority-Queue Task Scheduler    ║
        ╚══════════════════════════════════════════════════════╝
    """))

    # ------------------------------------------------------------------
    # Scenario: a simple priority-queue driven task scheduler.
    #
    # Tasks arrive with a priority (lower = more urgent) and a name.
    # We simulate three independent work queues that are later merged
    # into a single dispatcher queue, which then drains tasks in
    # priority order.
    # ------------------------------------------------------------------

    random.seed(42)

    task_pools: dict[str, list[tuple[int, str]]] = {
        "network": [
            (2, "Retry failed DNS resolution"),
            (5, "Flush connection pool"),
            (1, "Handle incoming TLS handshake"),
            (8, "Log slow-query metrics"),
            (3, "Send heartbeat to peers"),
        ],
        "disk_io": [
            (4, "Compact SSTable segment"),
            (1, "Fsync WAL buffer"),
            (6, "Reclaim tombstoned pages"),
            (2, "Flush dirty page cache"),
            (9, "Schedule background defrag"),
        ],
        "compute": [
            (3, "Run GC sweep on gen-2 heap"),
            (7, "Recompile hot JIT traces"),
            (1, "Service interrupt from device 0x3F"),
            (5, "Re-balance worker thread pool"),
            (10, "Profile memory allocator fragmentation"),
        ],
    }

    queue_heaps: list[SkewHeap] = []
    for queue_name, tasks in task_pools.items():
        heap = SkewHeap.heapify(tasks)
        print(f"  [{queue_name:>8}] built heap with {len(heap)} tasks  "
              f"(min priority = {heap.peek_min()[0]})")
        queue_heaps.append(heap)

    print()

    merged_queue = merge_all(queue_heaps)
    print(f"  Merged all queues → {len(merged_queue)} tasks in dispatcher\n")

    # Simulate arrival of late-breaking high-priority tasks
    late_arrivals = [
        (0, "CRITICAL: certificate expiry in 60 s"),
        (2, "Rebalance shard after node departure"),
    ]
    for pri, desc in late_arrivals:
        merged_queue.push(pri, desc)
        print(f"  ⚡ Late arrival pushed: pri={pri}  {desc}")

    print(f"\n  Dispatcher queue now has {len(merged_queue)} tasks.\n")
    print("  Draining in priority order:\n")

    step = 1
    while merged_queue:
        priority, description = merged_queue.pop_min()
        print(f"    {step:>2}. [pri {priority:>2}]  {description}")
        step += 1

    print(f"\n  All {step - 1} tasks dispatched.  Heap is empty: "
          f"{len(merged_queue) == 0}\n")

    # ------------------------------------------------------------------
    # Quick correctness smoke-test: heapify → sorted drain must produce
    # a non-decreasing key sequence.
    # ------------------------------------------------------------------
    random_keys = [random.randint(0, 999) for _ in range(200)]
    h = SkewHeap.heapify(random_keys)
    sorted_output = [h.pop_min()[0] for _ in range(len(h))]
    assert sorted_output == sorted(random_keys), "Heap-sort invariant violated!"
    print("  ✓ Smoke test passed: 200-element heapify → sorted drain OK.")
