package othello;

import java.util.ArrayList;
import java.util.List;

public class OthelloBoard {
    private static final int SIZE = 8;
    private static final int[][] DIRECTIONS = {
        { -1, -1 }, { -1, 0 }, { -1, 1 },
        { 0, -1 },            { 0, 1 },
        { 1, -1 },  { 1, 0 }, { 1, 1 }
    };

    private final OthelloPlayer[][] board;

    public OthelloBoard() {
        this.board = new OthelloPlayer[SIZE][SIZE];
    }

    public void initialize() {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
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
        for (int row = 0; row < SIZE; row++) {
            System.out.print(8 - row + " ");
            for (int col = 0; col < SIZE; col++) {
                OthelloPlayer piece = board[row][col];
                System.out.print((piece == null ? "." : piece.getSymbol()) + " ");
            }
            System.out.println(8 - row);
        }
        System.out.println("  a b c d e f g h");
        System.out.println("Score - Black: " + countPieces(OthelloPlayer.BLACK) + ", White: " + countPieces(OthelloPlayer.WHITE));
    }

    public OthelloMoveResult playMove(OthelloPosition position, OthelloPlayer player) {
        if (!isInside(position.getRow(), position.getCol())) {
            return OthelloMoveResult.failure("Move is outside the board.");
        }
        if (board[position.getRow()][position.getCol()] != null) {
            return OthelloMoveResult.failure("That square is already occupied.");
        }

        List<OthelloPosition> flipped = collectFlips(position, player);
        if (flipped.isEmpty()) {
            return OthelloMoveResult.failure("That move does not capture any opposing discs.");
        }

        board[position.getRow()][position.getCol()] = player;
        for (OthelloPosition flip : flipped) {
            board[flip.getRow()][flip.getCol()] = player;
        }

        OthelloPlayer opponent = player.opponent();
        boolean opponentHasMove = hasAnyValidMove(opponent);
        boolean playerHasMove = hasAnyValidMove(player);
        boolean gameOver = !opponentHasMove && !playerHasMove;

        String message = player + " played " + position + " and flipped " + flipped.size() + " disc" + (flipped.size() == 1 ? "" : "s") + ".";
        if (gameOver) {
            message += " " + winnerMessage();
        } else if (!opponentHasMove) {
            message += " " + opponent + " has no legal move and must pass.";
        }

        return OthelloMoveResult.success(gameOver, message);
    }

    public boolean hasAnyValidMove(OthelloPlayer player) {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (board[row][col] == null && !collectFlips(new OthelloPosition(row, col), player).isEmpty()) {
                    return true;
                }
            }
        }
        return false;
    }

    public List<OthelloPosition> validMovesFor(OthelloPlayer player) {
        List<OthelloPosition> moves = new ArrayList<>();
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                OthelloPosition position = new OthelloPosition(row, col);
                if (board[row][col] == null && !collectFlips(position, player).isEmpty()) {
                    moves.add(position);
                }
            }
        }
        return moves;
    }

    public boolean isBoardFull() {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (board[row][col] == null) {
                    return false;
                }
            }
        }
        return true;
    }

    public String winnerMessage() {
        int blackCount = countPieces(OthelloPlayer.BLACK);
        int whiteCount = countPieces(OthelloPlayer.WHITE);
        if (blackCount == whiteCount) {
            return "The game is a draw at " + blackCount + "-" + whiteCount + ".";
        }
        OthelloPlayer winner = blackCount > whiteCount ? OthelloPlayer.BLACK : OthelloPlayer.WHITE;
        int winnerCount = Math.max(blackCount, whiteCount);
        int loserCount = Math.min(blackCount, whiteCount);
        return winner + " wins " + winnerCount + "-" + loserCount + ".";
    }

    private int countPieces(OthelloPlayer player) {
        int count = 0;
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (board[row][col] == player) {
                    count++;
                }
            }
        }
        return count;
    }

    private List<OthelloPosition> collectFlips(OthelloPosition start, OthelloPlayer player) {
        List<OthelloPosition> allFlips = new ArrayList<>();
        for (int[] direction : DIRECTIONS) {
            allFlips.addAll(collectDirectionalFlips(start, player, direction[0], direction[1]));
        }
        return allFlips;
    }

    private List<OthelloPosition> collectDirectionalFlips(OthelloPosition start, OthelloPlayer player, int rowStep, int colStep) {
        List<OthelloPosition> flips = new ArrayList<>();
        int row = start.getRow() + rowStep;
        int col = start.getCol() + colStep;

        while (isInside(row, col) && board[row][col] == player.opponent()) {
            flips.add(new OthelloPosition(row, col));
            row += rowStep;
            col += colStep;
        }

        if (flips.isEmpty() || !isInside(row, col) || board[row][col] != player) {
            return List.of();
        }

        return flips;
    }

    private boolean isInside(int row, int col) {
        return row >= 0 && row < SIZE && col >= 0 && col < SIZE;
    }
}