package checkers;

import java.util.Scanner;

public class CheckersGame {
    public static void main(String[] args) {
        CheckersBoard board = new CheckersBoard();
        board.initialize();

        try (Scanner scanner = new Scanner(System.in)) {
            CheckersPlayer currentPlayer = CheckersPlayer.RED;
            boolean gameRunning = true;

            System.out.println("Welcome to Checkers!");
            System.out.println("Enter moves in the format 'b6 a5'. Type 'quit' to exit.\n");
            System.out.println("Red moves first. Captures are mandatory, and multi-jumps must be completed.\n");

            while (gameRunning) {
                board.printBoard();
                System.out.println();

                CheckersPosition forced = board.getForcedContinuation();
                if (forced != null) {
                    System.out.println(currentPlayer + " must continue jumping with " + forced + ".");
                } else {
                    System.out.println(currentPlayer + " to move.");
                }
                System.out.println("Enter your move:");

                String input = scanner.nextLine().trim();
                if (input.equalsIgnoreCase("quit")) {
                    System.out.println("Thanks for playing!");
                    break;
                }

                String[] parts = input.split("\\s+");
                if (parts.length != 2) {
                    System.out.println("Invalid format. Use moves like 'b6 a5'.\n");
                    continue;
                }

                try {
                    CheckersPosition from = CheckersPosition.fromString(parts[0]);
                    CheckersPosition to = CheckersPosition.fromString(parts[1]);
                    CheckersMoveResult result = board.move(from, to, currentPlayer);

                    System.out.println(result.getMessage());
                    System.out.println();

                    if (!result.isSuccess()) {
                        continue;
                    }
                    if (result.isGameOver()) {
                        board.printBoard();
                        gameRunning = false;
                        continue;
                    }
                    if (result.isTurnComplete()) {
                        currentPlayer = currentPlayer.opponent();
                    }
                } catch (IllegalArgumentException error) {
                    System.out.println(error.getMessage());
                    System.out.println();
                }
            }
        }
    }
}