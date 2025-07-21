def solve_nqueens(n):
    def is_safe(queens, row, col):
        for r, c in enumerate(queens):
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def place_queens(row, queens, results):
        if row == n:
            results.append(queens[:])
            return
        for col in range(n):
            if is_safe(queens, row, col):
                queens.append(col)
                place_queens(row + 1, queens, results)
                queens.pop()

    results = []
    place_queens(0, [], results)
    for solution in results:
        for col in solution:
            print(''.join('Q' if i == col else '.' for i in range(n)))
        print()
    print(f"Total solutions: {len(results)}")

# Example usage:
solve_nqueens(8)