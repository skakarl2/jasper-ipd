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
        # human edit: validate then store config compactly
        if size <= 0:
            raise ValueError("size must be positive")
        if num_hashes <= 0:
            raise ValueError("num_hashes must be positive")
        self._size = int(size)
        self._num_hashes = int(num_hashes)
        self._counters = bytearray(size)
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

    def union(self, other):
        """Return a new filter whose counters are the element-wise sum of two filters.

        Both filters must share the same size and hash configuration so that
        probe indices are consistent. The resulting filter behaves as if every
        item added to either operand had been added to the result.

        Raises ``ValueError`` if size or num_hashes differ between operands.
        """
        if self._size != other._size or self._num_hashes != other._num_hashes:
            raise ValueError(
                "Cannot union filters with different size or num_hashes"
            )
        merged = CountingBloomFilter(self._size, self._num_hashes)
        for i in range(self._size):
            merged._counters[i] = self._counters[i] + other._counters[i]
        merged._item_count = self._item_count + other._item_count
        return merged

    def estimated_count(self):
        """Approximate the number of distinct items in the filter.

        Derives the estimate from the fraction of zero-valued counters using
        the inverse of the standard Bloom-fill formula:

            n_hat = -(m / k) * ln(V / m)

        where m = size, k = num_hashes, and V = number of counters still at
        zero. When every counter is non-zero the formula is undefined, so we
        fall back to the raw insertion count.
        """
        zero_count = self._counters.count(0)
        if zero_count == 0:
            return self._item_count
        return -self._size / self._num_hashes * math.log(zero_count / self._size)

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
