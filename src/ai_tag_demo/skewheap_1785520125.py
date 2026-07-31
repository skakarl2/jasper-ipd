"""
Self-Adjusting Skew Heap Implementation
========================================
A mergeable priority queue that uses skew heaps, which self-adjust during merge
operations by unconditionally swapping children along the merge path. This provides
amortized logarithmic time complexity for operations without requiring balance tracking.

Author: AI Assistant
"""

from typing import Optional, Iterator
from collections import deque


class SkewHeapNode:
    """
    Node in a skew heap storing a key and references to left/right subtrees.
    """
    
    def __init__(self, key: int):
        """
        Initialize a heap node with the given key.
        
        Args:
            key: The integer value stored in this node
        """
        self.key = key
        self.left: Optional[SkewHeapNode] = None
        self.right: Optional[SkewHeapNode] = None
    
    def __repr__(self) -> str:
        """String representation showing the node's key."""
        return f"SkewHeapNode({self.key})"


class SkewHeap:
    """
    A self-adjusting skew heap that maintains min-heap property while unconditionally
    swapping children during merge operations to achieve amortized efficiency.
    """
    
    def __init__(self):
        """Initialize an empty skew heap."""
        self._root: Optional[SkewHeapNode] = None
        self._size: int = 0
        self._merge_count: int = 0
    
    def _merge_recursive(self, h1: Optional[SkewHeapNode], 
                        h2: Optional[SkewHeapNode]) -> Optional[SkewHeapNode]:
        """
        Recursively merge two skew heaps, swapping children at each step.
        This is the core operation that gives skew heaps their self-adjusting property.
        
        Args:
            h1: Root of first heap (or subtree)
            h2: Root of second heap (or subtree)
            
        Returns:
            Root of the merged heap
        """
        self._merge_count += 1
        # Base cases: if either heap is empty, return the other
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        
        # Ensure h1 has the smaller root (maintain min-heap property)
        if h1.key > h2.key:
            h1, h2 = h2, h1
        
        # The skew heap magic: merge h2 with the RIGHT child of h1,
        # then SWAP the children unconditionally
        h1.right = self._merge_recursive(h1.right, h2)
        h1.left, h1.right = h1.right, h1.left
        
        return h1
    
    def push(self, key: int) -> None:
        """
        Insert a new key into the heap.
        
        Args:
            key: The integer value to insert
        """
        new_node = SkewHeapNode(key)
        self._root = self._merge_recursive(self._root, new_node)
        self._size += 1
    
    def pop_min(self) -> int:
        """
        Remove and return the minimum element from the heap.
        
        Returns:
            The minimum key in the heap
            
        Raises:
            IndexError: If the heap is empty
        """
        if self._root is None:
            raise IndexError("pop_min from empty skew heap")
        
        min_key = self._root.key
        # Merge the left and right subtrees to form the new root
        self._root = self._merge_recursive(self._root.left, self._root.right)
        self._size -= 1
        return min_key
    
    def peek_min(self) -> int:
        """
        Return the minimum element without removing it.
        
        Returns:
            The minimum key in the heap
            
        Raises:
            IndexError: If the heap is empty
        """
        if self._root is None:
            raise IndexError("peek_min from empty skew heap")
        return self._root.key
    
    def merge_with(self, other: 'SkewHeap') -> None:
        """
        Merge another skew heap into this one, emptying the other heap.
        
        Args:
            other: Another SkewHeap instance to merge into this one
        """
        self._root = self._merge_recursive(self._root, other._root)
        self._size += other._size
        # Clear the other heap
        other._root = None
        other._size = 0
    
    def to_sorted_list(self) -> list:
        """
        Return a new list of all keys in the heap in ascending sorted order.

        This method does not mutate the original heap. It works by pushing
        every key into a temporary SkewHeap clone, then repeatedly calling
        pop_min on the clone to extract elements in order.

        Returns:
            A list of keys sorted from smallest to largest.
        """
        clone = SkewHeap()
        for key in self.level_order_traversal():
            clone.push(key)
        result = []
        while not clone.is_empty():
            result.append(clone.pop_min())
        return result

    def count_less_than(self, threshold) -> int:
        """
        Return the number of keys in the heap that are strictly less than
        the given threshold.

        This method traverses the internal node structure recursively and
        does not mutate the heap.

        Args:
            threshold: The value to compare each key against.

        Returns:
            The count of keys where key < threshold.
        """
        def _count(node: Optional[SkewHeapNode]) -> int:
            if node is None:
                return 0
            current = 1 if node.key < threshold else 0
            return current + _count(node.left) + _count(node.right)

        return _count(self._root)

    def merge_count(self) -> int:
        """
        Return the total number of merge operations performed over the heap's lifetime.
        
        This counter tracks all calls to the internal _merge_recursive method, including
        those triggered by push, pop_min, and merge_with operations. Each recursive call
        increments the counter, providing insight into the total work performed by the
        self-adjusting skew heap structure.
        
        Returns:
            The cumulative count of merge operations since heap initialization
        """
        return self._merge_count

    def is_empty(self) -> bool:
        """
        Check if the heap is empty.
        
        Returns:
            True if heap contains no elements, False otherwise
        """
        return self._root is None
    
    def __len__(self) -> int:
        """
        Return the number of elements in the heap.
        
        Returns:
            Count of elements currently stored
        """
        return self._size
    
    def level_order_traversal(self) -> Iterator[int]:
        """
        Yield keys in level-order (breadth-first) traversal of the heap structure.
        This shows the actual tree structure, not sorted order.
        
        Yields:
            Keys in the order they appear level-by-level in the heap tree
        """
        if self._root is None:
            return
        
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            yield node.key
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


