package connectfour;

import java.util.Scanner;

public class ConnectFourGame {
    private static final int ROWS = 6;
    private static final int COLUMNS = 7;
    private static final int CONNECT_LENGTH = 4;

    private final Disc[][] board;

    public ConnectFourGame() {
        this.board = new Disc[ROWS][COLUMNS];
    }

    public static void main(String[] args) {
        ConnectFourGame game = new ConnectFourGame();

        System.out.println("Welcome to Connect Four!");
        System.out.println("Choose a column from 1 to 7. Type 'quit' to exit.\n");

        try (Scanner scanner = new Scanner(System.in)) {
            Disc currentPlayer = Disc.RED;

            while (true) {
                game.printBoard();
                System.out.println();
                System.out.print(currentPlayer.getDisplayName() + " to move. Select a column: ");

                String input = scanner.nextLine().trim();
                if (input.equalsIgnoreCase("quit")) {
                    System.out.println("Thanks for playing!");
                    return;
                }

                int column;
                try {
                    column = Integer.parseInt(input) - 1;
                } catch (NumberFormatException error) {
                    System.out.println("Please enter a number from 1 to 7.\n");
                    continue;
                }

                if (!game.isValidColumn(column)) {
                    System.out.println("Column must be between 1 and 7.\n");
                    continue;
                }

                int row = game.dropDisc(column, currentPlayer);
                if (row == -1) {
                    System.out.println("That column is full. Try another one.\n");
                    continue;
                }

                if (game.hasConnectFour(row, column, currentPlayer)) {
                    game.printBoard();
                    System.out.println();
                    System.out.println(currentPlayer.getDisplayName() + " wins!");
                    return;
                }

                if (game.isBoardFull()) {
                    game.printBoard();
                    System.out.println();
                    System.out.println("The game is a draw!");
                    return;
                }

                currentPlayer = currentPlayer.opponent();
                System.out.println();
            }
        }
    }

    private void printBoard() {
        System.out.println("  1 2 3 4 5 6 7");
        for (int row = 0; row < ROWS; row++) {
            System.out.print("|");
            for (int col = 0; col < COLUMNS; col++) {
                Disc disc = board[row][col];
                char symbol = disc == null ? '.' : disc.getSymbol();
                System.out.print(symbol + "|");
            }
            System.out.println();
        }
        System.out.println("+-------------+");
    }

    private boolean isValidColumn(int column) {
        return column >= 0 && column < COLUMNS;
    }

    private int dropDisc(int column, Disc player) {
        for (int row = ROWS - 1; row >= 0; row--) {
            if (board[row][column] == null) {
                board[row][column] = player;
                return row;
            }
        }
        return -1;
    }

    private boolean isBoardFull() {
        for (int col = 0; col < COLUMNS; col++) {
            if (board[0][col] == null) {
                return false;
            }
        }
        return true;
    }

    private boolean hasConnectFour(int row, int col, Disc player) {
        return countConnected(row, col, 0, 1, player) >= CONNECT_LENGTH
            || countConnected(row, col, 1, 0, player) >= CONNECT_LENGTH
            || countConnected(row, col, 1, 1, player) >= CONNECT_LENGTH
            || countConnected(row, col, 1, -1, player) >= CONNECT_LENGTH;
    }

    private int countConnected(int row, int col, int rowStep, int colStep, Disc player) {
        int total = 1;
        total += countDirection(row, col, rowStep, colStep, player);
        total += countDirection(row, col, -rowStep, -colStep, player);
        return total;
    }

    private int countDirection(int row, int col, int rowStep, int colStep, Disc player) {
        int count = 0;
        int nextRow = row + rowStep;
        int nextCol = col + colStep;

        while (isInside(nextRow, nextCol) && board[nextRow][nextCol] == player) {
            count++;
            nextRow += rowStep;
            nextCol += colStep;
        }

        return count;
    }

    private boolean isInside(int row, int col) {
        return row >= 0 && row < ROWS && col >= 0 && col < COLUMNS;
    }

    private enum Disc {
        RED('R'),
        YELLOW('Y');

        private final char symbol;

        Disc(char symbol) {
            this.symbol = symbol;
        }

        public char getSymbol() {
            return symbol;
        }

        public String getDisplayName() {
            return name();
        }

        public Disc opponent() {
            return this == RED ? YELLOW : RED;
        }
    }
}