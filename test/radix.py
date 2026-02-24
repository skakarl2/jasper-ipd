"""
Fresh implementation of Radix Sort Algorithm
============================================

Radix sort is a non-comparison sorting algorithm that sorts integers by 
processing individual digits. It works by sorting the elements digit by digit,
starting from the least significant digit to the most significant digit.

Time Complexity: O(d * (n + k))
- d: number of digits in the largest number
- n: number of elements
- k: range of each digit (10 for decimal)

Space Complexity: O(n + k)
"""


def counting_sort_by_digit(arr, exp):
    """
    Counting sort function used by radix sort to sort elements based on a specific digit.
    
    Args:
        arr: List of integers to sort
        exp: The exponent representing which digit position to sort by (1, 10, 100, etc.)
    
    Returns:
        None (sorts in-place by modifying the original array)
    """
    n = len(arr)
    output = [0] * n  # Output array to store sorted elements
    count = [0] * 10  # Count array for digits 0-9
    
    # Count occurrences of each digit at the exp position
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # Modify count array to contain actual positions in output array
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array by placing elements in correct positions
    # Process from right to left to maintain stability
    i = n - 1
    while i >= 0:
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
        i -= 1
    
    # Copy sorted elements back to original array
    for i in range(n):
        arr[i] = output[i]


def radix_sort_positive(arr):
    """
    Radix sort implementation for positive integers.
    
    Args:
        arr: List of positive integers to sort
    
    Returns:
        None (sorts in-place)
    """
    if not arr:
        return
    
    # Find the maximum number to determine number of digits
    max_num = max(arr)
    
    # Sort by each digit, starting from least significant
    exp = 1
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10


def radix_sort(arr):
    """
    Main radix sort function that handles both positive and negative numbers.
    
    Args:
        arr: List of integers to sort
    
    Returns:
        List: New sorted list (original list remains unchanged)
    """
    if not arr:
        return []
    
    # Create a copy to avoid modifying the original array
    sorted_arr = arr.copy()
    
    # Separate negative and positive numbers
    negative_nums = []
    non_negative_nums = []
    
    for num in sorted_arr:
        if num < 0:
            negative_nums.append(-num)  # Store absolute value
        else:
            non_negative_nums.append(num)
    
    # Sort negative numbers (as positive) and positive numbers separately
    if negative_nums:
        radix_sort_positive(negative_nums)
        # Convert back to negative and reverse order
        negative_nums = [-num for num in reversed(negative_nums)]
    
    if non_negative_nums:
        radix_sort_positive(non_negative_nums)
    
    # Combine results: negatives first, then non-negatives
    return negative_nums + non_negative_nums


def radix_sort_inplace(arr):
    """
    In-place version of radix sort.
    
    Args:
        arr: List of integers to sort in-place
    """
    if not arr:
        return
    
    sorted_result = radix_sort(arr)
    arr.clear()
    arr.extend(sorted_result)


def get_max_digits(arr):
    """
    Helper function to get the maximum number of digits in the array.
    
    Args:
        arr: List of integers
    
    Returns:
        int: Maximum number of digits
    """
    if not arr:
        return 0
    
    max_num = max(abs(num) for num in arr)
    digits = 0
    while max_num > 0:
        digits += 1
        max_num //= 10
    
    return max(digits, 1)  # At least 1 digit for zero


def demo_radix_sort():
    """
    Demonstration function showing various radix sort examples.
    """
    print("=== Radix Sort Demo ===\n")
    
    # Test case 1: Basic positive numbers
    test1 = [170, 45, 75, 90, 2, 802, 24, 66]
    print(f"Test 1 - Original: {test1}")
    result1 = radix_sort(test1)
    print(f"Test 1 - Sorted:   {result1}")
    print(f"Max digits: {get_max_digits(test1)}\n")
    
    # Test case 2: Numbers with negative values
    test2 = [-5, 3, -2, 8, -1, 0, 4, -9, 7]
    print(f"Test 2 - Original: {test2}")
    result2 = radix_sort(test2)
    print(f"Test 2 - Sorted:   {result2}")
    print(f"Max digits: {get_max_digits(test2)}\n")
    
    # Test case 3: Large numbers
    test3 = [432, 8, 530, 90, 88, 231, 11, 45, 677, 199]
    print(f"Test 3 - Original: {test3}")
    result3 = radix_sort(test3)
    print(f"Test 3 - Sorted:   {result3}")
    print(f"Max digits: {get_max_digits(test3)}\n")
    
    # Test case 4: Numbers with varying digit counts
    test4 = [1, 23, 456, 7890, 12345, 6, 78, 901]
    print(f"Test 4 - Original: {test4}")
    result4 = radix_sort(test4)
    print(f"Test 4 - Sorted:   {result4}")
    print(f"Max digits: {get_max_digits(test4)}\n")
    
    # Test case 5: In-place sorting
    test5 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Test 5 - Original: {test5}")
    radix_sort_inplace(test5)
    print(f"Test 5 - In-place: {test5}")
    print(f"Max digits: {get_max_digits(test5)}\n")
    
    # Test case 6: Edge cases
    edge_cases = [
        [],  # Empty list
        [5],  # Single element
        [0, 0, 0],  # All zeros
        [-1, -1, -1],  # All same negative
        [100, 100, 100],  # All same positive
    ]
    
    print("=== Edge Cases ===")
    for i, case in enumerate(edge_cases, 1):
        original = case.copy()
        result = radix_sort(case)
        print(f"Edge {i} - Original: {original}")
        print(f"Edge {i} - Sorted:   {result}")
        print(f"Edge {i} - Max digits: {get_max_digits(original)}\n")


def benchmark_radix_sort():
    """
    Simple benchmark comparing radix sort with Python's built-in sort.
    """
    import random
    import time
    
    print("=== Performance Benchmark ===\n")
    
    # Generate random test data
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        # Generate random integers
        test_data = [random.randint(-9999, 9999) for _ in range(size)]
        
        # Test radix sort
        start_time = time.time()
        radix_result = radix_sort(test_data)
        radix_time = time.time() - start_time
        
        # Test Python's built-in sort
        start_time = time.time()
        python_result = sorted(test_data)
        python_time = time.time() - start_time
        
        # Verify results are the same
        results_match = radix_result == python_result
        
        print(f"Size: {size:,}")
        print(f"Radix Sort:    {radix_time:.6f} seconds")
        print(f"Python Sort:   {python_time:.6f} seconds")
        print(f"Ratio:         {radix_time / python_time:.2f}x")
        print(f"Results match: {results_match}")
        print("-" * 40)


if __name__ == "__main__":
    # Run demonstration
    demo_radix_sort()
    
    # Run benchmark
    benchmark_radix_sort()
    
    print("\n=== Radix Sort Implementation Complete ===")
    print("Features:")
    print("- Handles positive and negative integers")
    print("- In-place and copy-based versions")
    print("- Comprehensive test cases")
    print("- Performance benchmarking")
    print("- Well-documented with examples")