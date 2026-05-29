// Othello.java
// Simple Othello/Reversi game implementation in Java (console-based)
// Author: GitHub Copilot

import java.util.*;

public class Othello {
    private static final int SIZE = 8;
    private static final char EMPTY = '.';
    private static final char BLACK = 'B';
    private static final char WHITE = 'W';
    private char[][] board;
    private char currentPlayer;

    public Othello() {
        board = new char[SIZE][SIZE];
        for (char[] row : board) Arrays.fill(row, EMPTY);
        // Initial 4 pieces
        board[3][3] = WHITE;
        board[3][4] = BLACK;
        board[4][3] = BLACK;
        board[4][4] = WHITE;
        currentPlayer = BLACK;
    }

    public void printBoard() {
        System.out.print("  ");
        for (int i = 0; i < SIZE; i++) System.out.print(i + " ");
        System.out.println();
        for (int i = 0; i < SIZE; i++) {
            System.out.print(i + " ");
            for (int j = 0; j < SIZE; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }

    public boolean isValidMove(int row, int col, char player) {
        if (row < 0 || row >= SIZE || col < 0 || col >= SIZE || board[row][col] != EMPTY) return false;
        char opponent = (player == BLACK) ? WHITE : BLACK;
        int[] dx = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dy = {-1, 0, 1, -1, 1, -1, 0, 1};
        for (int d = 0; d < 8; d++) {
            int x = row + dx[d], y = col + dy[d];
            boolean foundOpponent = false;
            while (x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] == opponent) {
                x += dx[d];
                y += dy[d];
                foundOpponent = true;
            }
            if (foundOpponent && x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] == player) {
                return true;
            }
        }
        return false;
    }

    public boolean hasValidMove(char player) {
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (isValidMove(i, j, player)) return true;
            }
        }
        return false;
    }

    public void makeMove(int row, int col, char player) {
        board[row][col] = player;
        char opponent = (player == BLACK) ? WHITE : BLACK;
        int[] dx = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dy = {-1, 0, 1, -1, 1, -1, 0, 1};
        for (int d = 0; d < 8; d++) {
            int x = row + dx[d], y = col + dy[d];
            List<int[]> toFlip = new ArrayList<>();
            while (x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] == opponent) {
                toFlip.add(new int[]{x, y});
                x += dx[d];
                y += dy[d];
            }
            if (x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] == player) {
                for (int[] pos : toFlip) {
                    board[pos[0]][pos[1]] = player;
                }
            }
        }
    }

    public int countPieces(char player) {
        int count = 0;
        for (int i = 0; i < SIZE; i++)
            for (int j = 0; j < SIZE; j++)
                if (board[i][j] == player) count++;
        return count;
    }

    public void play() {
        Scanner scanner = new Scanner(System.in);
        while (hasValidMove(BLACK) || hasValidMove(WHITE)) {
            printBoard();
            if (!hasValidMove(currentPlayer)) {
                System.out.println("No valid moves for " + currentPlayer + ". Skipping turn.");
                currentPlayer = (currentPlayer == BLACK) ? WHITE : BLACK;
                continue;
            }
            System.out.println("Current player: " + currentPlayer);
            System.out.print("Enter row and column (e.g., 2 3): ");
            int row = scanner.nextInt();
            int col = scanner.nextInt();
            if (isValidMove(row, col, currentPlayer)) {
                makeMove(row, col, currentPlayer);
                currentPlayer = (currentPlayer == BLACK) ? WHITE : BLACK;
            } else {
                System.out.println("Invalid move. Try again.");
            }
        }
        printBoard();
        int blackCount = countPieces(BLACK);
        int whiteCount = countPieces(WHITE);
        System.out.println("Game over!");
        System.out.println("Black: " + blackCount + ", White: " + whiteCount);
        if (blackCount > whiteCount) System.out.println("Black wins!");
        else if (whiteCount > blackCount) System.out.println("White wins!");
        else System.out.println("It's a tie!");
    }

    public static void main(String[] args) {
        Othello game = new Othello();
        game.play();
    }
}
