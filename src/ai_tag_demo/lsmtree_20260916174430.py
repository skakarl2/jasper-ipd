"""Log-Structured Merge Tree implementation.

A simplified LSM tree supporting put, get, delete (via tombstones),
automatic memtable flushing, compaction of sorted runs, and range scans.
"""

import bisect
import itertools
from typing import Any, Generator, Optional

_TOMBSTONE = object()


class SortedRun:
    """An immutable, sorted sequence of key-value pairs flushed from the memtable.

    Entries are stored as a list of (key, value) tuples in ascending key order.
    Tombstone markers indicate deleted keys and are preserved until compaction
    eliminates them.
    """

    def __init__(self, entries: list[tuple[str, Any]]) -> None:
        self._entries = entries
        self._keys = [k for k, _ in entries]

    def get(self, key: str) -> tuple[bool, Any]:
        """Binary-search for *key* and return (found, value).

        Returns (True, value) if the key exists in this run (value may be
        _TOMBSTONE), or (False, None) if the key is absent.
        """
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            return True, self._entries[idx][1]
        return False, None

    def __iter__(self):
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def range_iter(self, start: Optional[str], end: Optional[str]) -> Generator[tuple[str, Any], None, None]:
        """Yield (key, value) pairs where start <= key < end.

        Either bound may be None to indicate an open-ended range.
        """
        lo = bisect.bisect_left(self._keys, start) if start is not None else 0
        hi = bisect.bisect_left(self._keys, end) if end is not None else len(self._keys)
        for i in range(lo, hi):
            yield self._entries[i]


def _merge_iterators(iterators: list[Generator[tuple[str, Any], None, None]]) -> Generator[tuple[str, Any], None, None]:
    """Merge multiple sorted iterators, keeping only the freshest value per key.

    Iterators earlier in the list are considered newer. When duplicate keys
    appear, the value from the newest iterator wins and older duplicates are
    discarded. This is the core merge logic used by both compaction and range
    scans.
    """
    tagged = []
    for priority, it in enumerate(iterators):
        tagged.append(((priority, it), None))

    heap_items: list[tuple[str, int, Any, Generator]] = []
    for (priority, it), _ in tagged:
        try:
            key, val = next(it)
            heap_items.append((key, priority, val, it))
        except StopIteration:
            pass

    import heapq
    heapq.heapify(heap_items)

    while heap_items:
        smallest_key = heap_items[0][0]
        candidates: list[tuple[int, Any]] = []

        while heap_items and heap_items[0][0] == smallest_key:
            key, priority, val, it = heapq.heappop(heap_items)
            candidates.append((priority, val))
            try:
                next_key, next_val = next(it)
                heapq.heappush(heap_items, (next_key, priority, next_val, it))
            except StopIteration:
                pass

        candidates.sort()
        winner_val = candidates[0][1]
        yield smallest_key, winner_val


