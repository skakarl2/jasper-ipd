"""Probabilistic skip list with range query support."""

import random
import math
from typing import Any, Optional

MAX_LEVEL = 16
P_FACTOR = 0.5


class _Node:
    __slots__ = ("key", "value", "forward")

    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward: list[Optional["_Node"]] = [None] * (level + 1)


def _random_level() -> int:
    """Generate a level using a geometric distribution with p=0.5."""
    level = 0
    while random.random() < P_FACTOR and level < MAX_LEVEL:
        level += 1
    return level


class SkipList:
    """A probabilistic skip list mapping comparable keys to values.

    Expected O(log n) insert, search, and delete. Range queries run in
    O(log n + k) where k is the number of results.
    """

    def __init__(self):
        self._header = _Node(key=None, value=None, level=MAX_LEVEL)
        self._level = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def min_key(self) -> Optional[Any]:
        """Return the smallest key in the skip list, or None if empty."""
        first = self._header.forward[0]
        if first is None:
            return None
        return first.key

    def max_key(self) -> Optional[Any]:
        """Return the largest key in the skip list, or None if empty."""
        node = self._header
        for level in range(self._level, -1, -1):
            while node.forward[level] is not None:
                node = node.forward[level]
        if node is self._header:
            return None
        return node.key

    def _find_update(self, key) -> list[Optional[_Node]]:
        # Human rewrite: walk down levels collecting the rightmost node
        # whose forward pointer stays strictly left of `key`.
        update: list[Optional[_Node]] = [None] * (MAX_LEVEL + 1)
        node = self._header
        level = self._level
        while level >= 0:
            nxt = node.forward[level]
            while nxt is not None and nxt.key < key:
                node = nxt
                nxt = node.forward[level]
            update[level] = node
            level -= 1
        return update

    def insert(self, key, value) -> None:
        """Insert a key-value pair, replacing the value if the key exists."""
        update = self._find_update(key)
        candidate = update[0].forward[0]

        if candidate is not None and candidate.key == key:
            candidate.value = value
            return

        new_level = _random_level()
        if new_level > self._level:
            for i in range(self._level + 1, new_level + 1):
                update[i] = self._header
            self._level = new_level

        node = _Node(key, value, new_level)
        for i in range(new_level + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

        self._size += 1

    def search(self, key) -> Optional[Any]:
        """Return the value for key, or None if not found."""
        current = self._header
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current is not None and current.key == key:
            return current.value
        return None

    def delete(self, key) -> bool:
        """Remove key from the list. Returns True if the key was present."""
        update = self._find_update(key)
        target = update[0].forward[0]

        if target is None or target.key != key:
            return False

        for i in range(self._level + 1):
            if update[i].forward[i] is not target:
                break
            update[i].forward[i] = target.forward[i]

        while self._level > 0 and self._header.forward[self._level] is None:
            self._level -= 1

        self._size -= 1
        return True

    def range_query(self, lo, hi) -> list[tuple[Any, Any]]:
        """Return all (key, value) pairs where lo <= key <= hi."""
        results: list[tuple[Any, Any]] = []
        current = self._header
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < lo:
                current = current.forward[i]
        current = current.forward[0]
        while current is not None and current.key <= hi:
            results.append((current.key, current.value))
            current = current.forward[0]
        return results

    def count_range(self, lo, hi) -> int:
        """Return the number of keys k satisfying lo <= k <= hi.

        Uses the skip list's upper levels to reach the start of the range
        in O(log n), then walks the bottom level counting entries until
        the key exceeds hi.  Total cost is O(log n + k) where k is the
        count returned.
        """
        count = 0
        current = self._header
        for i in range(self._level, -1, -1):
            while current.forward[i] is not None and current.forward[i].key < lo:
                current = current.forward[i]
        current = current.forward[0]
        while current is not None and current.key <= hi:
            count += 1
            current = current.forward[0]
        return count

    def to_sorted_list(self) -> list[tuple[Any, Any]]:
        """Return every (key, value) pair in ascending key order.

        Walks the bottom-level linked list from head to tail in O(n).
        """
        result: list[tuple[Any, Any]] = []
        current = self._header.forward[0]
        while current is not None:
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def items(self) -> list[tuple[Any, Any]]:
        """Return all (key, value) pairs in sorted order."""
        return self.range_query(float("-inf"), float("inf"))


if __name__ == "__main__":
    sl = SkipList()

    words = [
        (50, "fifty"),
        (30, "thirty"),
        (70, "seventy"),
        (20, "twenty"),
        (40, "forty"),
        (60, "sixty"),
        (80, "eighty"),
        (10, "ten"),
        (35, "thirty-five"),
        (55, "fifty-five"),
    ]

    print("=== Insert ===")
    for k, v in words:
        sl.insert(k, v)
        print(f"  insert({k}, {v!r})")
    print(f"  size: {len(sl)}")

    print("\n=== Search ===")
    for key in [30, 55, 99]:
        result = sl.search(key)
        print(f"  search({key}) -> {result!r}")

    print("\n=== Range Query [25, 60] ===")
    for k, v in sl.range_query(25, 60):
        print(f"  {k}: {v}")

    print("\n=== Delete 40, 70 ===")
    for key in [40, 70]:
        removed = sl.delete(key)
        print(f"  delete({key}) -> {removed}")
    print(f"  size: {len(sl)}")

    print("\n=== All items after deletions ===")
    for k, v in sl.items():
        print(f"  {k}: {v}")

    print("\n=== Update existing key ===")
    sl.insert(30, "THIRTY-UPDATED")
    print(f"  search(30) -> {sl.search(30)!r}")
    print(f"  size: {len(sl)} (unchanged)")
