package chess;

import java.util.Scanner;

public class ChessGame {
    public static void main(String[] args) {
        Board board = new Board();
        board.initialize();
        
        Scanner scanner = new Scanner(System.in);
        boolean gameRunning = true;
        Player currentPlayer = Player.WHITE;

        while (gameRunning) {
            System.out.println("Current board:");
            board.printBoard();

            System.out.println(currentPlayer + "'s turn. Enter your move (e.g., e2 e4): ");
            String move = scanner.nextLine();

            try {
                String[] parts = move.split(" ");
                Position from = Position.fromString(parts[0]);
                Position to = Position.fromString(parts[1]);

                if (board.movePiece(from, to, currentPlayer)) {
                    if (board.isCheckmate(currentPlayer.opponent())) {
                        System.out.println(currentPlayer + " wins by checkmate!");
                        gameRunning = false;
                    } else {
                        currentPlayer = currentPlayer.opponent();
                    }
                } else {
                    System.out.println("Invalid move. Try again.");
                }
            } catch (Exception e) {
                System.out.println("Invalid input. Please use the format 'e2 e4'.");
            }
        }

        scanner.close();
    }
}