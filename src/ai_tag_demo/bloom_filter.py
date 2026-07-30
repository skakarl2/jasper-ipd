"""Counting Bloom filter with double hashing and removal support.

A space-efficient probabilistic set that uses integer counters instead of
single bits, allowing both insertion and deletion. False positives are
possible; false negatives are not (assuming no counter underflow from
removing items that were never added).

Double hashing combines two independent base hashes to produce k probe
positions: h(i) = (h1 + i * h2) mod m, avoiding the cost of k separate
hash computations.
"""

import hashlib
import math
import struct


class CountingBloomFilter:
    """A counting Bloom filter backed by an array of integer counters.

    Parameters
    ----------
    size : int
        Number of counter slots (m). Larger values reduce false-positive rate.
    num_hashes : int
        Number of hash functions (k) synthesised via double hashing.
    """

    def __init__(self, size, num_hashes):
        if size <= 0:
            raise ValueError("size must be positive")
        if num_hashes <= 0:
            raise ValueError("num_hashes must be positive")
        self._size = size
        self._num_hashes = num_hashes
        self._counters = [0] * size
        self._item_count = 0

    def _base_hashes(self, item):
        raw = str(item).encode("utf-8")
        h1 = struct.unpack("<Q", hashlib.md5(raw).digest()[:8])[0]
        h2 = struct.unpack("<Q", hashlib.sha1(raw).digest()[:8])[0]
        if h2 % self._size == 0:
            h2 += 1
        return h1, h2

    def _probe_indices(self, item):
        h1, h2 = self._base_hashes(item)
        return [(h1 + i * h2) % self._size for i in range(self._num_hashes)]

    def add(self, item):
        """Insert *item* into the filter by incrementing each probed counter."""
        for idx in self._probe_indices(item):
            self._counters[idx] += 1
        self._item_count += 1

    def remove(self, item):
        """Remove *item* by decrementing each probed counter.

        Raises ``KeyError`` if any probed counter is already zero, which
        indicates the item was never added (or was already removed).
        """
        indices = self._probe_indices(item)
        for idx in indices:
            if self._counters[idx] <= 0:
                raise KeyError(f"{item!r} is not present in the filter")
        for idx in indices:
            self._counters[idx] -= 1
        self._item_count -= 1

    def contains(self, item):
        """Return ``True`` if *item* is probably in the set, ``False`` if definitely not."""
        return all(self._counters[idx] > 0 for idx in self._probe_indices(item))

    def current_false_positive_rate(self):
        """Estimate the current false-positive probability.

        Uses the standard approximation:  (1 - e^(-k*n/m))^k
        where k = num_hashes, n = items inserted, m = size.
        """
        if self._item_count == 0:
            return 0.0
        exponent = -self._num_hashes * self._item_count / self._size
        return (1.0 - math.exp(exponent)) ** self._num_hashes

    def __len__(self):
        return self._item_count

    def __contains__(self, item):
        return self.contains(item)

    def __repr__(self):
        return (
            f"CountingBloomFilter(size={self._size}, "
            f"num_hashes={self._num_hashes}, items={self._item_count})"
        )


if __name__ == "__main__":
    bf = CountingBloomFilter(size=1024, num_hashes=5)

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for w in words:
        bf.add(w)

    print(f"Filter: {bf}")
    print(f"Estimated FP rate: {bf.current_false_positive_rate():.6f}")
    print()

    for probe in ["apple", "banana", "fig", "grape", "cherry"]:
        status = "probably yes" if probe in bf else "definitely no"
        print(f"  contains({probe!r:>14}) -> {status}")

    print()
    bf.remove("banana")
    print("After removing 'banana':")
    print(f"  contains('banana') -> {'probably yes' if 'banana' in bf else 'definitely no'}")
    print(f"  items: {len(bf)}, FP rate: {bf.current_false_positive_rate():.6f}")

    print()
    fp_hits = sum(1 for i in range(10_000) if f"nonexistent_{i}" in bf)
    print(f"Empirical FP check: {fp_hits}/10000 false positives "
          f"({fp_hits / 10_000:.4%})")
