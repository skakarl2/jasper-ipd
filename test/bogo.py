"""
Bogosort (Permutation Sort / Monkey Sort) Implementation

Bogosort is an extremely inefficient sorting algorithm that works by 
randomly shuffling the elements until they happen to be in sorted order.

Time Complexity:
- Best Case: O(n) - if the array is already sorted
- Average Case: O(n!) - factorial time
- Worst Case: Unbounded - theoretically could run forever

This is primarily used as an educational example of what NOT to do
when designing algorithms, though it's interesting from a probabilistic
perspective.
"""

import random
import time
from typing import List, Union


def is_sorted(arr: List[Union[int, float]]) -> bool:
    """
    Check if an array is sorted in ascending order.
    
    Args:
        arr: List of comparable elements
        
    Returns:
        True if array is sorted, False otherwise
    """
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def shuffle_array(arr: List[Union[int, float]]) -> None:
    """
    Randomly shuffle array in-place using Fisher-Yates shuffle.
    
    Args:
        arr: List to shuffle (modified in-place)
    """
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def bogosort(arr: List[Union[int, float]], max_iterations: int = None, verbose: bool = False) -> List[Union[int, float]]:
    """
    Sort an array using the Bogosort algorithm.
    
    Args:
        arr: List of comparable elements to sort
        max_iterations: Maximum number of shuffles to attempt (None = unlimited)
        verbose: If True, print progress
        
    Returns:
        Sorted copy of the input array
        
    Raises:
        RuntimeError: If max_iterations is reached without finding solution
    """
    # Work on a copy to avoid modifying the original
    result = arr.copy()
    iterations = 0
    
    if verbose:
        print(f"Starting Bogosort on array: {result}")
    
    # Keep shuffling until sorted
    while not is_sorted(result):
        iterations += 1
        
        # Check iteration limit
        if max_iterations and iterations > max_iterations:
            raise RuntimeError(f"Bogosort failed to sort after {max_iterations} iterations")
        
        if verbose:
            print(f"Iteration {iterations}: {result} - not sorted, shuffling...")
        
        shuffle_array(result)
    
    if verbose:
        print(f"Success! Sorted in {iterations} iterations: {result}")
    
    return result


def bogosort_with_stats(arr: List[Union[int, float]]) -> tuple:
    """
    Sort using Bogosort and return statistics.
    
    Args:
        arr: List to sort
        
    Returns:
        Tuple of (sorted_array, iterations, time_taken)
    """
    result = arr.copy()
    iterations = 0
    start_time = time.time()
    
    while not is_sorted(result):
        iterations += 1
        shuffle_array(result)
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    return result, iterations, time_taken


def demonstrate_bogosort():
    """
    Demonstrate Bogosort with various examples.
    """
    print("=" * 50)
    print("BOGOSORT DEMONSTRATION")
    print("=" * 50)
    
    # Test cases - start small!
    test_cases = [
        [3, 1, 2],
        [5, 4, 3, 2, 1],
        [1, 3, 2, 4],
        [42, 17, 99, 3, 88],
        [7]  # Single element
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case}")
        
        try:
            # Use max_iterations to prevent infinite loops on unlucky runs
            max_iter = 50000 if len(test_case) <= 4 else 100000
            
            sorted_arr, iterations, time_taken = bogosort_with_stats(test_case)
            
            print(f"Original:  {test_case}")
            print(f"Sorted:    {sorted_arr}")
            print(f"Iterations: {iterations:,}")
            print(f"Time:      {time_taken:.4f} seconds")
            
            # Verify it's actually sorted
            expected = sorted(test_case)
            if sorted_arr == expected:
                print("✅ Correct!")
            else:
                print(f"❌ Error! Expected {expected}")
                
        except RuntimeError as e:
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("⏹️ Interrupted by user")
            break


def factorial_time_warning():
    """
    Warn about the extreme inefficiency of Bogosort.
    """
    print("\n" + "⚠️" * 20)
    print("WARNING: BOGOSORT IS EXTREMELY INEFFICIENT!")
    print("⚠️" * 20)
    print("Expected iterations for different array sizes:")
    
    import math
    for n in range(1, 8):
        expected_iterations = math.factorial(n)
        print(f"  {n} elements: ~{expected_iterations:,} iterations on average")
    
    print("\nDo NOT use this on arrays larger than 7-8 elements!")
    print("Even 10 elements could take 3.6 million iterations on average!")
    print("For anything serious, use quicksort, mergesort, or Python's built-in sort().")


if __name__ == "__main__":
    # Show the warning first
    factorial_time_warning()
    
    # Ask user if they want to proceed
    print("\nDo you want to see the demonstration? (y/n): ", end="")
    response = input().strip().lower()
    
    if response in ['y', 'yes']:
        demonstrate_bogosort()
    else:
        print("Wise choice! 😄")
        
    # Quick test with a tiny array
    print("\nQuick test with [3, 1, 2]:")
    result = bogosort([3, 1, 2], verbose=True)
    print(f"Final result: {result}")