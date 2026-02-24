def bubble_sort(arr):
    """
    Implements the bubble sort algorithm to sort an array in ascending order.
    
    Bubble sort works by repeatedly stepping through the list, comparing adjacent
    elements and swapping them if they are in the wrong order. The pass through
    the list is repeated until the list is sorted.
    
    Time Complexity: O(n²) in worst and average case, O(n) in best case
    Space Complexity: O(1) - sorts in place
    
    Args:
        arr (list): List of comparable elements to be sorted
        
    Returns:
        list: The sorted array (modifies the original array)
    """
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Track if any swaps were made in this pass
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swapping occurred, the array is already sorted
        if not swapped:
            break
    
    return arr


def bubble_sort_descending(arr):
    """
    Bubble sort implementation for descending order.
    
    Args:
        arr (list): List of comparable elements to be sorted
        
    Returns:
        list: The sorted array in descending order
    """
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            # Change comparison for descending order
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    return arr


def bubble_sort_verbose(arr):
    """
    Bubble sort with step-by-step output for educational purposes.
    
    Args:
        arr (list): List of comparable elements to be sorted
        
    Returns:
        list: The sorted array
    """
    n = len(arr)
    print(f"Starting bubble sort on: {arr}")
    
    for i in range(n):
        swapped = False
        print(f"\nPass {i + 1}:")
        
        for j in range(0, n - i - 1):
            print(f"  Comparing {arr[j]} and {arr[j + 1]}", end="")
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(f" -> Swapped! Array: {arr}")
            else:
                print(" -> No swap needed")
        
        if not swapped:
            print(f"  No swaps made in pass {i + 1}. Array is sorted!")
            break
        else:
            print(f"  End of pass {i + 1}: {arr}")
    
    print(f"\nFinal sorted array: {arr}")
    return arr


if __name__ == "__main__":
    # Example usage and testing
    print("=== Bubble Sort Demo ===")
    
    # Test case 1: Random integers
    test_arr1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nOriginal array: {test_arr1}")
    sorted_arr1 = bubble_sort(test_arr1.copy())
    print(f"Sorted ascending: {sorted_arr1}")
    
    # Test case 2: Already sorted array
    test_arr2 = [1, 2, 3, 4, 5]
    print(f"\nAlready sorted array: {test_arr2}")
    sorted_arr2 = bubble_sort(test_arr2.copy())
    print(f"Still sorted: {sorted_arr2}")
    
    # Test case 3: Reverse sorted array
    test_arr3 = [5, 4, 3, 2, 1]
    print(f"\nReverse sorted array: {test_arr3}")
    sorted_arr3 = bubble_sort(test_arr3.copy())
    print(f"Now ascending: {sorted_arr3}")
    
    # Test case 4: Descending sort
    test_arr4 = [3, 7, 1, 9, 4]
    print(f"\nDescending sort test: {test_arr4}")
    desc_sorted = bubble_sort_descending(test_arr4.copy())
    print(f"Sorted descending: {desc_sorted}")
    
    # Test case 5: Verbose mode (small array)
    test_arr5 = [5, 2, 8, 1]
    print(f"\n=== Verbose Mode Demo ===")
    bubble_sort_verbose(test_arr5.copy())