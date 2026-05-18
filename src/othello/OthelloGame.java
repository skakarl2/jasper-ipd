package othello;

import java.util.Scanner;

public class OthelloGame {
    public static void main(String[] args) {
        OthelloBoard board = new OthelloBoard();
        board.initialize();

        System.out.println("Welcome to Othello!");
        System.out.println("Enter moves like 'd3'. Type 'quit' to exit.\n");

        try (Scanner scanner = new Scanner(System.in)) {
            OthelloPlayer currentPlayer = OthelloPlayer.BLACK;

            while (!board.isBoardFull()) {
                boolean currentCanMove = board.hasAnyLegalMove(currentPlayer);
                boolean opponentCanMove = board.hasAnyLegalMove(currentPlayer.opponent());

                if (!currentCanMove && !opponentCanMove) {
                    break;
                }

                if (!currentCanMove) {
                    System.out.println(currentPlayer + " has no legal moves and must pass.\n");
                    currentPlayer = currentPlayer.opponent();
                    continue;
                }

                board.printBoard();
                System.out.println();
                System.out.println("Score - BLACK: " + board.countPieces(OthelloPlayer.BLACK)
                    + ", WHITE: " + board.countPieces(OthelloPlayer.WHITE));
                System.out.println("Legal moves for " + currentPlayer + ": " + board.legalMovesSummary(currentPlayer));
                System.out.println(currentPlayer + " to move:");

                String input = scanner.nextLine().trim();
                if (input.equalsIgnoreCase("quit")) {
                    System.out.println("Thanks for playing!");
                    return;
                }

                try {
                    OthelloPosition move = OthelloPosition.fromString(input);
                    int flipped = board.playMove(move, currentPlayer);
                    System.out.println(currentPlayer + " played " + move + " and flipped " + flipped + " piece"
                        + (flipped == 1 ? "." : "s.") + "\n");
                    currentPlayer = currentPlayer.opponent();
                } catch (IllegalArgumentException error) {
                    System.out.println(error.getMessage());
                    System.out.println("Use a legal square like d3.\n");
                }
            }

            board.printBoard();
            int blackCount = board.countPieces(OthelloPlayer.BLACK);
            int whiteCount = board.countPieces(OthelloPlayer.WHITE);
            System.out.println();
            System.out.println("Final score - BLACK: " + blackCount + ", WHITE: " + whiteCount);

            if (blackCount > whiteCount) {
                System.out.println("BLACK wins!");
            } else if (whiteCount > blackCount) {
                System.out.println("WHITE wins!");
            } else {
                System.out.println("The game is a draw!");
            }
        }
    }
}