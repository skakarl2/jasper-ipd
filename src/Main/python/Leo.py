def bump_sort(arr):
    """
    Sort list 'arr' in-place using a bump-sort style algorithm.
    This repeatedly scans left-to-right and swaps adjacent out-of-order items,
    continuing passes until no swaps are needed.

    Args:
        arr (list): mutable sequence of comparable items

    Returns:
        list: the same list object, sorted in ascending order
    """
    n = len(arr)
    if n < 2:
        return arr

    while True:
        swapped = False
        # Left-to-right pass: whenever arr[i] < arr[i-1], swap to "bump" it left
        for i in range(1, n):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                swapped = True
        if not swapped:
            break
    return arr


# Small self-test
if __name__ == "__main__":
    tests = [
        [],
        [1],
        [2, 1],
        [5, 3, 8, 1, 2],
        [3, 3, 2, 1, 4],
        list(range(10, 0, -1)),  # reversed
    ]
    for t in tests:
        original = t.copy()
        sorted_list = bump_sort(t)
        print(f"{original} -> {sorted_list}")