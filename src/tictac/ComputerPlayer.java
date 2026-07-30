package tictac;

import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class ComputerPlayer implements Player {
    private final String name;
    private final Mark mark;
    private final Difficulty difficulty;
    private final Random random;

    public ComputerPlayer(String name, Mark mark, Difficulty difficulty) {
        this.name = name;
        this.mark = mark;
        this.difficulty = difficulty;
        this.random = new Random();
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public Mark getMark() {
        return mark;
    }

    @Override
    public boolean isComputer() {
        return true;
    }

    @Override
    public Move chooseMove(TicTacToeBoard board, Scanner scanner) {
        List<Move> availableMoves = board.getAvailableMoves();
        if (availableMoves.isEmpty()) {
            return new Move(-1, -1);
        }

        if (difficulty == Difficulty.EASY) {
            return randomMove(availableMoves);
        }

        if (difficulty == Difficulty.MEDIUM) {
            // Medium level intentionally makes occasional mistakes.
            if (random.nextInt(100) < 40) {
                return randomMove(availableMoves);
            }
            return bestMove(board);
        }

        return bestMove(board);
    }

    private Move randomMove(List<Move> availableMoves) {
        return availableMoves.get(random.nextInt(availableMoves.size()));
    }

    private Move bestMove(TicTacToeBoard board) {
        int bestScore = Integer.MIN_VALUE;
        Move best = null;

        for (Move move : board.getAvailableMoves()) {
            board.placeMark(move, mark);
            int score = minimax(board, mark.opposite(), false, 0, Integer.MIN_VALUE, Integer.MAX_VALUE);
            board.clearCell(move.getRow(), move.getCol());

            if (score > bestScore) {
                bestScore = score;
                best = move;
            }
        }

        return best;
    }

    private int minimax(TicTacToeBoard board, Mark currentTurn, boolean maximizing, int depth, int alpha, int beta) {
        GameResult result = board.evaluate();
        if (result != GameResult.IN_PROGRESS) {
            return evaluateTerminal(result, depth);
        }

        if (maximizing) {
            int maxScore = Integer.MIN_VALUE;
            for (Move move : board.getAvailableMoves()) {
                board.placeMark(move, currentTurn);
                int score = minimax(board, currentTurn.opposite(), false, depth + 1, alpha, beta);
                board.clearCell(move.getRow(), move.getCol());
                maxScore = Math.max(maxScore, score);
                alpha = Math.max(alpha, score);
                if (beta <= alpha) {
                    break;
                }
            }
            return maxScore;
        }

        int minScore = Integer.MAX_VALUE;
        for (Move move : board.getAvailableMoves()) {
            board.placeMark(move, currentTurn);
            int score = minimax(board, currentTurn.opposite(), true, depth + 1, alpha, beta);
            board.clearCell(move.getRow(), move.getCol());
            minScore = Math.min(minScore, score);
            beta = Math.min(beta, score);
            if (beta <= alpha) {
                break;
            }
        }
        return minScore;
    }

    private int evaluateTerminal(GameResult result, int depth) {
        if ((result == GameResult.X_WINS && mark == Mark.X) || (result == GameResult.O_WINS && mark == Mark.O)) {
            return 10 - depth;
        }
        if ((result == GameResult.X_WINS && mark == Mark.O) || (result == GameResult.O_WINS && mark == Mark.X)) {
            return depth - 10;
        }
        return 0;
    }
}
