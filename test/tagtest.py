def is_safe(board, row, col, n):
    # Directions a king can attack (8 directions)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < n and 0 <= c < n and board[r][c] == 1:
            return False
    return True

def solve_n_kings(n):
    solutions = []
    board = [[0 for _ in range(n)] for _ in range(n)]

    def backtrack(row, placed):
        if placed == n:
            # Deep copy the board
            solutions.append([row[:] for row in board])
            return
        if row >= n:
            return
        for col in range(n):
            if is_safe(board, row, col, n):
                board[row][col] = 1
                backtrack(row + 1, placed + 1)
                board[row][col] = 0
        # Optionally skip placing a king in this row
        backtrack(row + 1, placed)

    backtrack(0, 0)
    return solutions

def print_boards(solutions):
    for idx, board in enumerate(solutions):
        print(f"Solution {idx+1}:")
        for row in board:
            print(' '.join('K' if cell else '.' for cell in row))
        print()

if __name__ == "__main__":
    n = 4  # Change n as needed
    solutions = solve_n_kings(n)
    print(f"Total solutions for {n} kings: {len(solutions)}")
    print_boards(solutions)