class LSMTree:
    """A log-structured merge tree providing fast writes with sorted-run storage.

    Writes go into an in-memory sorted buffer (the memtable). When the memtable
    reaches *memtable_threshold* entries it is flushed to a new immutable
    SortedRun. Reads check the memtable first, then probe sorted runs from
    newest to oldest, returning the first match found.

    Deletes insert a tombstone marker so that older values in deeper runs are
    masked. Compaction merges all sorted runs into a single run, dropping
    tombstones to reclaim space.
    """

    def __init__(self, memtable_threshold: int = 4) -> None:
        self._memtable: dict[str, Any] = {}
        self._runs: list[SortedRun] = []
        self._memtable_threshold = memtable_threshold
        self._write_sequence = 0

    @property
    def run_count(self) -> int:
        """Number of on-disk sorted runs (excludes the in-memory memtable)."""
        return len(self._runs)

    @property
    def memtable_size(self) -> int:
        """Number of entries currently buffered in the memtable."""
        return len(self._memtable)

    def put(self, key: str, value: Any) -> None:
        """Insert or update *key* with *value*.

        If the memtable exceeds the configured threshold after this write,
        it is automatically flushed to a new sorted run.
        """
        self._memtable[key] = value
        self._write_sequence += 1
        if len(self._memtable) >= self._memtable_threshold:
            self._flush()

    def get(self, key: str) -> Optional[Any]:
        """Return the value associated with *key*, or None if not found.

        The memtable is checked first, followed by sorted runs from newest to
        oldest. If a tombstone is encountered the key is treated as deleted
        and None is returned immediately without searching deeper runs.
        """
        if key in self._memtable:
            val = self._memtable[key]
            return None if val is _TOMBSTONE else val

        for run in reversed(self._runs):
            found, val = run.get(key)
            if found:
                return None if val is _TOMBSTONE else val

        return None

    def delete(self, key: str) -> None:
        """Mark *key* as deleted by inserting a tombstone.

        The tombstone masks any older values in deeper sorted runs. The key
        will read as None until a new value is written or compaction drops
        the tombstone.
        """
        self.put(key, _TOMBSTONE)

    def _flush(self) -> None:
        """Convert the current memtable into an immutable SortedRun.

        Entries are sorted by key and appended as the newest run. The
        memtable is then cleared for new writes.
        """
        if not self._memtable:
            return
        entries = sorted(self._memtable.items())
        self._runs.append(SortedRun(entries))
        self._memtable.clear()

    def compact(self) -> int:
        """Merge all sorted runs and the memtable into a single sorted run.

        Tombstones are dropped during compaction since there are no older
        runs left to mask. Returns the number of live entries after
        compaction.
        """
        self._flush()
        if not self._runs:
            return 0

        iterators = [iter(run) for run in reversed(self._runs)]
        merged_entries = [
            (k, v) for k, v in _merge_iterators(iterators) if v is not _TOMBSTONE
        ]

        self._runs.clear()
        if merged_entries:
            self._runs.append(SortedRun(merged_entries))
        return len(merged_entries)

    def range_scan(self, start: Optional[str] = None, end: Optional[str] = None) -> Generator[tuple[str, Any], None, None]:
        """Yield (key, value) pairs for all live keys where start <= key < end.

        Merges the memtable and all sorted runs, resolving duplicates by
        recency (memtable wins over newer runs, which win over older runs).
        Tombstoned keys are silently skipped. Either bound may be None for
        an open-ended scan.
        """
        sources: list[Generator[tuple[str, Any], None, None]] = []

        memtable_entries = sorted(self._memtable.items())
        filtered_mem = (
            (k, v)
            for k, v in memtable_entries
            if (start is None or k >= start) and (end is None or k < end)
        )
        sources.append(filtered_mem)

        for run in reversed(self._runs):
            sources.append(run.range_iter(start, end))

        for key, val in _merge_iterators(sources):
            if val is not _TOMBSTONE:
                yield key, val

    def bloom_hint(self, key: str) -> bool:
        """Return a cheap membership hint for *key*.

        Checks the memtable and every sorted run. A return value of True
        means the key *may* exist (it could be a tombstone); False means it
        is definitely absent. This mirrors the contract of a Bloom filter:
        no false negatives, possible false positives.
        """
        if key in self._memtable:
            return True
        for run in reversed(self._runs):
            found, _ = run.get(key)
            if found:
                return True
        return False

    def stats(self) -> dict[str, Any]:
        """Return diagnostic counters for the tree's internal state."""
        tombstone_count = sum(
            1 for v in self._memtable.values() if v is _TOMBSTONE
        ) + sum(
            1 for run in self._runs for _, v in run if v is _TOMBSTONE
        )
        return {
            "memtable_size": len(self._memtable),
            "run_count": len(self._runs),
            "tombstone_count": tombstone_count,
            "total_run_entries": sum(len(r) for r in self._runs),
            "write_sequence": self._write_sequence,
            "memtable_threshold": self._memtable_threshold,
        }


if __name__ == "__main__":
    print("=== LSM Tree Demo ===\n")

    tree = LSMTree(memtable_threshold=4)

    print("--- Inserting key-value pairs ---")
    data = [
        ("user:alice", "admin"),
        ("user:bob", "editor"),
        ("user:carol", "viewer"),
        ("config:theme", "dark"),
        ("config:lang", "en"),
        ("user:dave", "editor"),
        ("metric:cpu", "72.5"),
        ("metric:mem", "61.3"),
        ("user:eve", "viewer"),
        ("config:tz", "UTC"),
    ]
    for key, value in data:
        tree.put(key, value)
        print(f"  put({key!r}, {value!r})")

    print(f"\nStats after inserts: {tree.stats()}")

    print("\n--- Point reads ---")
    for probe in ["user:alice", "user:carol", "config:theme", "metric:cpu", "nonexistent"]:
        result = tree.get(probe)
        print(f"  get({probe!r}) = {result!r}")

    print("\n--- Deleting keys ---")
    tree.delete("user:bob")
    tree.delete("config:theme")
    print("  Deleted user:bob and config:theme")
    print(f"  get('user:bob')     = {tree.get('user:bob')!r}")
    print(f"  get('config:theme') = {tree.get('config:theme')!r}")

    print("\n--- Overwriting a key ---")
    tree.put("user:alice", "superadmin")
    print(f"  put('user:alice', 'superadmin')")
    print(f"  get('user:alice') = {tree.get('user:alice')!r}")

    print(f"\nStats before compaction: {tree.stats()}")

    print("\n--- Range scan: all user:* keys ---")
    for key, val in tree.range_scan("user:", "user:\xff"):
        print(f"  {key} => {val}")

    print("\n--- Range scan: config:* keys ---")
    for key, val in tree.range_scan("config:", "config:\xff"):
        print(f"  {key} => {val}")

    print("\n--- Full range scan (all keys) ---")
    for key, val in tree.range_scan():
        print(f"  {key} => {val}")

    print("\n--- Compaction ---")
    live_count = tree.compact()
    print(f"  Live entries after compaction: {live_count}")
    print(f"  Stats after compaction: {tree.stats()}")

    print("\n--- Post-compaction reads ---")
    print(f"  get('user:alice') = {tree.get('user:alice')!r}  (overwritten)")
    print(f"  get('user:bob')   = {tree.get('user:bob')!r}  (was deleted)")
    print(f"  get('user:dave')  = {tree.get('user:dave')!r}")
    print(f"  get('metric:mem') = {tree.get('metric:mem')!r}")

    print("\n--- Post-compaction full scan ---")
    for key, val in tree.range_scan():
        print(f"  {key} => {val}")

    print("\nDone.")
