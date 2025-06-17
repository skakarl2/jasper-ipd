def is_safe(board, row, col, n):
    # Directions: left, up-left, up, up-right, right, down-right, down, down-left
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        nr, nc = row+dr, col+dc
        if 0 <= nr < n and 0 <= nc < n:
            if board[nr][nc] == 1:
                return False
    return True

def solve_n_kings(n, row=0, placed=0, board=None, solutions=None):
    if board is None:
        board = [[0]*n for _ in range(n)]
    if solutions is None:
        solutions = []
    if placed == n:
        # Deep copy the board
        solutions.append([row[:] for row in board])
        return
    if row >= n:
        return
    for col in range(n):
        if is_safe(board, row, col, n):
            board[row][col] = 1
            solve_n_kings(n, row+1, placed+1, board, solutions)
            board[row][col] = 0
    solve_n_kings(n, row+1, placed, board, solutions)
    return solutions

# Example: Print all solutions for 3 kings
solutions = solve_n_kings(3)
for solution in solutions:
    for row in solution:
        print(row)
    print()