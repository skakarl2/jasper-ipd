"""
Log-Structured Merge Tree (LSM Tree) implementation.

An LSM tree optimizes write-heavy workloads by buffering writes in an in-memory
sorted structure (memtable) and periodically flushing to immutable sorted runs
on disk (simulated here as in-memory lists). Reads merge results across the
memtable and all sorted runs, respecting tombstones for deleted keys. Compaction
merges multiple sorted runs into fewer, larger ones to bound read amplification.
"""

from __future__ import annotations

import heapq
import time
from dataclasses import dataclass, field
from typing import Generator, Iterator


_TOMBSTONE = object()


@dataclass(order=True)
class _Entry:
    """A single key-value record with a monotonic sequence number for ordering.

    Newer sequence numbers win during merges. A value of ``_TOMBSTONE``
    represents a deletion marker that suppresses older values for the same key.
    """

    key: str
    seq: int = field(compare=False)
    value: object = field(compare=False)

    @property
    def is_tombstone(self) -> bool:
        return self.value is _TOMBSTONE


class _SortedRun:
    """An immutable, key-sorted sequence of entries produced by a memtable flush.

    Entries are stored in ascending key order. Within the same key, the entry
    with the highest sequence number is authoritative.
    """

    __slots__ = ("_entries",)

    def __init__(self, entries: list[_Entry]) -> None:
        self._entries = sorted(entries, key=lambda e: (e.key, -e.seq))

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[_Entry]:
        return iter(self._entries)

    def scan(self, start_key: str | None = None, end_key: str | None = None) -> Generator[_Entry, None, None]:
        """Yield entries whose keys fall within [start_key, end_key)."""
        for entry in self._entries:
            if start_key is not None and entry.key < start_key:
                continue
            if end_key is not None and entry.key >= end_key:
                break
            yield entry


class _Memtable:
    """A mutable in-memory buffer that accumulates writes before flushing.

    Internally backed by a dict keyed on the string key, storing the latest
    ``_Entry`` for each key. This gives O(1) point lookups and deduplication
    while the table is live.
    """

    def __init__(self) -> None:
        self._data: dict[str, _Entry] = {}
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def put(self, entry: _Entry) -> None:
        prev = self._data.get(entry.key)
        self._data[entry.key] = entry
        if prev is None:
            self._size += 1

    def get(self, key: str) -> _Entry | None:
        return self._data.get(key)

    def flush(self) -> _SortedRun:
        """Drain the memtable into an immutable sorted run and reset."""
        run = _SortedRun(list(self._data.values()))
        self._data.clear()
        self._size = 0
        return run

    def entries(self) -> list[_Entry]:
        return list(self._data.values())


def _merge_entry_streams(*streams: Iterator[_Entry]) -> Generator[_Entry, None, None]:
    """K-way merge of pre-sorted entry streams, emitting the newest entry per key.

    Uses a min-heap keyed on (key, -seq) so that for duplicate keys the
    highest sequence number surfaces first. Subsequent duplicates for the
    same key are skipped.
    """
    heap: list[tuple[str, int, int, _Entry]] = []
    for idx, stream in enumerate(streams):
        entry = next(stream, None)
        if entry is not None:
            heapq.heappush(heap, (entry.key, -entry.seq, idx, entry))

    iterators = list(streams)
    last_key: str | None = None

    while heap:
        key, neg_seq, idx, entry = heapq.heappop(heap)

        nxt = next(iterators[idx], None)
        if nxt is not None:
            heapq.heappush(heap, (nxt.key, -nxt.seq, idx, nxt))

        if key == last_key:
            continue
        last_key = key
        yield entry


