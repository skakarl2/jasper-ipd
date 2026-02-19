def solve_n_queens(n):
    """
    Solves the N-Queens problem and returns all distinct solutions.
    Each solution is represented as a list of column indices for each row.
    """
    def is_safe(queens, row, col):
        for r, c in enumerate(queens):
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def backtrack(row, queens, solutions):
        if row == n:
            solutions.append(queens[:])
            return
        for col in range(n):
            if is_safe(queens, row, col):
                queens.append(col)
                backtrack(row + 1, queens, solutions)
                queens.pop()

    solutions = []
    backtrack(0, [], solutions)
    return solutions


def print_solutions(solutions):
    for sol in solutions:
        for col in sol:
            print('.' * col + 'Q' + '.' * (len(sol) - col - 1))
        print()


def main():
    n = 8  # Change this value for different board sizes
    solutions = solve_n_queens(n)
    print(f"Number of solutions for {n}-Queens: {len(solutions)}\n")
    print_solutions(solutions[:3])  # Print first 3 solutions as example


if __name__ == "__main__":
    main()
