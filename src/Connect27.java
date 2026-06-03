import java.util.Scanner;

public class Connect27 {
    private static final int ROWS = 27;
    private static final int COLS = 27;
    private static final int CONNECT = 27;
    private static final char EMPTY = '.';
    private static final char PLAYER_ONE = 'X';
    private static final char PLAYER_TWO = 'O';

    private final char[][] board;
    private char currentPlayer;

    public Connect27() {
        board = new char[ROWS][COLS];
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                board[row][col] = EMPTY;
            }
        }
        currentPlayer = PLAYER_ONE;
    }

    public static void main(String[] args) {
        Connect27 game = new Connect27();
        game.play();
    }

    public void play() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            printBoard();
            int column = promptForColumn(scanner);
            int placedRow = dropPiece(column, currentPlayer);

            if (hasConnect(placedRow, column, currentPlayer)) {
                printBoard();
                System.out.println("Player " + currentPlayer + " wins!");
                break;
            }

            if (isBoardFull()) {
                printBoard();
                System.out.println("The board is full. It's a draw!");
                break;
            }

            currentPlayer = (currentPlayer == PLAYER_ONE) ? PLAYER_TWO : PLAYER_ONE;
        }
    }

    private void printBoard() {
        System.out.println();
        System.out.print("   ");
        for (int col = 1; col <= COLS; col++) {
            System.out.printf("%2d ", col);
        }
        System.out.println();

        for (int row = 0; row < ROWS; row++) {
            System.out.printf("%2d ", row + 1);
            for (int col = 0; col < COLS; col++) {
                System.out.print(" " + board[row][col] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    private int promptForColumn(Scanner scanner) {
        while (true) {
            System.out.print("Player " + currentPlayer + ", choose a column (1-" + COLS + "): ");
            String input = scanner.nextLine().trim();

            int column;
            try {
                column = Integer.parseInt(input) - 1;
            } catch (NumberFormatException ex) {
                System.out.println("Invalid input. Please enter a number.");
                continue;
            }

            if (column < 0 || column >= COLS) {
                System.out.println("Column out of range. Try again.");
                continue;
            }

            if (board[0][column] != EMPTY) {
                System.out.println("That column is full. Try another one.");
                continue;
            }

            return column;
        }
    }

    private int dropPiece(int column, char player) {
        for (int row = ROWS - 1; row >= 0; row--) {
            if (board[row][column] == EMPTY) {
                board[row][column] = player;
                return row;
            }
        }
        return -1;
    }

    private boolean hasConnect(int row, int col, char player) {
        return countInDirection(row, col, 0, 1, player) >= CONNECT
            || countInDirection(row, col, 1, 0, player) >= CONNECT
            || countInDirection(row, col, 1, 1, player) >= CONNECT
            || countInDirection(row, col, 1, -1, player) >= CONNECT;
    }

    private int countInDirection(int row, int col, int deltaRow, int deltaCol, char player) {
        int count = 1;
        count += countOneSide(row, col, deltaRow, deltaCol, player);
        count += countOneSide(row, col, -deltaRow, -deltaCol, player);
        return count;
    }

    private int countOneSide(int row, int col, int deltaRow, int deltaCol, char player) {
        int count = 0;
        int currentRow = row + deltaRow;
        int currentCol = col + deltaCol;

        while (isInsideBoard(currentRow, currentCol) && board[currentRow][currentCol] == player) {
            count++;
            currentRow += deltaRow;
            currentCol += deltaCol;
        }

        return count;
    }

    private boolean isInsideBoard(int row, int col) {
        return row >= 0 && row < ROWS && col >= 0 && col < COLS;
    }

    private boolean isBoardFull() {
        for (int col = 0; col < COLS; col++) {
            if (board[0][col] == EMPTY) {
                return false;
            }
        }
        return true;
    }
}