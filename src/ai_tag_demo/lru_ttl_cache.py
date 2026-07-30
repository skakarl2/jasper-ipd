"""LRU cache with per-entry TTL expiry.

Uses collections.OrderedDict for O(1) recency promotion (move_to_end)
and O(1) key lookup.  Each entry carries its own expiration timestamp
so stale data is evicted lazily on access or explicitly via evict_expired().
"""

from __future__ import annotations

import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Hashable


@dataclass
class _Entry:
    """A single cache entry pairing a value with its expiration."""

    value: Any
    expires_at: float


@dataclass
class _Stats:
    """Mutable hit/miss/eviction counters."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0


class LRUTTLCache:
    """Bounded LRU cache where every entry has an individual TTL.

    Parameters
    ----------
    capacity:
        Maximum number of live (non-expired) entries the cache may hold.
        When a ``put`` would exceed this limit the least-recently-used
        entry is evicted first.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._data: OrderedDict[Hashable, _Entry] = OrderedDict()
        self._stats = _Stats()

    # -- public API ----------------------------------------------------------

    def get(self, key: Hashable) -> Any | None:
        """Return the value for *key*, or ``None`` if missing or expired.

        A hit promotes the entry to most-recently-used.  An expired entry
        is removed lazily on access.
        """
        entry = self._data.get(key)
        if entry is None:
            self._stats.misses += 1
            return None
        if time.monotonic() >= entry.expires_at:
            del self._data[key]
            self._stats.evictions += 1
            self._stats.misses += 1
            return None
        self._data.move_to_end(key)
        self._stats.hits += 1
        return entry.value

    def put(self, key: Hashable, value: Any, ttl: float) -> None:
        """Insert or update *key* with *value* and a per-entry *ttl* in seconds.

        If the key already exists its value, TTL, and recency are refreshed.
        If the cache is at capacity the least-recently-used entry is evicted.
        """
        if ttl <= 0:
            raise ValueError("ttl must be > 0")

        now = time.monotonic()

        if key in self._data:
            self._data[key].value = value
            self._data[key].expires_at = now + ttl
            self._data.move_to_end(key)
            return

        if len(self._data) >= self._capacity:
            self._data.popitem(last=False)
            self._stats.evictions += 1

        self._data[key] = _Entry(value=value, expires_at=now + ttl)

    def evict_expired(self) -> int:
        """Remove every expired entry and return how many were evicted."""
        now = time.monotonic()
        expired_keys = [k for k, e in self._data.items() if now >= e.expires_at]
        for k in expired_keys:
            del self._data[k]
        self._stats.evictions += len(expired_keys)
        return len(expired_keys)

    def stats(self) -> dict[str, int]:
        """Return a snapshot of cache performance counters.

        Returns a dict with keys ``hits``, ``misses``, and ``evictions``.
        """
        return {
            "hits": self._stats.hits,
            "misses": self._stats.misses,
            "evictions": self._stats.evictions,
        }

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: Hashable) -> bool:
        entry = self._data.get(key)
        if entry is None:
            return False
        if time.monotonic() >= entry.expires_at:
            del self._data[key]
            self._stats.evictions += 1
            return False
        return True

    def keys(self) -> list[Hashable]:
        """Return non-expired keys ordered most- to least-recently-used."""
        self.evict_expired()
        return list(reversed(self._data))


if __name__ == "__main__":
    print("=== LRUTTLCache demo ===\n")

    cache = LRUTTLCache(capacity=3)

    cache.put("a", 1, ttl=0.5)
    cache.put("b", 2, ttl=5.0)
    cache.put("c", 3, ttl=5.0)
    print(f"after 3 puts:  keys={cache.keys()}, len={len(cache)}")

    cache.put("d", 4, ttl=5.0)
    print(f"after 4th put: keys={cache.keys()}, len={len(cache)}  ('a' evicted as LRU)")

    _ = cache.get("b")
    cache.put("e", 5, ttl=5.0)
    print(f"after get(b)+put(e): keys={cache.keys()}  ('c' evicted; 'b' was promoted)")

    print(f"\nstats so far: {cache.stats()}")

    cache2 = LRUTTLCache(capacity=5)
    cache2.put("x", 10, ttl=0.3)
    cache2.put("y", 20, ttl=5.0)
    print(f"\nbefore sleep:  'x' in cache2 = {'x' in cache2}")
    time.sleep(0.35)
    print(f"after 0.35s:   get('x') = {cache2.get('x')}  (expired)")
    print(f"               'x' in cache2 = {'x' in cache2}")
    print(f"               get('y') = {cache2.get('y')}  (still alive)")

    print(f"\ncache2 stats:  {cache2.stats()}")

    cache3 = LRUTTLCache(capacity=10)
    for i in range(5):
        cache3.put(f"k{i}", i, ttl=0.2)
    cache3.put("keeper", 99, ttl=10.0)
    print(f"\nbefore sweep:  len={len(cache3)}")
    time.sleep(0.25)
    n = cache3.evict_expired()
    print(f"after sweep:   evicted={n}, len={len(cache3)}, keys={cache3.keys()}")
    print(f"cache3 stats:  {cache3.stats()}")

    print("\ndone.")
