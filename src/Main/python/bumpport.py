def bump_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                # Swap the elements if they are in the wrong order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == "__main__":
    # Test the bump sort implementation
    input_list = list(map(int, input("Enter numbers separated by spaces: ").split()))
    print("Original list:", input_list)
    sorted_list = bump_sort(input_list)
    print("Sorted list:", sorted_list)