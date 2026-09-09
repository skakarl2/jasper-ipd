"""LRU Cache implementation using a doubly-linked list and hash map.

All core operations (get, put, evict) run in O(1) time. The linked list
maintains access order so the least-recently-used entry is always at the
tail, ready for eviction when capacity is exceeded.
"""

from __future__ import annotations


class Node:
    """Doubly-linked list node that holds a single cache entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.key!r}, {self.value!r})"


class CacheStats:
    """Accumulates hit / miss / eviction counters for an LRU cache."""

    def __init__(self) -> None:
        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0

    @property
    def hit_rate(self) -> float:
        """Return the fraction of lookups that were hits, or 0.0 if none."""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0

    def __repr__(self) -> str:
        return (
            f"CacheStats(hits={self.hits}, misses={self.misses}, "
            f"evictions={self.evictions}, hit_rate={self.hit_rate:.2%})"
        )


class LRUCache:
    """Least-Recently-Used cache backed by a dict and a doubly-linked list.

    Args:
        capacity: Maximum number of entries. Must be at least 1.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._map: dict[int, Node] = {}
        self._head = Node(0, 0)  # sentinel
        self._tail = Node(0, 0)  # sentinel
        self._head.next = self._tail
        self._tail.prev = self._head
        self.stats = CacheStats()

    # -- internal linked-list helpers --

    def _remove(self, node: Node) -> None:
        """Unlink *node* from the list."""
        prev, nxt = node.prev, node.next
        assert prev is not None and nxt is not None
        prev.next = nxt
        nxt.prev = prev

    def _push_front(self, node: Node) -> None:
        """Insert *node* right after the head sentinel (most-recent spot)."""
        nxt = self._head.next
        assert nxt is not None
        self._head.next = node
        node.prev = self._head
        node.next = nxt
        nxt.prev = node

    def _move_to_front(self, node: Node) -> None:
        """Promote *node* to the most-recently-used position."""
        self._remove(node)
        self._push_front(node)

    # -- public API --

    def get(self, key: int) -> int | None:
        """Return the value for *key*, or ``None`` on a miss."""
        node = self._map.get(key)
        if node is None:
            self.stats.misses += 1
            return None
        self.stats.hits += 1
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update *key*. Evicts the LRU entry when at capacity."""
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return
        if len(self._map) >= self._capacity:
            self.evict()
        new_node = Node(key, value)
        self._map[key] = new_node
        self._push_front(new_node)

    def evict(self) -> tuple[int, int] | None:
        """Remove and return the least-recently-used ``(key, value)`` pair.

        Returns ``None`` if the cache is empty.
        """
        lru = self._tail.prev
        if lru is self._head:
            return None
        assert lru is not None
        self._remove(lru)
        del self._map[lru.key]
        self.stats.evictions += 1
        return (lru.key, lru.value)

    def keys(self) -> list[int]:
        """Return keys in most-recently-used to least-recently-used order."""
        result: list[int] = []
        cur = self._head.next
        while cur is not self._tail:
            assert cur is not None
            result.append(cur.key)
            cur = cur.next
        return result

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: int) -> bool:
        return key in self._map

    def __repr__(self) -> str:
        items = ", ".join(f"{k}: {self._map[k].value}" for k in self.keys())
        return f"LRUCache(capacity={self._capacity}, {{{items}}})"


# -- demo --

if __name__ == "__main__":
    import random

    random.seed(42)

    CAPACITY = 5
    KEY_RANGE = 10
    OPS = 40

    cache = LRUCache(CAPACITY)
    print(f"LRU Cache demo  —  capacity={CAPACITY}, key_range=0..{KEY_RANGE - 1}, ops={OPS}\n")

    for i in range(1, OPS + 1):
        if random.random() < 0.5 or len(cache) == 0:
            key = random.randint(0, KEY_RANGE - 1)
            val = random.randint(100, 999)
            cache.put(key, val)
            tag = "PUT"
            detail = f"key={key} val={val}"
        else:
            key = random.randint(0, KEY_RANGE - 1)
            result = cache.get(key)
            tag = "GET"
            detail = f"key={key} -> {result}"

        if i % 10 == 0:
            print(f"  [{i:>2}] {tag:3}  {detail:<25}  cache={cache.keys()}")

    print(f"\nFinal cache ({len(cache)} entries): {cache}")
    print(f"Stats: {cache.stats}")
    print(f"Hit rate: {cache.stats.hit_rate:.1%}")