class LSMTree:
    """A log-structured merge tree supporting put, get, delete, and range scan.

    Writes are buffered in a memtable. When the memtable reaches
    ``flush_threshold`` entries it is flushed to an immutable sorted run.
    ``compact()`` merges all sorted runs (and optionally the memtable) into a
    single run, discarding superseded entries and resolved tombstones.

    Args:
        flush_threshold: Number of unique keys in the memtable before an
            automatic flush to a sorted run.
    """

    def __init__(self, flush_threshold: int = 64) -> None:
        if flush_threshold < 1:
            raise ValueError("flush_threshold must be >= 1")
        self._flush_threshold = flush_threshold
        self._memtable = _Memtable()
        self._runs: list[_SortedRun] = []
        self._seq = 0
        self._stats = {"puts": 0, "gets": 0, "deletes": 0, "flushes": 0, "compactions": 0}

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def _maybe_flush(self) -> None:
        if len(self._memtable) >= self._flush_threshold:
            self._runs.append(self._memtable.flush())
            self._stats["flushes"] += 1

    def put(self, key: str, value: object) -> None:
        """Insert or update a key-value pair.

        If the memtable reaches the flush threshold after this write it is
        automatically flushed to a new sorted run.

        Args:
            key: The lookup key (must be a string).
            value: Any Python object to associate with the key.

        Raises:
            TypeError: If *key* is not a string.
        """
        if not isinstance(key, str):
            raise TypeError(f"key must be str, got {type(key).__name__}")
        self._memtable.put(_Entry(key=key, seq=self._next_seq(), value=value))
        self._stats["puts"] += 1
        self._maybe_flush()

    def get(self, key: str) -> object | None:
        """Retrieve the value for *key*, or ``None`` if absent or deleted.

        The memtable is checked first (most recent writes), then sorted runs
        are probed from newest to oldest. A tombstone is treated as an absent
        key.

        Args:
            key: The lookup key.

        Returns:
            The stored value, or ``None`` if the key was never written or has
            been deleted.
        """
        self._stats["gets"] += 1

        entry = self._memtable.get(key)
        if entry is not None:
            return None if entry.is_tombstone else entry.value

        for run in reversed(self._runs):
            for e in run:
                if e.key == key:
                    return None if e.is_tombstone else e.value
                if e.key > key:
                    break

        return None

    def delete(self, key: str) -> None:
        """Mark *key* as deleted by inserting a tombstone.

        The tombstone suppresses any older value for this key during reads and
        range scans. Tombstones are purged during compaction.

        Args:
            key: The key to delete.
        """
        if not isinstance(key, str):
            raise TypeError(f"key must be str, got {type(key).__name__}")
        self._memtable.put(_Entry(key=key, seq=self._next_seq(), value=_TOMBSTONE))
        self._stats["deletes"] += 1
        self._maybe_flush()

    def compact(self) -> int:
        """Merge all sorted runs and the memtable into a single sorted run.

        Entries that have been superseded by a newer write to the same key are
        discarded. Tombstones are also removed since after compaction there are
        no older runs they need to suppress.

        Returns:
            The number of live (non-tombstone) entries remaining after
            compaction.
        """
        streams: list[Iterator[_Entry]] = []

        if self._memtable.entries():
            memtable_run = _SortedRun(self._memtable.entries())
            streams.append(iter(memtable_run))

        for run in reversed(self._runs):
            streams.append(iter(run))

        merged: list[_Entry] = [e for e in _merge_entry_streams(*streams) if not e.is_tombstone]

        self._memtable = _Memtable()
        self._runs = [_SortedRun(merged)] if merged else []
        self._stats["compactions"] += 1
        return len(merged)

    def range_scan(self, start_key: str | None = None, end_key: str | None = None) -> Generator[tuple[str, object], None, None]:
        """Yield ``(key, value)`` pairs in sorted key order over [start_key, end_key).

        Merges the memtable with all sorted runs, respecting tombstones.

        Args:
            start_key: Inclusive lower bound (``None`` means the beginning).
            end_key: Exclusive upper bound (``None`` means the end).

        Yields:
            Tuples of ``(key, value)`` in ascending key order.
        """
        streams: list[Iterator[_Entry]] = []

        mem_entries = self._memtable.entries()
        if mem_entries:
            mem_run = _SortedRun(mem_entries)
            streams.append(mem_run.scan(start_key, end_key))

        for run in reversed(self._runs):
            streams.append(run.scan(start_key, end_key))

        for entry in _merge_entry_streams(*streams):
            if not entry.is_tombstone:
                yield entry.key, entry.value

    @property
    def stats(self) -> dict[str, int]:
        """Return a copy of cumulative operation statistics."""
        return dict(self._stats)

    @property
    def run_count(self) -> int:
        """Number of immutable sorted runs currently held."""
        return len(self._runs)

    def __len__(self) -> int:
        """Approximate number of entries across the memtable and all runs.

        This counts raw entries including tombstones and duplicates across
        runs; use ``compact()`` for an exact live-entry count.
        """
        total = len(self._memtable)
        for run in self._runs:
            total += len(run)
        return total

    def __repr__(self) -> str:
        return (
            f"LSMTree(flush_threshold={self._flush_threshold}, "
            f"runs={len(self._runs)}, memtable_size={len(self._memtable)}, "
            f"seq={self._seq})"
        )


def _demo() -> None:
    """Demonstrate LSM tree operations: inserts, reads, deletes, compaction."""
    tree = LSMTree(flush_threshold=4)
    print(f"Created {tree!r}\n")

    # -- Bulk inserts --
    cities = {
        "nyc": "New York City",
        "lax": "Los Angeles",
        "chi": "Chicago",
        "hou": "Houston",
        "phx": "Phoenix",
        "phi": "Philadelphia",
        "sat": "San Antonio",
        "sdg": "San Diego",
        "dal": "Dallas",
        "sjo": "San Jose",
    }
    print(f"Inserting {len(cities)} cities...")
    for code, name in cities.items():
        tree.put(code, name)
    print(f"State after inserts: {tree!r}")
    print(f"Stats: {tree.stats}\n")

    # -- Point reads --
    print("Point reads:")
    for key in ("nyc", "phx", "zzz"):
        val = tree.get(key)
        print(f"  get({key!r}) -> {val!r}")
    print()

    # -- Range scan --
    print("Range scan [d, p):")
    for k, v in tree.range_scan("d", "p"):
        print(f"  {k}: {v}")
    print()

    # -- Deletes --
    print("Deleting 'chi' and 'hou'...")
    tree.delete("chi")
    tree.delete("hou")
    print(f"  get('chi') after delete -> {tree.get('chi')!r}")
    print(f"  get('hou') after delete -> {tree.get('hou')!r}")
    print(f"  get('nyc') still alive  -> {tree.get('nyc')!r}\n")

    # -- Overwrite --
    print("Overwriting 'nyc' with new value...")
    tree.put("nyc", "NYC (updated)")
    print(f"  get('nyc') -> {tree.get('nyc')!r}\n")

    # -- Pre-compaction state --
    print(f"Pre-compaction: {tree.run_count} sorted runs, ~{len(tree)} total entries")

    # -- Compaction --
    t0 = time.perf_counter_ns()
    live = tree.compact()
    elapsed_us = (time.perf_counter_ns() - t0) / 1_000
    print(f"Compaction finished in {elapsed_us:.1f} µs")
    print(f"Post-compaction: {tree.run_count} sorted run(s), {live} live entries\n")

    # -- Full scan after compaction --
    print("Full scan after compaction:")
    for k, v in tree.range_scan():
        print(f"  {k}: {v}")
    print()

    print(f"Final stats: {tree.stats}")
    print(f"Final state: {tree!r}")


if __name__ == "__main__":
    _demo()
