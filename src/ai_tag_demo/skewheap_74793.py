"""
SkewHeap: A self-adjusting mergeable priority queue implementation.

A skew heap is a self-adjusting heap data structure with the heap property
(parent key ≤ child keys in a min-heap). Unlike binary heaps, skew heaps
support efficient merging of two heaps. The key insight is that merge operations
swap the left and right children at each node, which provides amortized
logarithmic time complexity without requiring explicit balancing.

This implementation provides:
- O(log n) amortized time for push, pop, and merge operations
- O(1) time for peek and size queries
- Efficient heap merging for combining priority queues
"""

from dataclasses import dataclass
from typing import Any, Optional, Iterator, List


@dataclass
class Node:
    """
    A node in the skew heap.
    
    Each node contains a key value and references to left and right children.
    The heap property is maintained: parent.key <= left.key and parent.key <= right.key
    
    Attributes:
        key: The priority value stored in this node
        left: Reference to the left child node (or None)
        right: Reference to the right child node (or None)
    """
    key: Any
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    
    def __repr__(self) -> str:
        """Return a string representation of the node."""
        return f"Node({self.key})"


class SkewHeap:
    """
    A self-adjusting mergeable min-heap implementation.
    
    The skew heap maintains the heap property through a simple merge strategy:
    always swap the left and right children during merge operations. This
    unconditional swapping provides amortization that keeps operations efficient
    without requiring complex balancing logic.
    
    Key features:
    - Mergeable: Two skew heaps can be efficiently combined
    - Self-adjusting: No explicit balancing required
    - Simple implementation: Recursive merge with child swapping
    
    Example:
        >>> heap = SkewHeap()
        >>> heap.push(5)
        >>> heap.push(3)
        >>> heap.push(7)
        >>> heap.peek_min()
        3
        >>> heap.pop_min()
        3
        >>> len(heap)
        2
    """
    
    def __init__(self):
        """Initialize an empty skew heap."""
        self._root: Optional[Node] = None
        self._size: int = 0
    
    def _merge(self, h1: Optional[Node], h2: Optional[Node]) -> Optional[Node]:
        """
        Recursively merge two skew heap nodes.
        
        This is the core operation of the skew heap. It merges two heap trees
        by always choosing the node with the smaller key as the root, then
        recursively merging the right child with the other tree, and finally
        swapping the left and right children.
        
        The swapping ensures that the heap remains roughly balanced through
        amortization, even though we don't enforce strict structural invariants.
        
        Args:
            h1: Root of the first heap (or None)
            h2: Root of the second heap (or None)
        
        Returns:
            The root of the merged heap
        
        Time Complexity:
            O(log n) amortized, where n is the total number of nodes
        """
        # Base cases: if either heap is empty, return the other
        if h1 is None:
            return h2
        if h2 is None:
            return h1
        
        # Ensure h1 has the smaller root (maintain heap property)
        if h1.key > h2.key:
            h1, h2 = h2, h1
        
        # Recursively merge h2 with the right subtree of h1
        h1.right = self._merge(h1.right, h2)
        
        # Swap left and right children (the "skew" operation)
        # This unconditional swapping is what makes the heap self-adjusting
        h1.left, h1.right = h1.right, h1.left
        
        return h1
    
    def meld(self, other: 'SkewHeap') -> None:
        """
        Merge another skew heap into this heap.
        
        After this operation, the other heap becomes empty and all its elements
        are now part of this heap.
        
        Args:
            other: Another SkewHeap to merge into this one
        
        Time Complexity:
            O(log n) amortized
        
        Example:
            >>> h1 = SkewHeap()
            >>> h1.push(1)
            >>> h1.push(3)
            >>> h2 = SkewHeap()
            >>> h2.push(2)
            >>> h2.push(4)
            >>> h1.meld(h2)
            >>> len(h1)
            4
            >>> len(h2)
            0
        """
        self._root = self._merge(self._root, other._root)
        self._size += other._size
        
        # Clear the other heap
        other._root = None
        other._size = 0
    
    def push(self, key: Any) -> None:
        """
        Insert a new key into the heap.
        
        Creates a new single-node heap and merges it with the existing heap.
        
        Args:
            key: The value to insert
        
        Time Complexity:
            O(log n) amortized
        
        Example:
            >>> heap = SkewHeap()
            >>> heap.push(10)
            >>> heap.push(5)
            >>> heap.peek_min()
            5
        """
        new_node = Node(key)
        self._root = self._merge(self._root, new_node)
        self._size += 1
    
    def pop_min(self) -> Any:
        """
        Remove and return the minimum key from the heap.
        
        The minimum is always at the root. After removing it, we merge its
        left and right subtrees to form the new heap.
        
        Returns:
            The minimum key in the heap
        
        Raises:
            IndexError: If the heap is empty
        
        Time Complexity:
            O(log n) amortized
        
        Example:
            >>> heap = SkewHeap()
            >>> heap.push(3)
            >>> heap.push(1)
            >>> heap.push(2)
            >>> heap.pop_min()
            1
            >>> heap.pop_min()
            2
        """
        if self.is_empty():
            raise IndexError("pop_min from empty heap")
        
        min_key = self._root.key
        self._root = self._merge(self._root.left, self._root.right)
        self._size -= 1
        
        return min_key
    
    def peek_min(self) -> Any:
        """
        Return the minimum key without removing it.
        
        Returns:
            The minimum key in the heap
        
        Raises:
            IndexError: If the heap is empty
        
        Time Complexity:
            O(1)
        
        Example:
            >>> heap = SkewHeap()
            >>> heap.push(5)
            >>> heap.peek_min()
            5
            >>> len(heap)
            1
        """
        if self.is_empty():
            raise IndexError("peek_min from empty heap")
        
        return self._root.key
    
    def is_empty(self) -> bool:
        """
        Check if the heap is empty.
        
        Returns:
            True if the heap contains no elements, False otherwise
        
        Time Complexity:
            O(1)
        """
        return self._size == 0
    
    def __len__(self) -> int:
        """
        Return the number of elements in the heap.
        
        Returns:
            The count of elements
        
        Time Complexity:
            O(1)
        """
        return self._size
    
    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the heap in sorted (ascending) order.
        
        This performs an in-order traversal that yields elements from smallest
        to largest. Note that this is a destructive operation on a temporary
        copy of the heap structure.
        
        Yields:
            Keys in ascending order
        
        Time Complexity:
            O(n log n) for complete iteration
        
        Example:
            >>> heap = SkewHeap()
            >>> for val in [5, 2, 8, 1, 9]:
            ...     heap.push(val)
            >>> list(heap)
            [1, 2, 5, 8, 9]
        """
        # Create a copy of the root to avoid modifying the original heap
        def copy_tree(node: Optional[Node]) -> Optional[Node]:
            if node is None:
                return None
            return Node(node.key, copy_tree(node.left), copy_tree(node.right))
        
        temp_root = copy_tree(self._root)
        temp_size = self._size
        
        # Pop elements one by one in sorted order
        while temp_root is not None:
            min_key = temp_root.key
            temp_root = self._merge(temp_root.left, temp_root.right)
            yield min_key
    
    @staticmethod
    def merge_all(heaps: List['SkewHeap']) -> 'SkewHeap':
        """
        Merge multiple skew heaps into a single heap.
        
        This static method takes a list of heaps and merges them all together
        into a new heap. The original heaps remain unchanged.
        
        Args:
            heaps: A list of SkewHeap instances to merge
        
        Returns:
            A new SkewHeap containing all elements from all input heaps
        
        Time Complexity:
            O(k log n) where k is the number of heaps and n is total elements
        
        Example:
            >>> h1 = SkewHeap()
            >>> h1.push(1)
            >>> h2 = SkewHeap()
            >>> h2.push(2)
            >>> h3 = SkewHeap()
            >>> h3.push(3)
            >>> merged = SkewHeap.merge_all([h1, h2, h3])
            >>> len(merged)
            3
            >>> merged.peek_min()
            1
        """
        if not heaps:
            return SkewHeap()
        
        # Create a new heap to hold the result
        result = SkewHeap()
        
        # Copy and merge each heap
        for heap in heaps:
            if not heap.is_empty():
                # Create a temporary heap with a copy of the tree
                def copy_tree(node: Optional[Node]) -> Optional[Node]:
                    if node is None:
                        return None
                    return Node(node.key, copy_tree(node.left), copy_tree(node.right))
                
                temp_heap = SkewHeap()
                temp_heap._root = copy_tree(heap._root)
                temp_heap._size = heap._size
                
                result.meld(temp_heap)
        
        return result
    
    def _get_tree_structure(self, node: Optional[Node], prefix: str = "", is_tail: bool = True) -> str:
        """
        Get a string representation of the tree structure for debugging.
        
        Args:
            node: The current node to represent
            prefix: The prefix string for indentation
            is_tail: Whether this node is the last child
        
        Returns:
            A multi-line string showing the tree structure
        """
        if node is None:
            return ""
        
        result = prefix + ("└── " if is_tail else "├── ") + str(node.key) + "\n"
        
        children = []
        if node.left is not None:
            children.append(("L", node.left))
        if node.right is not None:
            children.append(("R", node.right))
        
        for i, (label, child) in enumerate(children):
            extension = "    " if is_tail else "│   "
            result += prefix + extension + f"[{label}]\n"
            result += self._get_tree_structure(
                child,
                prefix + extension,
                i == len(children) - 1
            )
        
        return result
    
    def __repr__(self) -> str:
        """
        Return a string representation of the heap.
        
        Returns:
            A string showing the heap's size and root value (if any)
        """
        if self.is_empty():
            return "SkewHeap(empty)"
        return f"SkewHeap(size={self._size}, min={self._root.key})"


def main():
    """
    Demonstration of SkewHeap functionality.
    
    This main block demonstrates:
    1. Building a heap from a list
    2. Popping all elements to show sorted order
    3. Merging two heaps together
    4. Using the iterator interface
    5. Merging multiple heaps with merge_all
    """
    print("=" * 60)
    print("SkewHeap Demonstration")
    print("=" * 60)
    
    # Demo 1: Build a heap and pop elements in sorted order
    print("\n1. Building a heap from a list and popping in sorted order:")
    print("-" * 60)
    
    values = [15, 3, 9, 7, 21, 1, 12, 5, 18, 2]
    print(f"Input values: {values}")
    
    heap1 = SkewHeap()
    for val in values:
        heap1.push(val)
    
    print(f"Heap created: {heap1}")
    print(f"Heap size: {len(heap1)}")
    print(f"Minimum element: {heap1.peek_min()}")
    
    print("\nPopping all elements:")
    sorted_values = []
    while not heap1.is_empty():
        min_val = heap1.pop_min()
        sorted_values.append(min_val)
        print(f"  Popped: {min_val:2d}  (remaining: {len(heap1)})")
    
    print(f"\nSorted order: {sorted_values}")
    
    # Demo 2: Merging two heaps
    print("\n2. Merging two heaps:")
    print("-" * 60)
    
    heap_a = SkewHeap()
    heap_a_values = [10, 20, 30, 40]
    for val in heap_a_values:
        heap_a.push(val)
    print(f"Heap A values: {heap_a_values}")
    print(f"Heap A: {heap_a}")
    
    heap_b = SkewHeap()
    heap_b_values = [5, 15, 25, 35]
    for val in heap_b_values:
        heap_b.push(val)
    print(f"Heap B values: {heap_b_values}")
    print(f"Heap B: {heap_b}")
    
    print("\nMelding Heap B into Heap A...")
    heap_a.meld(heap_b)
    
    print(f"Heap A after meld: {heap_a}")
    print(f"Heap B after meld: {heap_b} (now empty)")
    
    print("\nElements in merged heap:")
    merged_sorted = []
    while not heap_a.is_empty():
        val = heap_a.pop_min()
        merged_sorted.append(val)
    print(f"  {merged_sorted}")
    
    # Demo 3: Using the iterator interface
    print("\n3. Using the iterator interface:")
    print("-" * 60)
    
    heap3 = SkewHeap()
    iterator_values = [50, 30, 70, 20, 40, 60, 80, 10]
    for val in iterator_values:
        heap3.push(val)
    
    print(f"Heap values (unsorted): {iterator_values}")
    print(f"Iterating over heap (sorted): {list(heap3)}")
    print(f"Heap after iteration: {heap3} (unchanged)")
    
    # Demo 4: Merging multiple heaps
    print("\n4. Merging multiple heaps with merge_all:")
    print("-" * 60)
    
    heap_list = []
    for i in range(4):
        h = SkewHeap()
        start = i * 10
        values = [start + j for j in [3, 1, 2]]
        for val in values:
            h.push(val)
        heap_list.append(h)
        print(f"Heap {i}: min={h.peek_min()}, size={len(h)}")
    
    print("\nMerging all heaps...")
    mega_heap = SkewHeap.merge_all(heap_list)
    print(f"Merged heap: {mega_heap}")
    
    print("\nAll elements in sorted order:")
    all_sorted = list(mega_heap)
    print(f"  {all_sorted}")
    
    # Demo 5: Error handling
    print("\n5. Error handling:")
    print("-" * 60)
    
    empty_heap = SkewHeap()
    print(f"Empty heap: {empty_heap}")
    print(f"Is empty? {empty_heap.is_empty()}")
    
    try:
        empty_heap.peek_min()
    except IndexError as e:
        print(f"Attempting peek_min on empty heap: IndexError - {e}")
    
    try:
        empty_heap.pop_min()
    except IndexError as e:
        print(f"Attempting pop_min on empty heap: IndexError - {e}")
    
    # Demo 6: Performance showcase with larger dataset
    print("\n6. Performance with larger dataset:")
    print("-" * 60)
    
    import random
    large_data = random.sample(range(1000), 100)
    
    large_heap = SkewHeap()
    for val in large_data:
        large_heap.push(val)
    
    print(f"Created heap with {len(large_heap)} random elements")
    print(f"Minimum element: {large_heap.peek_min()}")
    print(f"Maximum element: {max(large_data)}")
    
    # Extract top 10 elements
    top_10 = []
    for _ in range(10):
        top_10.append(large_heap.pop_min())
    
    print(f"Top 10 smallest elements: {top_10}")
    print(f"Remaining elements in heap: {len(large_heap)}")
    
    print("\n" + "=" * 60)
    print("Demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
