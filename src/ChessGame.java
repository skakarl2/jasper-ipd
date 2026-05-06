package chess;

import java.util.Scanner;

public class ChessGame {
    public static void main(String[] args) {
        Board board = new Board();
        board.initialize();
        
        Scanner scanner = new Scanner(System.in);
        boolean gameRunning = true;
        Player currentPlayer = Player.WHITE;

        System.out.println("Welcome to Chess!");
        System.out.println("Enter moves in the format 'a2 a4' (from-to in algebraic notation)\n");

        while (gameRunning) {
            board.printBoard();

            String status = "";
            if (board.isInCheck(currentPlayer)) {
                status = " [CHECK!]";
            }
            System.out.println("\n" + currentPlayer + "'s turn" + status + ". Enter your move (e.g., e2 e4):");

            try {
                String move = scanner.nextLine().trim();
                
                if (move.equalsIgnoreCase("quit")) {
                    System.out.println("Thanks for playing!");
                    gameRunning = false;
                    break;
                }

                String[] parts = move.split(" ");
                if (parts.length != 2) {
                    System.out.println("Invalid format. Please use: 'e2 e4'\n");
                    continue;
                }

                Position from = Position.fromString(parts[0]);
                Position to = Position.fromString(parts[1]);

                if (board.movePiece(from, to, currentPlayer)) {
                    // Check game end conditions
                    Player opponent = currentPlayer.opponent();
                    
                    if (board.isCheckmate(opponent)) {
                        board.printBoard();
                        System.out.println("\n" + currentPlayer + " wins by checkmate!");
                        gameRunning = false;
                    } else if (board.isStalemate(opponent)) {
                        board.printBoard();
                        System.out.println("\nGame ends in stalemate!");
                        gameRunning = false;
                    } else {
                        currentPlayer = opponent;
                        System.out.println();
                    }
                } else {
                    System.out.println("Invalid move. Try again.\n");
                }
            } catch (IllegalArgumentException e) {
                System.out.println("Error: " + e.getMessage());
                System.out.println("Use algebraic notation (a1-h8). Try again.\n");
            } catch (Exception e) {
                System.out.println("Invalid input: " + e.getMessage());
                System.out.println("Please use the format 'e2 e4'.\n");
            }
        }

        scanner.close();
    }
}