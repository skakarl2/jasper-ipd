def print_board(board):
    print("  " + " ".join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(i, " ".join(row))
    print()

def opponent(player):
    return 'B' if player == 'W' else 'W'

def in_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_moves(board, player):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    moves = set()
    for x in range(8):
        for y in range(8):
            if board[x][y] != '.':
                continue
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                found_opponent = False
                while in_board(nx, ny) and board[nx][ny] == opponent(player):
                    nx += dx
                    ny += dy
                    found_opponent = True
                if found_opponent and in_board(nx, ny) and board[nx][ny] == player:
                    moves.add((x, y))
    return moves

def make_move(board, player, x, y):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1)]
    board[x][y] = player
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flips = []
        while in_board(nx, ny) and board[nx][ny] == opponent(player):
            flips.append((nx, ny))
            nx += dx
            ny += dy
        if flips and in_board(nx, ny) and board[nx][ny] == player:
            for fx, fy in flips:
                board[fx][fy] = player

def count_discs(board):
    blacks = sum(row.count('B') for row in board)
    whites = sum(row.count('W') for row in board)
    return blacks, whites

def main():
    board = [['.']*8 for _ in range(8)]
    board[3][3], board[4][4] = 'W', 'W'
    board[3][4], board[4][3] = 'B', 'B'
    player = 'B'
    while True:
        print_board(board)
        moves = valid_moves(board, player)
        if not moves:
            if not valid_moves(board, opponent(player)):
                break
            print(f"Player {player} has no valid moves. Passing turn.")
            player = opponent(player)
            continue
        print(f"Player {player}'s turn. Valid moves: {moves}")
        move = None
        while move not in moves:
            move_input = input(f"Enter your move as 'row col': ")
            try:
                x, y = map(int, move_input.strip().split())
                move = (x, y)
                if move not in moves:
                    print("Invalid move.")
            except Exception:
                print("Invalid input.")
        make_move(board, player, *move)
        player = opponent(player)
    print_board(board)
    blacks, whites = count_discs(board)
    print(f"Game over! Black: {blacks}  White: {whites}")
    if blacks > whites:
        print("Black wins!")
    elif whites > blacks:
        print("White wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()