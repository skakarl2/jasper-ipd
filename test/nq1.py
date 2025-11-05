def solve_n_queens(n):
    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

    def solve(row, board, solutions):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(row + 1, board, solutions)

    solutions = []
    solve(0, [0]*n, solutions)
    return solutions

def print_solutions(solutions):
    for sol in solutions:
        for i in sol:
            print('.' * i + 'Q' + '.' * (len(sol) - i - 1))
        print()

if __name__ == "__main__":
    n = 8
    solutions = solve_n_queens(n)
    print(f"Number of solutions for {n}-Queens: {len(solutions)}")
    print_solutions(solutions[:3])  # Print first 3 solutions