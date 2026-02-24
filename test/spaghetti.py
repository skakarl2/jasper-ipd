"""
Spaghetti Sort Implementation

A creative sorting algorithm that mimics the physical process of sorting spaghetti strands.
The metaphor: Hold spaghetti strands vertically, then sweep horizontally from bottom to top.
The shortest strand is encountered first, then the next shortest, and so on.

This implementation uses the counting approach: for each element, count how many 
elements are smaller than it to determine its final position.

Time Complexity: O(n²) in the basic version, O(n + k) with optimizations where k is the range
Space Complexity: O(n) for the result array
"""

def spaghetti_sort(arr):
    """
    Sort an array using the Spaghetti Sort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        List: Sorted array in ascending order
        
    Example:
        >>> spaghetti_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]
    """
    if not arr:
        return arr
    
    if len(arr) <= 1:
        return arr[:]
    
    n = len(arr)
    result = [0] * n
    
    # For each element, count how many elements are smaller
    # This determines the "height" at which we encounter this spaghetti strand
    for i in range(n):
        position = 0
        current_val = arr[i]
        
        # Count elements smaller than current element
        for j in range(n):
            if arr[j] < current_val:
                position += 1
            elif arr[j] == current_val and j < i:
                # Handle duplicates by considering original position
                position += 1
        
        # Place the element in its sorted position
        result[position] = current_val
    
    return result


def spaghetti_sort_optimized(arr):
    """
    Optimized version of Spaghetti Sort using counting sort principles.
    Works best when the range of values is not too large.
    
    Args:
        arr: List of integers to sort
        
    Returns:
        List: Sorted array in ascending order
    """
    if not arr:
        return arr
    
    if len(arr) <= 1:
        return arr[:]
    
    # Find the range of values
    min_val = min(arr)
    max_val = max(arr)
    range_size = max_val - min_val + 1
    
    # If range is too large, fall back to basic version
    if range_size > len(arr) * 2:
        return spaghetti_sort(arr)
    
    # Count frequency of each value
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Build the sorted result
    result = []
    for i in range(range_size):
        value = i + min_val
        frequency = count[i]
        result.extend([value] * frequency)
    
    return result


def spaghetti_sort_visual(arr, show_steps=False):
    """
    Visual version that simulates the actual spaghetti sorting process.
    
    Args:
        arr: List of numbers representing spaghetti lengths
        show_steps: If True, print each step of the sorting process
        
    Returns:
        List: Sorted array
    """
    if not arr:
        return arr
    
    original_arr = arr[:]
    n = len(arr)
    
    if show_steps:
        print("🍝 Spaghetti Sort Visualization")
        print(f"Original strands: {original_arr}")
        print("\nHolding all spaghetti strands vertically...")
        print("Sweeping hand from bottom to top...")
    
    # Create a list to track which strands we've collected
    collected = []
    remaining = arr[:]
    
    # Simulate sweeping from shortest to longest
    while remaining:
        # Find the shortest remaining strand
        shortest = min(remaining)
        shortest_index = remaining.index(shortest)
        
        if show_steps:
            print(f"✋ Hand encounters strand of length {shortest}")
        
        # Remove this strand and add to collected
        collected.append(remaining.pop(shortest_index))
    
    if show_steps:
        print(f"\n✅ All strands collected in order: {collected}")
    
    return collected


def demonstrate_spaghetti_sort():
    """Demonstrate the Spaghetti Sort algorithm with examples."""
    print("🍝 Spaghetti Sort Demonstration\n")
    
    # Example 1: Basic sorting
    test1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Test 1 - Basic array: {test1}")
    sorted1 = spaghetti_sort(test1)
    print(f"Sorted result: {sorted1}")
    print(f"Verification: {sorted(test1) == sorted1}\n")
    
    # Example 2: Array with duplicates
    test2 = [5, 2, 8, 2, 9, 1, 5, 5]
    print(f"Test 2 - With duplicates: {test2}")
    sorted2 = spaghetti_sort(test2)
    print(f"Sorted result: {sorted2}")
    print(f"Verification: {sorted(test2) == sorted2}\n")
    
    # Example 3: Visual demonstration
    test3 = [30, 10, 50, 20, 40]
    print(f"Test 3 - Visual demonstration:")
    spaghetti_sort_visual(test3, show_steps=True)
    
    # Example 4: Performance comparison
    import time
    test4 = list(range(100, 0, -1))  # Reverse sorted array
    
    start = time.time()
    basic_result = spaghetti_sort(test4)
    basic_time = time.time() - start
    
    start = time.time()
    optimized_result = spaghetti_sort_optimized(test4)
    optimized_time = time.time() - start
    
    print(f"\nPerformance Test (100 elements):")
    print(f"Basic version: {basic_time:.6f} seconds")
    print(f"Optimized version: {optimized_time:.6f} seconds")
    print(f"Both produce same result: {basic_result == optimized_result}")


if __name__ == "__main__":
    demonstrate_spaghetti_sort()