package tictac;

import java.util.Scanner;

public class TicTacToeCLI {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("=== Tic-Tac-Toe ===");

        while (true) {
            printMenu();
            int mode = readMode(scanner);
            if (mode == 0) {
                System.out.println("Goodbye.");
                break;
            }

            Player playerX;
            Player playerO;

            if (mode == 1) {
                playerX = new HumanPlayer(readName(scanner, "Enter name for Player X"), Mark.X);
                playerO = new HumanPlayer(readName(scanner, "Enter name for Player O"), Mark.O);
            } else if (mode == 2) {
                playerX = new HumanPlayer(readName(scanner, "Enter your name"), Mark.X);
                playerO = new ComputerPlayer("Computer", Mark.O, readDifficulty(scanner));
            } else {
                playerX = new ComputerPlayer("Computer X", Mark.X, readDifficulty(scanner, "Select difficulty for Computer X"));
                playerO = new ComputerPlayer("Computer O", Mark.O, readDifficulty(scanner, "Select difficulty for Computer O"));
            }

            TicTacToeGame game = new TicTacToeGame(playerX, playerO, scanner);
            game.playSession();
        }

        scanner.close();
    }

    private static void printMenu() {
        System.out.println("\nChoose mode:");
        System.out.println("1. Human vs Human");
        System.out.println("2. Human vs Computer");
        System.out.println("3. Computer vs Computer");
        System.out.println("0. Exit");
    }

    private static int readMode(Scanner scanner) {
        while (true) {
            System.out.print("Select option: ");
            String input = scanner.nextLine().trim();
            try {
                int value = Integer.parseInt(input);
                if (value >= 0 && value <= 3) {
                    return value;
                }
            } catch (NumberFormatException ex) {
                // continue prompt
            }
            System.out.println("Please enter 0, 1, 2, or 3.");
        }
    }

    private static String readName(Scanner scanner, String label) {
        while (true) {
            System.out.print(label + ": ");
            String name = scanner.nextLine().trim();
            if (!name.isEmpty()) {
                return name;
            }
            System.out.println("Name cannot be empty.");
        }
    }

    private static Difficulty readDifficulty(Scanner scanner) {
        return readDifficulty(scanner, "Select computer difficulty");
    }

    private static Difficulty readDifficulty(Scanner scanner, String title) {
        while (true) {
            System.out.println(title + ":");
            System.out.println("1. Easy");
            System.out.println("2. Medium");
            System.out.println("3. Hard");
            System.out.print("Choice: ");

            String input = scanner.nextLine().trim();
            if (input.equals("1")) {
                return Difficulty.EASY;
            }
            if (input.equals("2")) {
                return Difficulty.MEDIUM;
            }
            if (input.equals("3")) {
                return Difficulty.HARD;
            }
            System.out.println("Please choose 1, 2, or 3.");
        }
    }
}
