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

def print_solutions(solutions, n):
    for sol in solutions:
        for i in range(n):
            row = ['.']*n
            row[sol[i]] = 'Q'
            print(' '.join(row))
        print()

if __name__ == "__main__":
    n = 8  # Change n for different board sizes
    solutions = solve_n_queens(n)
    print(f"Total solutions for {n} queens: {len(solutions)}\n")
    print_solutions(solutions, n)