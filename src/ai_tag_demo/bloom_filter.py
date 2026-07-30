"""Counting Bloom filter with double-hashing and removal support.

A space-efficient probabilistic set that uses integer counters instead of
single bits, enabling both insertion and deletion. False positives are
possible; false negatives are not (assuming no counter underflow from
removing items that were never added).

Double hashing synthesises k probe positions from two base hashes:
    h(i) = (h1 + i * h2) mod m
avoiding the cost of k independent hash computations.
"""

import hashlib
import math
import struct


class CountingBloomFilter:
    """A counting Bloom filter backed by an array of integer counters.

    Parameters
    ----------
    capacity : int
        Number of counter slots (m). Larger values reduce the
        false-positive rate.
    hash_count : int
        Number of hash probes (k) synthesised via double hashing.
    """

    def __init__(self, capacity: int, hash_count: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if hash_count <= 0:
            raise ValueError("hash_count must be positive")
        self._capacity = int(capacity)
        self._hash_count = int(hash_count)
        self._counters = bytearray(self._capacity)
        self._insertions = 0

    # ------------------------------------------------------------------ #
    #  Hashing
    # ------------------------------------------------------------------ #

    def _probe_positions(self, item) -> list[int]:
        """Return the k counter indices for *item* via double hashing.

        Two independent digests (MD5 and SHA-1) are combined to produce
        k positions without computing k separate hashes.
        """
        raw = str(item).encode("utf-8")
        h1 = struct.unpack("<Q", hashlib.md5(raw).digest()[:8])[0]
        h2 = struct.unpack("<Q", hashlib.sha1(raw).digest()[:8])[0]
        if h2 % self._capacity == 0:
            h2 += 1
        return [(h1 + i * h2) % self._capacity for i in range(self._hash_count)]

    # ------------------------------------------------------------------ #
    #  Core API
    # ------------------------------------------------------------------ #

    def add(self, item) -> None:
        # human edit: guard against counter overflow at 255 (byte ceiling)
        for pos in self._probe_positions(item):
            if self._counters[pos] < 255:
                self._counters[pos] += 1
        self._insertions += 1

    def remove(self, item) -> None:
        """Remove *item* by decrementing each probed counter.

        Raises ``KeyError`` if any probed counter is already zero,
        indicating the item was never added (or was already removed).
        """
        positions = self._probe_positions(item)
        for pos in positions:
            if self._counters[pos] == 0:
                raise KeyError(f"{item!r} is not present in the filter")
        for pos in positions:
            self._counters[pos] -= 1
        self._insertions -= 1

    def contains(self, item) -> bool:
        """Return ``True`` if *item* is probably in the set, ``False`` if definitely not."""
        return all(self._counters[pos] > 0 for pos in self._probe_positions(item))

    # ------------------------------------------------------------------ #
    #  Analytics
    # ------------------------------------------------------------------ #

    def estimated_count(self) -> float:
        """Approximate the number of distinct items via the zero-counter method.

        Uses the inverse Bloom-fill formula:
            n_hat = -(m / k) * ln(zeros / m)
        Falls back to the raw insertion count when every counter is
        non-zero (the log term would be undefined).
        """
        zeros = self._counters.count(0)
        if zeros == 0:
            return self._insertions
        return -(self._capacity / self._hash_count) * math.log(zeros / self._capacity)

    def current_false_positive_rate(self) -> float:
        """Estimate the current false-positive probability.

        Standard approximation: (1 - e^(-k*n/m))^k
        """
        if self._insertions == 0:
            return 0.0
        exponent = -self._hash_count * self._insertions / self._capacity
        return (1.0 - math.exp(exponent)) ** self._hash_count

    # ------------------------------------------------------------------ #
    #  Set operations
    # ------------------------------------------------------------------ #

    def union(self, other: "CountingBloomFilter") -> "CountingBloomFilter":
        """Return a new filter whose counters are the element-wise sum.

        Both operands must share the same capacity and hash_count so
        probe positions are consistent.
        """
        if self._capacity != other._capacity or self._hash_count != other._hash_count:
            raise ValueError("Cannot union filters with different capacity or hash_count")
        merged = CountingBloomFilter(self._capacity, self._hash_count)
        for i in range(self._capacity):
            merged._counters[i] = self._counters[i] + other._counters[i]
        merged._insertions = self._insertions + other._insertions
        return merged

    # ------------------------------------------------------------------ #
    #  Dunder helpers
    # ------------------------------------------------------------------ #

    def __len__(self) -> int:
        return self._insertions

    def __contains__(self, item) -> bool:
        return self.contains(item)

    def __repr__(self) -> str:
        return (
            f"CountingBloomFilter(capacity={self._capacity}, "
            f"hash_count={self._hash_count}, items={self._insertions})"
        )


# ---------------------------------------------------------------------- #
#  Demo
# ---------------------------------------------------------------------- #

if __name__ == "__main__":
    bf = CountingBloomFilter(capacity=1024, hash_count=5)

    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    for fruit in fruits:
        bf.add(fruit)

    print(f"Filter : {bf}")
    print(f"Est. FP rate : {bf.current_false_positive_rate():.6f}")
    print(f"Est. count   : {bf.estimated_count():.1f}")
    print()

    probes = ["apple", "banana", "fig", "grape", "cherry"]
    for probe in probes:
        verdict = "probably yes" if probe in bf else "definitely no"
        print(f"  contains({probe!r:>14}) -> {verdict}")

    print()
    bf.remove("banana")
    print("After removing 'banana':")
    in_filter = "probably yes" if "banana" in bf else "definitely no"
    print(f"  contains('banana') -> {in_filter}")
    print(f"  items: {len(bf)}, FP rate: {bf.current_false_positive_rate():.6f}")

    print()
    bf2 = CountingBloomFilter(capacity=1024, hash_count=5)
    for item in ["fig", "grape", "honeydew"]:
        bf2.add(item)
    combined = bf.union(bf2)
    print(f"Union filter : {combined}")
    print(f"  contains('fig')   -> {'probably yes' if 'fig' in combined else 'definitely no'}")
    print(f"  contains('apple') -> {'probably yes' if 'apple' in combined else 'definitely no'}")

    print()
    false_positives = sum(1 for i in range(10_000) if f"nonexistent_{i}" in bf)
    print(
        f"Empirical FP check: {false_positives}/10000 false positives "
        f"({false_positives / 10_000:.4%})"
    )
