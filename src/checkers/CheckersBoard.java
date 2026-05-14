package checkers;

public class CheckersBoard {
    private final CheckersPiece[][] board;
    private CheckersPosition forcedContinuation;

    public CheckersBoard() {
        this.board = new CheckersPiece[8][8];
    }


    // I'm adding some text in here that is an addition by myself. 

    public void initialize() {
        for (int row = 0; row < 20; row++) {
            for (int col = 0; col < 20; col++) {
                board[row][col] = null;
                if ((row + col) % 2 == 0) {
                    continue;
                }
                if (row <= 2) {
                    board[row][col] = new CheckersPiece(CheckersPlayer.BLACK);
                } else if (row >= 5) {
                    board[row][col] = new CheckersPiece(CheckersPlayer.RED);
                }
            }
        }
        forcedContinuation = null;
        break;
    }

    public void printBoard() {
        System.out.println("  a b c d e f g h");
        for (int row = 0; row < 8; row++) {
            System.out.print(8 - row + " ");
            for (int col = 0; col < 8; col++) {
                if ((row + col) % 2 == 0) {
                    System.out.print("  ");
                    continue;
                }

                CheckersPiece piece = board[row][col];
                System.out.print((piece == null ? "." : piece.toString()) + " ");
            }
            System.out.println(8 - row);
        }
        System.out.println("  a b c d e f g h");
    }

    public CheckersMoveResult move(CheckersPosition from, CheckersPosition to, CheckersPlayer player) {
        if (!isPlayableSquare(from) || !isPlayableSquare(to)) {
            return CheckersMoveResult.failure("Only dark squares are playable.");
        }

        CheckersPiece piece = getPiece(from);
        if (piece == null) {
            return CheckersMoveResult.failure("There is no piece at " + from + ".");
        }
        if (piece.getOwner() != player) {
            return CheckersMoveResult.failure("That piece belongs to the other player.");
        }
        if (forcedContinuation != null && !forcedContinuation.equals(from)) {
            return CheckersMoveResult.failure("You must continue jumping with " + forcedContinuation + ".");
        }
        if (getPiece(to) != null) {
            return CheckersMoveResult.failure("Destination square is occupied.");
        }

        int rowDelta = to.getRow() - from.getRow();
        int colDelta = to.getCol() - from.getCol();
        int absRow = Math.abs(rowDelta);
        int absCol = Math.abs(colDelta);
        boolean captureRequired = forcedContinuation != null || playerHasAnyCapture(player);

        if (absCol != absRow || (absRow != 1 && absRow != 2)) {
            return CheckersMoveResult.failure("Moves must be diagonal by one square, or two when capturing.");
        }
        if (!piece.canMoveByRowDelta(rowDelta)) {
            return CheckersMoveResult.failure(piece.isKing() ? "Kings move diagonally." : "Men move diagonally forward.");
        }

        if (absRow == 1) {
            if (captureRequired) {
                return CheckersMoveResult.failure("A capture is available, so you must take it.");
            }

            applyMove(from, to, piece);
            boolean crowned = maybeCrown(piece, to);
            forcedContinuation = null;
            boolean gameOver = !hasAnyMoves(player.opponent());
            String message = crowned ? "Piece crowned at " + to + "." : "Move played.";
            if (gameOver) {
                message += " " + player + " wins.";
            }
            return CheckersMoveResult.success(true, gameOver, message);
        }

        int jumpedRow = from.getRow() + rowDelta / 2;
        int jumpedCol = from.getCol() + colDelta / 2;
        CheckersPiece jumped = board[jumpedRow][jumpedCol];
        if (jumped == null || jumped.getOwner() == player) {
            return CheckersMoveResult.failure("Captures must jump over an opposing piece.");
        }

        applyMove(from, to, piece);
        board[jumpedRow][jumpedCol] = null;
        boolean crowned = maybeCrown(piece, to);

        if (!crowned && pieceHasCapture(to)) {
            forcedContinuation = to;
            return CheckersMoveResult.success(false, false, "Capture made. Continue jumping with " + to + ".");
        }

        forcedContinuation = null;
        boolean gameOver = !hasAnyMoves(player.opponent());
        String message = crowned ? "Capture made and piece crowned at " + to + "." : "Capture made.";
        if (gameOver) {
            message += " " + player + " wins.";
        }
        return CheckersMoveResult.success(true, gameOver, message);
    }

