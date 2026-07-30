"""LRU cache with per-entry TTL expiry.

Uses a doubly-linked list for O(1) recency promotion and a dict for O(1)
key lookup.  Each entry carries its own expiration timestamp so stale
data is evicted lazily on access or explicitly via evict_expired().
"""

from __future__ import annotations

import time
from typing import Any, Hashable


class _Node:
    """Doubly-linked list node holding one cache entry."""

    __slots__ = ("key", "value", "expires_at", "prev", "next")

    def __init__(
        self,
        key: Hashable,
        value: Any,
        expires_at: float,
    ) -> None:
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: _Node | None = None
        self.next: _Node | None = None


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
        self._map: dict[Hashable, _Node] = {}
        self._head = _Node(None, None, 0.0)  # sentinel
        self._tail = _Node(None, None, 0.0)  # sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    # -- public API ----------------------------------------------------------

    def get(self, key: Hashable) -> Any | None:
        """Return the value for *key*, or ``None`` if missing or expired.

        A hit promotes the entry to most-recently-used.  An expired entry
        is removed lazily on access.
        """
        node = self._map.get(key)
        if node is None:
            return None
        if time.monotonic() >= node.expires_at:
            self._remove_node(node)
            del self._map[key]
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key: Hashable, value: Any, ttl: float) -> None:
        """Insert or update *key* with *value* and a per-entry *ttl* in seconds.

        If the key already exists its value, TTL, and recency are refreshed.
        If the cache is at capacity the least-recently-used entry is evicted.
        """
        if ttl <= 0:
            raise ValueError("ttl must be > 0")

        now = time.monotonic()
        existing = self._map.get(key)
        if existing is not None:
            existing.value = value
            existing.expires_at = now + ttl
            self._move_to_front(existing)
            return

        if len(self._map) >= self._capacity:
            self._evict_lru()

        node = _Node(key, value, now + ttl)
        self._map[key] = node
        self._push_front(node)

    def evict_expired(self) -> int:
        """Remove every expired entry and return how many were evicted."""
        now = time.monotonic()
        victims = [k for k, n in self._map.items() if now >= n.expires_at]
        for k in victims:
            self._remove_node(self._map.pop(k))
        return len(victims)

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: Hashable) -> bool:
        node = self._map.get(key)
        if node is None:
            return False
        if time.monotonic() >= node.expires_at:
            self._remove_node(node)
            del self._map[key]
            return False
        return True

    def keys(self) -> list[Hashable]:
        """Return non-expired keys ordered most- to least-recently-used."""
        self.evict_expired()
        result: list[Hashable] = []
        cur = self._head.next
        while cur is not self._tail:
            result.append(cur.key)
            cur = cur.next
        return result

    # -- linked-list internals -----------------------------------------------

    def _push_front(self, node: _Node) -> None:
        after_head = self._head.next
        self._head.next = node
        node.prev = self._head
        node.next = after_head
        after_head.prev = node

    def _remove_node(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None

    def _move_to_front(self, node: _Node) -> None:
        self._remove_node(node)
        self._push_front(node)

    def _evict_lru(self) -> None:
        lru = self._tail.prev
        if lru is self._head:
            return
        self._remove_node(lru)
        del self._map[lru.key]


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

    cache2 = LRUTTLCache(capacity=5)
    cache2.put("x", 10, ttl=0.3)
    cache2.put("y", 20, ttl=5.0)
    print(f"\nbefore sleep:  'x' in cache2 = {'x' in cache2}")
    time.sleep(0.35)
    print(f"after 0.35s:   get('x') = {cache2.get('x')}  (expired)")
    print(f"               'x' in cache2 = {'x' in cache2}")
    print(f"               get('y') = {cache2.get('y')}  (still alive)")

    cache3 = LRUTTLCache(capacity=10)
    for i in range(5):
        cache3.put(f"k{i}", i, ttl=0.2)
    cache3.put("keeper", 99, ttl=10.0)
    print(f"\nbefore sweep:  len={len(cache3)}")
    time.sleep(0.25)
    n = cache3.evict_expired()
    print(f"after sweep:   evicted={n}, len={len(cache3)}, keys={cache3.keys()}")

    print("\ndone.")
