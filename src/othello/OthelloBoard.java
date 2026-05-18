package othello;

import java.util.ArrayList;
import java.util.List;

public class OthelloBoard {
    private static final int BOARD_SIZE = 8;
    private static final int[][] DIRECTIONS = {
        { -1, -1 }, { -1, 0 }, { -1, 1 },
        { 0, -1 },            { 0, 1 },
        { 1, -1 },  { 1, 0 }, { 1, 1 }
    };

    private final OthelloPlayer[][] board;

    public OthelloBoard() {
        this.board = new OthelloPlayer[BOARD_SIZE][BOARD_SIZE];
    }

    public void initialize() {
        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                board[row][col] = null;
            }
        }

        board[3][3] = OthelloPlayer.BLACK;
        board[3][4] = OthelloPlayer.WHITE;
        board[4][3] = OthelloPlayer.WHITE;
        board[4][4] = OthelloPlayer.BLACK;
    }

    public void printBoard() {
        System.out.println("  a b c d e f g h");
        for (int row = 0; row < BOARD_SIZE; row++) {
            System.out.print(8 - row + " ");
            for (int col = 0; col < BOARD_SIZE; col++) {
                OthelloPlayer cell = board[row][col];
                System.out.print((cell == null ? '.' : cell.getSymbol()) + " ");
            }
            System.out.println(8 - row);
        }
        System.out.println("  a b c d e f g h");
    }

    public boolean hasAnyLegalMove(OthelloPlayer player) {
        return !getLegalMoves(player).isEmpty();
    }

    public List<OthelloPosition> getLegalMoves(OthelloPlayer player) {
        List<OthelloPosition> legalMoves = new ArrayList<>();
        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                OthelloPosition move = new OthelloPosition(row, col);
                if (isLegalMove(move, player)) {
                    legalMoves.add(move);
                }
            }
        }
        return legalMoves;
    }

    public boolean isLegalMove(OthelloPosition move, OthelloPlayer player) {
        if (board[move.getRow()][move.getCol()] != null) {
            return false;
        }

        for (int[] direction : DIRECTIONS) {
            if (countFlips(move, player, direction[0], direction[1]) > 0) {
                return true;
            }
        }
        return false;
    }

    public int playMove(OthelloPosition move, OthelloPlayer player) {
        if (!isLegalMove(move, player)) {
            throw new IllegalArgumentException("Illegal move: " + move);
        }

        int flipped = 0;
        board[move.getRow()][move.getCol()] = player;
        for (int[] direction : DIRECTIONS) {
            int rowStep = direction[0];
            int colStep = direction[1];
            int captured = countFlips(move, player, rowStep, colStep);
            flipped += captured;

            for (int offset = 1; offset <= captured; offset++) {
                int row = move.getRow() + rowStep * offset;
                int col = move.getCol() + colStep * offset;
                board[row][col] = player;
            }
        }
        return flipped;
    }

    public int countPieces(OthelloPlayer player) {
        int count = 0;
        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                if (board[row][col] == player) {
                    count++;
                }
            }
        }
        return count;
    }

    public boolean isBoardFull() {
        for (int row = 0; row < BOARD_SIZE; row++) {
            for (int col = 0; col < BOARD_SIZE; col++) {
                if (board[row][col] == null) {
                    return false;
                }
            }
        }
        return true;
    }

    public String legalMovesSummary(OthelloPlayer player) {
        List<OthelloPosition> legalMoves = getLegalMoves(player);
        if (legalMoves.isEmpty()) {
            return "none";
        }

        StringBuilder builder = new StringBuilder();
        for (int index = 0; index < legalMoves.size(); index++) {
            if (index > 0) {
                builder.append(' ');
            }
            builder.append(legalMoves.get(index));
        }
        return builder.toString();
    }

    private int countFlips(OthelloPosition move, OthelloPlayer player, int rowStep, int colStep) {
        int row = move.getRow() + rowStep;
        int col = move.getCol() + colStep;
        int captured = 0;

        while (isInside(row, col) && board[row][col] == player.opponent()) {
            captured++;
            row += rowStep;
            col += colStep;
        }

        if (captured == 0 || !isInside(row, col) || board[row][col] != player) {
            return 0;
        }
        return captured;
    }

    private boolean isInside(int row, int col) {
        return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
    }
}