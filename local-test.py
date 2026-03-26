def merge_sort(data):
    """
    Sorts a list of integers using the merge sort algorithm.

    Parameters:
    - data (list): The list to be sorted.

    Returns:
    - sorted_data (list): The sorted list.
    """
    if len(data) <= 1:
        return data  # Base case: a single element is already sorted

    # Split the list into two halves
    midpoint = len(data) // 2
    left_half = data[:midpoint]  # Left portion
    right_half = data[midpoint:]  # Right portion

    # Recursively sort both halves
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # Merge the sorted halves
    combined = merge(sorted_left, sorted_right)

    # Debugging: Print the intermediate steps
    print(f"Merging: {sorted_left} and {sorted_right} -> {combined}")

    return combined

# Placeholder for the merge function (to be implemented)
def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.

    Parameters:
    - left (list): The first sorted list.
    - right (list): The second sorted list.

    Returns:
    - merged_list (list): The merged sorted list.
    """
    result = []
    i, j = 0, 0

    # Merge the two lists while maintaining sorted order
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])

    return result
