#!/usr/bin/env python3
"""
Quicksort Implementation

A fresh implementation of the quicksort algorithm with multiple variations
and utility functions for testing and demonstration.
"""

def quicksort(arr):
    """
    Classic quicksort implementation with Lomuto partition scheme.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        New sorted list (does not modify original)
    """
    if len(arr) <= 1:
        return arr.copy()
    
    # Create a copy to avoid modifying the original array
    arr_copy = arr.copy()
    _quicksort_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _quicksort_helper(arr, low, high):
    """
    Recursive helper function for quicksort.
    
    Args:
        arr: Array to sort (modified in place)
        low: Starting index
        high: Ending index
    """
    if low < high:
        # Partition the array and get the pivot index
        pivot_index = _lomuto_partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        _quicksort_helper(arr, low, pivot_index - 1)
        _quicksort_helper(arr, pivot_index + 1, high)


def _lomuto_partition(arr, low, high):
    """
    Lomuto partition scheme.
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Final position of pivot element
    """
    # Choose the rightmost element as pivot
    pivot = arr[high]
    
    # Index of smaller element, indicates right position of pivot
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Swap pivot to its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_hoare(arr):
    """
    Quicksort implementation using Hoare partition scheme.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        New sorted list (does not modify original)
    """
    if len(arr) <= 1:
        return arr.copy()
    
    arr_copy = arr.copy()
    _quicksort_hoare_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _quicksort_hoare_helper(arr, low, high):
    """
    Recursive helper function for Hoare quicksort.
    """
    if low < high:
        pivot_index = _hoare_partition(arr, low, high)
        _quicksort_hoare_helper(arr, low, pivot_index)
        _quicksort_hoare_helper(arr, pivot_index + 1, high)


def _hoare_partition(arr, low, high):
    """
    Hoare partition scheme.
    
    Args:
        arr: Array to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Index of partition point
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Find element on left that should be on right
        i += 1
        while arr[i] < pivot:
            i += 1
            
        # Find element on right that should be on left
        j -= 1
        while arr[j] > pivot:
            j -= 1
            
        # If elements crossed, partitioning is done
        if i >= j:
            return j
            
        # Swap elements
        arr[i], arr[j] = arr[j], arr[i]


def quicksort_iterative(arr):
    """
    Iterative implementation of quicksort using a stack.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        New sorted list (does not modify original)
    """
    if len(arr) <= 1:
        return arr.copy()
    
    arr_copy = arr.copy()
    stack = [(0, len(arr_copy) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            pivot_index = _lomuto_partition(arr_copy, low, high)
            
            # Push left and right subarrays to stack
            stack.append((low, pivot_index - 1))
            stack.append((pivot_index + 1, high))
    
    return arr_copy


def quicksort_3way(arr):
    """
    3-way quicksort for handling arrays with many duplicate elements efficiently.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        New sorted list (does not modify original)
    """
    if len(arr) <= 1:
        return arr.copy()
    
    arr_copy = arr.copy()
    _quicksort_3way_helper(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def _quicksort_3way_helper(arr, low, high):
    """
    Recursive helper for 3-way quicksort.
    """
    if low >= high:
        return
    
    lt, gt = _three_way_partition(arr, low, high)
    _quicksort_3way_helper(arr, low, lt - 1)
    _quicksort_3way_helper(arr, gt + 1, high)


def _three_way_partition(arr, low, high):
    """
    3-way partition: elements < pivot | elements = pivot | elements > pivot
    
    Returns:
        (lt, gt) where arr[low..lt-1] < pivot, arr[lt..gt] = pivot, arr[gt+1..high] > pivot
    """
    pivot = arr[low]
    lt = low       # arr[low..lt-1] < pivot
    i = low + 1    # arr[lt..i-1] = pivot
    gt = high + 1  # arr[gt..high] > pivot
    
    while i < gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            gt -= 1
            arr[i], arr[gt] = arr[gt], arr[i]
        else:
            i += 1
    
    return lt, gt - 1


def quickselect(arr, k):
    """
    Find the k-th smallest element using quickselect algorithm.
    
    Args:
        arr: List of comparable elements
        k: 1-based index of element to find (1 = smallest)
        
    Returns:
        The k-th smallest element
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k must be between 1 and {len(arr)}")
    
    arr_copy = arr.copy()
    return _quickselect_helper(arr_copy, 0, len(arr_copy) - 1, k - 1)


def _quickselect_helper(arr, low, high, k):
    """
    Recursive helper for quickselect.
    """
    if low == high:
        return arr[low]
    
    pivot_index = _lomuto_partition(arr, low, high)
    
    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        return _quickselect_helper(arr, low, pivot_index - 1, k)
    else:
        return _quickselect_helper(arr, pivot_index + 1, high, k)


def is_sorted(arr):
    """
    Check if array is sorted in ascending order.
    
    Args:
        arr: List to check
        
    Returns:
        True if sorted, False otherwise
    """
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def benchmark_quicksort_variants(arr):
    """
    Benchmark different quicksort implementations.
    
    Args:
        arr: Array to sort
        
    Returns:
        Dictionary with timing results
    """
    import time
    
    variants = {
        'Lomuto': quicksort,
        'Hoare': quicksort_hoare,
        'Iterative': quicksort_iterative,
        '3-way': quicksort_3way
    }
    
    results = {}
    
    for name, func in variants.items():
        start_time = time.perf_counter()
        sorted_arr = func(arr)
        end_time = time.perf_counter()
        
        # Verify correctness
        if not is_sorted(sorted_arr):
            results[name] = "FAILED - Not sorted correctly"
        else:
            results[name] = f"{end_time - start_time:.6f} seconds"
    
    return results


def demo():
    """
    Demonstration of quicksort implementations.
    """
    import random
    
    print("Quicksort Implementation Demo")
    print("=" * 40)
    
    # Test with small array
    small_arr = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Original array: {small_arr}")
    
    sorted_arr = quicksort(small_arr)
    print(f"Sorted (Lomuto): {sorted_arr}")
    print(f"Original unchanged: {small_arr}")
    print()
    
    # Test with duplicates
    dup_arr = [5, 2, 8, 2, 9, 1, 5, 5]
    print(f"Array with duplicates: {dup_arr}")
    print(f"3-way quicksort: {quicksort_3way(dup_arr)}")
    print()
    
    # Test quickselect
    test_arr = [3, 6, 8, 10, 1, 2, 1]
    for k in [1, 3, 5, 7]:
        kth = quickselect(test_arr, k)
        print(f"{k}-th smallest element in {test_arr}: {kth}")
    print()
    
    # Performance comparison
    print("Performance comparison (1000 random elements):")
    random_arr = [random.randint(1, 1000) for _ in range(1000)]
    results = benchmark_quicksort_variants(random_arr)
    for variant, time_result in results.items():
        print(f"{variant:12}: {time_result}")


if __name__ == "__main__":
    demo()