if __name__ == "__main__":
    print("=" * 60)
    print("Skew Heap Demonstration")
    print("=" * 60)
    
    # Create first heap with a set of integers
    heap1 = SkewHeap()
    data1 = [15, 3, 9, 21, 7, 12]
    print(f"\nBuilding Heap 1 from: {data1}")
    for value in data1:
        heap1.push(value)
    print(f"Heap 1 size: {len(heap1)}, min: {heap1.peek_min()}")
    
    # Create second heap with different integers
    heap2 = SkewHeap()
    data2 = [4, 18, 1, 14, 6]
    print(f"\nBuilding Heap 2 from: {data2}")
    for value in data2:
        heap2.push(value)
    print(f"Heap 2 size: {len(heap2)}, min: {heap2.peek_min()}")
    
    # Merge the heaps
    print(f"\nMerging Heap 2 into Heap 1...")
    heap1.merge_with(heap2)
    print(f"Merged heap size: {len(heap1)}, min: {heap1.peek_min()}")
    print(f"Heap 2 is now empty: {heap2.is_empty()}")
    
    # Show level-order structure
    print(f"\nLevel-order traversal (heap structure): ", end="")
    print(list(heap1.level_order_traversal()))
    
    # Pop all elements to demonstrate sorted order
    print("\nPopping all elements in sorted order:")
    sorted_values = []
    while not heap1.is_empty():
        value = heap1.pop_min()
        sorted_values.append(value)
        print(f"  Popped: {value:2d}  (remaining: {len(heap1)})")
    
    print(f"\nFinal sorted sequence: {sorted_values}")
    
    # Verify it's actually sorted
    expected = sorted(data1 + data2)
    assert sorted_values == expected, "Heap did not produce correct sorted order!"
    print("✓ Verification passed: Output is correctly sorted")
    
    # Demonstrate count_less_than on heap2 (rebuilt for this demo)
    heap2 = SkewHeap()
    for value in data2:
        heap2.push(value)
    print(f"\nHeap2 keys: {list(heap2.level_order_traversal())}")
    print(f"count_less_than(10) on heap2: {heap2.count_less_than(10)}")

    # Demonstrate to_sorted_list on a small fresh heap
    demo_heap = SkewHeap()
    for v in [8, 2, 5, 11, 1]:
        demo_heap.push(v)
    print(f"\nto_sorted_list on [8, 2, 5, 11, 1]: {demo_heap.to_sorted_list()}")

    print(f"Total merges performed: {heap1.merge_count()}")

    print("\n" + "=" * 60)
    print("=== Skew Heap Demo Complete ===")
    print("=" * 60)
