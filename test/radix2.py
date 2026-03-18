def radix_sort(arr):
    if not arr:
        return arr

    # Find the maximum number to know the number of digits
    max_num = max(arr)
    exp = 1
    n = len(arr)
    output = [0] * n

    while max_num // exp > 0:
        count = [0] * 10

        # Store count of occurrences in count[]
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        # Change count[i] so that count[i] contains actual position
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array
        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        # Copy the output array to arr[]
        for i in range(n):
            arr[i] = output[i]

        exp *= 10
    return arr

if __name__ == "__main__":
    # Example usage
    data = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Original array:", data)
    radix_sort(data)
    print("Sorted array:", data)
