def bubble_sort(arr):
    """
    Sorts an array in ascending order using the bubble sort algorithm.
    
    Args:
        arr: List of comparable elements to be sorted
        
    Returns:
        The sorted list
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize by detecting if array is already sorted
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps occurred, array is sorted
        if not swapped:
            break
    
    return arr


# Example usage and testing
if __name__ == "__main__":
    # Test with various arrays
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 1, 4, 2, 8],
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [42],              # Single element
        [],                # Empty array
    ]
    
    for arr in test_arrays:
        original = arr.copy()
        sorted_arr = bubble_sort(arr)
        print(f"Original: {original}")
        print(f"Sorted:   {sorted_arr}")
        print()
