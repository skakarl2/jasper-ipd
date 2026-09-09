#!/usr/bin/env python3
"""
A complete Bloom filter implementation from scratch.

This module provides a space-efficient probabilistic data structure for
testing set membership. False positives are possible, but false negatives
are not.

Classes:
    BloomFilter: Main Bloom filter implementation
    BloomStats: Helper class for analyzing filter statistics
"""

import hashlib
import math


class BloomFilter:
    """
    A Bloom filter implementation using double hashing.
    
    The filter automatically calculates optimal bit array size and number
    of hash functions based on desired capacity and error rate.
    
    Attributes:
        capacity: Expected number of elements to store
        error_rate: Desired false positive probability (0 < error_rate < 1)
    """
    
    def __init__(self, capacity, error_rate):
        """
        Initialize a Bloom filter with optimal parameters.
        
        Args:
            capacity: Expected number of elements to store
            error_rate: Target false positive rate (e.g., 0.01 for 1%)
            
        Raises:
            ValueError: If capacity <= 0 or error_rate not in (0, 1)
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if not 0 < error_rate < 1:
            raise ValueError("Error rate must be between 0 and 1")
            
        self.capacity = capacity
        self.error_rate = error_rate
        
        # Calculate optimal bit array size
        # m = -(n * ln(p)) / (ln(2)^2)
        self.bit_count = self._optimal_bit_count(capacity, error_rate)
        
        # Calculate optimal number of hash functions
        # k = (m/n) * ln(2)
        self.hash_count = self._optimal_hash_count(self.bit_count, capacity)
        
        # Initialize bit array as a bytearray
        self.bit_array = bytearray((self.bit_count + 7) // 8)
        
        # Track number of items added
        self.items_added = 0
    
    @staticmethod
    def _optimal_bit_count(capacity, error_rate):
        """
        Calculate optimal bit array size.
        
        Args:
            capacity: Expected number of elements
            error_rate: Target false positive rate
            
        Returns:
            Optimal number of bits (integer)
        """
        m = -(capacity * math.log(error_rate)) / (math.log(2) ** 2)
        return int(math.ceil(m))
    
    @staticmethod
    def _optimal_hash_count(bit_count, capacity):
        """
        Calculate optimal number of hash functions.
        
        Args:
            bit_count: Size of bit array
            capacity: Expected number of elements
            
        Returns:
            Optimal number of hash functions (integer, minimum 1)
        """
        k = (bit_count / capacity) * math.log(2)
        return max(1, int(math.ceil(k)))
    
    def _hashes(self, item):
        """
        Generate hash values using double hashing technique.
        
        Uses two independent hash functions (MD5 and SHA256) to generate
        k hash values via the formula: h_i(x) = (h1(x) + i*h2(x)) mod m
        
        Args:
            item: Item to hash (will be converted to bytes if needed)
            
        Yields:
            Hash values in range [0, bit_count)
        """
        # Convert item to bytes if necessary
        if isinstance(item, str):
            data = item.encode('utf-8')
        elif isinstance(item, bytes):
            data = item
        else:
            data = str(item).encode('utf-8')
        
        # Generate two independent hash values
        h1 = int.from_bytes(hashlib.md5(data).digest(), 'big')
        h2 = int.from_bytes(hashlib.sha256(data).digest(), 'big')
        
        # Generate k hash values using double hashing
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.bit_count
    
    def _set_bit(self, index):
        """
        Set a bit at the given index to 1.
        
        Args:
            index: Bit position to set
        """
        byte_index = index // 8
        bit_offset = index % 8
        self.bit_array[byte_index] |= (1 << bit_offset)
    
    def _get_bit(self, index):
        """
        Get the value of a bit at the given index.
        
        Args:
            index: Bit position to check
            
        Returns:
            True if bit is set, False otherwise
        """
        byte_index = index // 8
        bit_offset = index % 8
        return bool(self.bit_array[byte_index] & (1 << bit_offset))
    
    def add(self, item):
        """
        Add an item to the Bloom filter.
        
        Args:
            item: Item to add to the filter
        """
        for hash_value in self._hashes(item):
            self._set_bit(hash_value)
        self.items_added += 1
    
    def __contains__(self, item):
        """
        Test if an item might be in the set.
        
        Args:
            item: Item to check for membership
            
        Returns:
            True if item might be in set (possible false positive)
            False if item is definitely not in set (no false negatives)
        """
        return all(self._get_bit(hash_value) for hash_value in self._hashes(item))
    
    def clear(self):
        """
        Clear all items from the Bloom filter.
        
        Resets the bit array to all zeros and resets the item counter.
        """
        self.bit_array = bytearray((self.bit_count + 7) // 8)
        self.items_added = 0
    
    def __len__(self):
        """
        Return the number of items added to the filter.
        
        Note: This is a count of add() calls, not unique items.
        
        Returns:
            Number of items added
        """
        return self.items_added
    
    def __repr__(self):
        """String representation of the Bloom filter."""
        return (f"BloomFilter(capacity={self.capacity}, "
                f"error_rate={self.error_rate}, "
                f"bits={self.bit_count}, "
                f"hashes={self.hash_count}, "
                f"items={self.items_added})")


class BloomStats:
    """
    Helper class for analyzing Bloom filter statistics.
    
    Provides methods to calculate fill ratio and estimated false positive
    rate based on actual filter state.
    """
    
    def __init__(self, bloom_filter):
        """
        Initialize statistics analyzer for a Bloom filter.
        
        Args:
            bloom_filter: BloomFilter instance to analyze
        """
        self.bloom_filter = bloom_filter
    
    @property
    def fill_ratio(self):
        """
        Calculate the ratio of set bits to total bits.
        
        Returns:
            Float between 0 and 1 representing fraction of bits set
        """
        bits_set = sum(
            bin(byte).count('1') for byte in self.bloom_filter.bit_array
        )
        return bits_set / self.bloom_filter.bit_count
    
    @property
    def estimated_false_positive_rate(self):
        """
        Estimate the actual false positive rate based on fill ratio.
        
        Formula: (1 - e^(-kn/m))^k
        where k = number of hash functions
              n = number of items added
              m = bit array size
        
        Returns:
            Estimated false positive probability (0 to 1)
        """
        k = self.bloom_filter.hash_count
        n = self.bloom_filter.items_added
        m = self.bloom_filter.bit_count
        
        if n == 0:
            return 0.0
        
        # Calculate using the standard formula
        exponent = -k * n / m
        return (1 - math.exp(exponent)) ** k
    
    def __str__(self):
        """Human-readable statistics summary."""
        return (f"BloomStats:\n"
                f"  Fill Ratio: {self.fill_ratio:.4f}\n"
                f"  Estimated FP Rate: {self.estimated_false_positive_rate:.6f}\n"
                f"  Target FP Rate: {self.bloom_filter.error_rate:.6f}\n"
                f"  Items Added: {self.bloom_filter.items_added}\n"
                f"  Capacity: {self.bloom_filter.capacity}")


def _generate_test_words(count, prefix="testword_"):
    """
    Generate test words for demonstration.
    
    Args:
        count: Number of words to generate
        prefix: Prefix for generated words
        
    Returns:
        List of generated word strings
    """
    return [f"{prefix}{i}" for i in range(count)]


if __name__ == "__main__":
    print("=" * 70)
    print("Bloom Filter Demonstration")
    print("=" * 70)
    
    # Configuration
    CAPACITY = 500
    ERROR_RATE = 0.01
    WORDS_TO_INSERT = 500
    WORDS_TO_PROBE = 100
    
    print(f"\nConfiguration:")
    print(f"  Target Capacity: {CAPACITY}")
    print(f"  Target Error Rate: {ERROR_RATE} ({ERROR_RATE * 100}%)")
    
    # Create Bloom filter
    bloom = BloomFilter(capacity=CAPACITY, error_rate=ERROR_RATE)
    print(f"\n{bloom}")
    
    # Generate and insert words
    print(f"\nInserting {WORDS_TO_INSERT} words...")
    inserted_words = _generate_test_words(WORDS_TO_INSERT, prefix="present_")
    for word in inserted_words:
        bloom.add(word)
    
    print(f"Inserted {len(bloom)} items")
    
    # Verify all inserted words are found
    print(f"\nVerifying inserted words...")
    found_count = sum(1 for word in inserted_words if word in bloom)
    print(f"  Found: {found_count}/{len(inserted_words)} "
          f"(should be {len(inserted_words)})")
    
    # Test with words NOT in the filter
    print(f"\nProbing {WORDS_TO_PROBE} words NOT in the filter...")
    absent_words = _generate_test_words(WORDS_TO_PROBE, prefix="absent_")
    false_positives = sum(1 for word in absent_words if word in bloom)
    
    measured_fp_rate = false_positives / WORDS_TO_PROBE
    
    print(f"  False Positives: {false_positives}/{WORDS_TO_PROBE}")
    print(f"  Measured FP Rate: {measured_fp_rate:.4f} "
          f"({measured_fp_rate * 100:.2f}%)")
    
    # Show statistics
    print(f"\n{'-' * 70}")
    stats = BloomStats(bloom)
    print(stats)
    
    # Compare measured vs theoretical
    print(f"\n{'-' * 70}")
    print("Comparison:")
    print(f"  Measured FP Rate:    {measured_fp_rate:.6f} "
          f"({measured_fp_rate * 100:.4f}%)")
    print(f"  Theoretical FP Rate: {stats.estimated_false_positive_rate:.6f} "
          f"({stats.estimated_false_positive_rate * 100:.4f}%)")
    print(f"  Target FP Rate:      {ERROR_RATE:.6f} "
          f"({ERROR_RATE * 100:.4f}%)")
    
    # Demonstrate clear functionality
    print(f"\n{'-' * 70}")
    print("Testing clear() method...")
    bloom.clear()
    print(f"After clear: {bloom}")
    remaining = sum(1 for word in inserted_words[:10] if word in bloom)
    print(f"  Words still found: {remaining}/10 (should be 0)")
    
    print(f"\n{'=' * 70}")
    print("Demonstration complete!")
    print("=" * 70)
