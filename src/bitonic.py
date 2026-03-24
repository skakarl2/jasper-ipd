def bitonic_sort(arr):
    """
    Perform a bitonic sort on the given array.

    :param arr: List of integers to sort
    :return: Sorted list of integers
    """
    def compare_and_swap(arr, i, j, direction):
        if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, direction)
            bitonic_merge(arr, low, k, direction)
            bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(arr, low, cnt, direction):
        if cnt > 1:
            k = cnt // 2
            bitonic_sort_recursive(arr, low, k, 1)  # Sort in ascending order
            bitonic_sort_recursive(arr, low + k, k, 0)  # Sort in descending order
            bitonic_merge(arr, low, cnt, direction)

    n = len(arr)
    bitonic_sort_recursive(arr, 0, n, 1)
    return arr

# Example usage
if __name__ == "__main__":
    sample_array = [3, 7, 4, 8, 6, 2, 1, 5]
    print("Original array:", sample_array)
    sorted_array = bitonic_sort(sample_array)
    print("Sorted array:", sorted_array)