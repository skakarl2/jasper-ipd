"""
LRU Cache Implementation using Doubly-Linked List and Hash Map

This module provides a time-efficient and space-efficient implementation of
an LRU (Least Recently Used) cache with O(1) time complexity for both get
and put operations.

Author: AI Assistant
Date: 2026-07-31
"""


class Node:
    """
    A doubly-linked list node for storing cache entries.
    
    Each node contains a key-value pair along with pointers to the
    previous and next nodes in the list.
    
    Attributes:
        key: The cache key (used for bidirectional lookup)
        value: The cached value
        prev: Reference to the previous node in the list
        next: Reference to the next node in the list
    """
    
    def __init__(self, key=None, value=None):
        """
        Initialize a new node with the given key and value.
        
        Args:
            key: The key for this cache entry
            value: The value for this cache entry
        """
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
    
    def __repr__(self):
        """String representation of the node."""
        return f"Node({self.key}: {self.value})"


class LRUCache:
    """
    LRU Cache implementation with O(1) get and put operations.
    
    This cache maintains a fixed capacity and evicts the least recently
    used item when the capacity is exceeded. It uses a doubly-linked list
    to maintain access order and a hash map for O(1) lookups.
    
    The head of the list represents the most recently used item, and the
    tail represents the least recently used item.
    
    Attributes:
        capacity: Maximum number of items the cache can hold
        cache: Hash map for O(1) key lookups
        head: Dummy head node of the doubly-linked list
        tail: Dummy tail node of the doubly-linked list
    """
    
    def __init__(self, capacity):
        """
        Initialize the LRU cache with a given capacity.
        
        Args:
            capacity: Maximum number of items the cache can hold (must be > 0)
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Cache capacity must be at least 1")
        
        self.capacity = capacity
        self.cache = {}
        
        # Create dummy head and tail nodes for easier list manipulation
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_head(self, node):
        """
        Add a node right after the head (most recently used position).
        
        Args:
            node: The node to add to the front of the list
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """
        Remove a node from the doubly-linked list.
        
        Args:
            node: The node to remove from the list
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node):
        """
        Move an existing node to the head (mark as most recently used).
        
        Args:
            node: The node to move to the front
        """
        self._remove_node(node)
        self._add_to_head(node)
    
    def _pop_tail(self):
        """
        Remove and return the least recently used node (just before tail).
        
        Returns:
            The node that was removed from the tail position
        """
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node
    
    def get(self, key):
        """
        Retrieve a value from the cache by key.
        
        If the key exists, the corresponding node is moved to the head
        to mark it as recently used.
        
        Args:
            key: The key to look up in the cache
            
        Returns:
            The value associated with the key, or -1 if key not found
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.value
    
    def put(self, key, value):
        """
        Insert or update a key-value pair in the cache.
        
        If the key already exists, update its value and move it to the head.
        If the key doesn't exist, create a new node and add it to the head.
        If capacity is exceeded, evict the least recently used item.
        
        Args:
            key: The key to insert or update
            value: The value to associate with the key
        """
        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Create new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # Check capacity and evict if necessary
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]
    
    def size(self):
        """
        Get the current number of items in the cache.
        
        Returns:
            The number of items currently stored in the cache
        """
        return len(self.cache)
    
    def is_empty(self):
        """
        Check if the cache is empty.
        
        Returns:
            True if the cache contains no items, False otherwise
        """
        return len(self.cache) == 0
    
    def clear(self):
        """Remove all items from the cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def __repr__(self):
        """
        String representation showing cache contents in order from MRU to LRU.
        
        Returns:
            A string showing the cache contents ordered from most to least recently used
        """
        if self.is_empty():
            return "LRUCache(capacity={}, contents=[])"
        
        items = []
        current = self.head.next
        while current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        
        contents = " -> ".join(items)
        return f"LRUCache(capacity={self.capacity}, size={self.size()}, MRU->LRU: [{contents}])"


def demonstrate_lru_cache():
    """
    Demonstrate the LRU cache functionality with various operations.
    
    This function shows cache initialization, insertion, retrieval,
    eviction behavior, and cache ordering.
    """
    print("=" * 70)
    print("LRU Cache Demonstration")
    print("=" * 70)
    
    # Create a cache with capacity of 3
    print("\n1. Creating LRU cache with capacity 3")
    cache = LRUCache(3)
    print(f"   {cache}")
    
    # Add some items
    print("\n2. Adding items to cache:")
    cache.put("A", 100)
    print(f"   After put('A', 100): {cache}")
    
    cache.put("B", 200)
    print(f"   After put('B', 200): {cache}")
    
    cache.put("C", 300)
    print(f"   After put('C', 300): {cache}")
    
    # Retrieve an item (makes it most recently used)
    print("\n3. Accessing item 'A' (moves to front):")
    value = cache.get("A")
    print(f"   get('A') returned: {value}")
    print(f"   Cache state: {cache}")
    
    # Add another item (should evict 'B' as it's LRU)
    print("\n4. Adding 'D' (capacity exceeded, evicts LRU):")
    cache.put("D", 400)
    print(f"   After put('D', 400): {cache}")
    print(f"   Note: 'B' was evicted (it was the least recently used)")
    
    # Try to get evicted item
    print("\n5. Attempting to retrieve evicted item 'B':")
    value = cache.get("B")
    print(f"   get('B') returned: {value} (not found)")
    
    # Update an existing item
    print("\n6. Updating existing item 'C' with new value:")
    cache.put("C", 999)
    print(f"   After put('C', 999): {cache}")
    
    # Add more items to show further eviction
    print("\n7. Adding more items to demonstrate eviction:")
    cache.put("E", 500)
    print(f"   After put('E', 500): {cache}")
    print(f"   Note: 'A' was evicted")
    
    cache.put("F", 600)
    print(f"   After put('F', 600): {cache}")
    print(f"   Note: 'D' was evicted")
    
    # Show final state
    print("\n8. Final cache state:")
    print(f"   {cache}")
    print(f"   Cache size: {cache.size()}/{cache.capacity}")
    
    # Test cache clearing
    print("\n9. Clearing the cache:")
    cache.clear()
    print(f"   After clear(): {cache}")
    print(f"   Is empty: {cache.is_empty()}")
    
    # Edge case: capacity of 1
    print("\n10. Edge case - cache with capacity 1:")
    small_cache = LRUCache(1)
    small_cache.put("X", 10)
    print(f"    After put('X', 10): {small_cache}")
    small_cache.put("Y", 20)
    print(f"    After put('Y', 20): {small_cache}")
    print(f"    Note: 'X' was immediately evicted when 'Y' was added")
    
    print("\n" + "=" * 70)
    print("Demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_lru_cache()
