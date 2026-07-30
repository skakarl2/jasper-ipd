package tictac;

import java.util.ArrayList;
import java.util.List;

public class TicTacToeBoard {
    public static final int SIZE = 3;
    private final Mark[][] cells;

    public TicTacToeBoard() {
        cells = new Mark[SIZE][SIZE];
        reset();
    }

    public void reset() {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                cells[row][col] = Mark.EMPTY;
            }
        }
    }

    public Mark getCell(int row, int col) {
        return cells[row][col];
    }

    public boolean isInBounds(int row, int col) {
        return row >= 0 && row < SIZE && col >= 0 && col < SIZE;
    }

    public boolean isCellEmpty(int row, int col) {
        return isInBounds(row, col) && cells[row][col] == Mark.EMPTY;
    }

    public boolean placeMark(Move move, Mark mark) {
        int row = move.getRow();
        int col = move.getCol();
        if (!isCellEmpty(row, col) || mark == Mark.EMPTY) {
            return false;
        }
        cells[row][col] = mark;
        return true;
    }

    public void clearCell(int row, int col) {
        if (isInBounds(row, col)) {
            cells[row][col] = Mark.EMPTY;
        }
    }

    public List<Move> getAvailableMoves() {
        List<Move> moves = new ArrayList<>();
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (cells[row][col] == Mark.EMPTY) {
                    moves.add(new Move(row, col));
                }
            }
        }
        return moves;
    }

    public boolean isFull() {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (cells[row][col] == Mark.EMPTY) {
                    return false;
                }
            }
        }
        return true;
    }

    public GameResult evaluate() {
        Mark winner = getWinner();
        if (winner == Mark.X) {
            return GameResult.X_WINS;
        }
        if (winner == Mark.O) {
            return GameResult.O_WINS;
        }
        if (isFull()) {
            return GameResult.DRAW;
        }
        return GameResult.IN_PROGRESS;
    }

    public Mark getWinner() {
        for (int i = 0; i < SIZE; i++) {
            if (cells[i][0] != Mark.EMPTY && cells[i][0] == cells[i][1] && cells[i][1] == cells[i][2]) {
                return cells[i][0];
            }
            if (cells[0][i] != Mark.EMPTY && cells[0][i] == cells[1][i] && cells[1][i] == cells[2][i]) {
                return cells[0][i];
            }
        }

        if (cells[0][0] != Mark.EMPTY && cells[0][0] == cells[1][1] && cells[1][1] == cells[2][2]) {
            return cells[0][0];
        }
        if (cells[0][2] != Mark.EMPTY && cells[0][2] == cells[1][1] && cells[1][1] == cells[2][0]) {
            return cells[0][2];
        }

        return Mark.EMPTY;
    }

    public String render() {
        StringBuilder sb = new StringBuilder();
        sb.append("    1   2   3\n");
        for (int row = 0; row < SIZE; row++) {
            char rowLabel = (char) ('A' + row);
            sb.append(" ").append(rowLabel).append(" ");
            for (int col = 0; col < SIZE; col++) {
                sb.append(" ").append(cells[row][col].getSymbol()).append(" ");
                if (col < SIZE - 1) {
                    sb.append("|");
                }
            }
            sb.append("\n");
            if (row < SIZE - 1) {
                sb.append("   ---+---+---\n");
            }
        }
        return sb.toString();
    }
}