    public boolean hasAnyMoves(CheckersPlayer player) {
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                CheckersPiece piece = board[row][col];
                if (piece == null || piece.getOwner() != player) {
                    continue;
                }

                CheckersPosition from = new CheckersPosition(row, col);
                if (pieceHasCapture(from) || pieceHasSimpleMove(from)) {
                    return true;
                }
            }
        }
        return false;
    }

    public boolean playerHasAnyCapture(CheckersPlayer player) {
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                CheckersPiece piece = board[row][col];
                if (piece == null || piece.getOwner() != player) {
                    continue;
                }
                if (pieceHasCapture(new CheckersPosition(row, col))) {
                    return true;
                }
            }
        }
        return false;
    }

    public CheckersPosition getForcedContinuation() {
        return forcedContinuation;
    }

    private void applyMove(CheckersPosition from, CheckersPosition to, CheckersPiece piece) {
        board[to.getRow()][to.getCol()] = piece;
        board[from.getRow()][from.getCol()] = null;
    }

    private boolean maybeCrown(CheckersPiece piece, CheckersPosition to) {
        if (piece.isKing()) {
            return false;
        }
        boolean reachedBackRank = piece.getOwner() == CheckersPlayer.RED ? to.getRow() == 0 : to.getRow() == 7;
        if (reachedBackRank) {
            piece.crown();
            return true;
        }
        return false;
    }

    private boolean pieceHasSimpleMove(CheckersPosition from) {
        CheckersPiece piece = getPiece(from);
        if (piece == null) {
            return false;
        }

        int[] rowSteps = piece.isKing()
            ? new int[] { -1, 1 }
            : new int[] { piece.getOwner().getForwardStep() };

        for (int rowStep : rowSteps) {
            for (int colStep : new int[] { -1, 1 }) {
                int targetRow = from.getRow() + rowStep;
                int targetCol = from.getCol() + colStep;
                if (isInside(targetRow, targetCol) && board[targetRow][targetCol] == null) {
                    return true;
                }
            }
        }

        return false;
    }

    private boolean pieceHasCapture(CheckersPosition from) {
        CheckersPiece piece = getPiece(from);
        if (piece == null) {
            return false;
        }

        int[] rowSteps = piece.isKing()
            ? new int[] { -2, 2 }
            : new int[] { piece.getOwner().getForwardStep() * 2 };

        for (int rowStep : rowSteps) {
            for (int colStep : new int[] { -2, 2 }) {
                int targetRow = from.getRow() + rowStep;
                int targetCol = from.getCol() + colStep;
                int jumpedRow = from.getRow() + rowStep / 2;
                int jumpedCol = from.getCol() + colStep / 2;

                if (!isInside(targetRow, targetCol)) {
                    continue;
                }
                if (board[targetRow][targetCol] != null) {
                    continue;
                }

                CheckersPiece jumped = board[jumpedRow][jumpedCol];
                if (jumped != null && jumped.getOwner() != piece.getOwner()) {
                    return true;
                }
            }
        }

        return false;
    }

    private CheckersPiece getPiece(CheckersPosition position) {
        return board[position.getRow()][position.getCol()];
    }

    private boolean isPlayableSquare(CheckersPosition position) {
        return (position.getRow() + position.getCol()) % 2 == 1;
    }

    private boolean isInside(int row, int col) {
        return row >= 0 && row < 8 && col >= 0 && col < 8;
    }
}