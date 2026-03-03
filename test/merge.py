def merge_sort(arr):
    """
    Perform merge sort on a list and return a new sorted list.
    Args:
        arr (list): The list to sort.
    Returns:
        list: A new sorted list.
    """
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted lists into a single sorted list.
    Args:
        left (list): First sorted list.
        right (list): Second sorted list.
    Returns:
        list: Merged sorted list.
    """
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


if __name__ == "__main__":
    # Example usage
    sample = [38, 27, 43, 3, 9, 82, 10]
    print("Original:", sample)
    print("Sorted:", merge_sort(sample))
