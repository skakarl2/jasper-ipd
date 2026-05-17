package othello;

import java.util.List;
import java.util.Scanner;

public class OthelloGame {
    public static void main(String[] args) {
        OthelloBoard board = new OthelloBoard();
        board.initialize();

        try (Scanner scanner = new Scanner(System.in)) {
            OthelloPlayer currentPlayer = OthelloPlayer.BLACK;

            System.out.println("Welcome to Othello!");
            System.out.println("Enter a move like 'd3'. Type 'moves' to list legal moves, or 'quit' to exit.\n");

            while (true) {
                board.printBoard();
                System.out.println();

                if (board.isBoardFull() || (!board.hasAnyValidMove(OthelloPlayer.BLACK) && !board.hasAnyValidMove(OthelloPlayer.WHITE))) {
                    System.out.println(board.winnerMessage());
                    break;
                }

                if (!board.hasAnyValidMove(currentPlayer)) {
                    System.out.println(currentPlayer + " has no legal moves and must pass.\n");
                    currentPlayer = currentPlayer.opponent();
                    continue;
                }

                System.out.println(currentPlayer + " to move.");
                System.out.println("Enter your move:");

                String input = scanner.nextLine().trim();
                if (input.equalsIgnoreCase("quit")) {
                    System.out.println("Thanks for playing!");
                    break;
                }
                if (input.equalsIgnoreCase("moves")) {
                    List<OthelloPosition> moves = board.validMovesFor(currentPlayer);
                    System.out.println("Legal moves: " + formatMoves(moves) + "\n");
                    continue;
                }

                try {
                    OthelloPosition move = OthelloPosition.fromString(input);
                    OthelloMoveResult result = board.playMove(move, currentPlayer);
                    System.out.println(result.getMessage());
                    System.out.println();

                    if (!result.isSuccess()) {
                        continue;
                    }
                    if (result.isGameOver()) {
                        board.printBoard();
                        break;
                    }

                    currentPlayer = currentPlayer.opponent();
                } catch (IllegalArgumentException error) {
                    System.out.println(error.getMessage());
                    System.out.println();
                }
            }
        }
    }

    private static String formatMoves(List<OthelloPosition> moves) {
        if (moves.isEmpty()) {
            return "none";
        }

        StringBuilder builder = new StringBuilder();
        for (int index = 0; index < moves.size(); index++) {
            if (index > 0) {
                builder.append(", ");
            }
            builder.append(moves.get(index));
        }
        return builder.toString();
    }
}