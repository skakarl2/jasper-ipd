#include <iostream>
#include <vector>
#include <algorithm>

// Compare and swap two elements in the given direction
// direction: true = ascending, false = descending
void compAndSwap(std::vector<int>& arr, int i, int j, bool ascending) {
    if (ascending == (arr[i] > arr[j])) {
        std::swap(arr[i], arr[j]);
    }
}

// Merge a bitonic sequence starting at index lo of length cnt
void bitonicMerge(std::vector<int>& arr, int lo, int cnt, bool ascending) {
    if (cnt <= 1) return;

    int k = cnt / 2;
    for (int i = lo; i < lo + k; ++i) {
        compAndSwap(arr, i, i + k, ascending);
    }
    bitonicMerge(arr, lo, k, ascending);
    bitonicMerge(arr, lo + k, k, ascending);
}

// Recursively sort a bitonic sequence
void bitonicSort(std::vector<int>& arr, int lo, int cnt, bool ascending) {
    if (cnt <= 1) return;

    int k = cnt / 2;

    // Sort first half in ascending order to build the bitonic sequence
    bitonicSort(arr, lo, k, true);
    // Sort second half in descending order
    bitonicSort(arr, lo + k, k, false);
    // Merge the full bitonic sequence in the desired direction
    bitonicMerge(arr, lo, cnt, ascending);
}

// Public entry point — sorts arr in ascending order
// NOTE: array size must be a power of 2
void bitonicSort(std::vector<int>& arr) {
    bitonicSort(arr, 0, static_cast<int>(arr.size()), true);
}

int main() {
    std::vector<int> data = {3, 7, 4, 8, 6, 2, 1, 5};

    std::cout << "Before: ";
    for (int x : data) std::cout << x << " ";
    std::cout << "\n";

    bitonicSort(data);

    std::cout << "After:  ";
    for (int x : data) std::cout << x << " ";
    std::cout << "\n";

    return 0;
}
