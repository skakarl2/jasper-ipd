package tictac;

import java.util.Scanner;

public class TicTacToeGame {
    private final Scanner scanner;
    private final TicTacToeBoard board;
    private final Player playerX;
    private final Player playerO;

    private int roundsPlayed;
    private int xWins;
    private int oWins;
    private int draws;

    public TicTacToeGame(Player playerX, Player playerO, Scanner scanner) {
        this.playerX = playerX;
        this.playerO = playerO;
        this.scanner = scanner;
        this.board = new TicTacToeBoard();
    }

    public void playSession() {
        System.out.println("\nStarting Tic-Tac-Toe session: " + playerX.getName() + " (X) vs " + playerO.getName() + " (O)");

        while (true) {
            boolean finished = playSingleRound();
            if (!finished) {
                System.out.println("Session ended by user.");
                break;
            }

            printScoreboard();

            System.out.print("Play another round? (y/n): ");
            String answer = scanner.nextLine().trim();
            if (!answer.equalsIgnoreCase("y") && !answer.equalsIgnoreCase("yes")) {
                break;
            }
        }

        System.out.println("\nFinal session summary:");
        printScoreboard();
    }

    private boolean playSingleRound() {
        board.reset();
        roundsPlayed++;
        Mark turn = (roundsPlayed % 2 == 1) ? Mark.X : Mark.O;

        while (board.evaluate() == GameResult.IN_PROGRESS) {
            Player currentPlayer = (turn == Mark.X) ? playerX : playerO;
            System.out.println("\nRound " + roundsPlayed + " - Turn: " + currentPlayer.getName() + " (" + turn + ")");
            System.out.println(board.render());

            if (currentPlayer.isComputer()) {
                System.out.println(currentPlayer.getName() + " is thinking...");
            }

            Move move = currentPlayer.chooseMove(board, scanner);
            if (move.isQuitCommand()) {
                return false;
            }

            if (!board.placeMark(move, turn)) {
                System.out.println("That move cannot be played. Try again.");
                continue;
            }

            turn = turn.opposite();
        }

        System.out.println("\nFinal board for round " + roundsPlayed + ":");
        System.out.println(board.render());

        GameResult result = board.evaluate();
        if (result == GameResult.X_WINS) {
            xWins++;
            System.out.println("Winner: " + playerX.getName() + " (X)");
        } else if (result == GameResult.O_WINS) {
            oWins++;
            System.out.println("Winner: " + playerO.getName() + " (O)");
        } else {
            draws++;
            System.out.println("Result: Draw");
        }

        return true;
    }

    private void printScoreboard() {
        System.out.println("Rounds played: " + roundsPlayed);
        System.out.println(playerX.getName() + " (X) wins: " + xWins);
        System.out.println(playerO.getName() + " (O) wins: " + oWins);
        System.out.println("Draws: " + draws);
    }
}
