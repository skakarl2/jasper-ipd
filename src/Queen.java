package chess;

public class Queen extends Piece {
    public Queen(Player player) {
        super(player);
    }

    @Override
    public boolean isValidMove(Position from, Position to, Board board) {
        // Queen moves like Rook or Bishop (horizontal, vertical, or diagonal)
        int rowDiff = Math.abs(to.getRow() - from.getRow());
        int colDiff = Math.abs(to.getCol() - from.getCol());

        // Must move in a straight line (horizontal/vertical) or diagonal
        if (rowDiff != colDiff && from.getRow() != to.getRow() && from.getCol() != to.getCol()) {
            return false;
        }

        // Can't move to the same square
        if (from.getRow() == to.getRow() && from.getCol() == to.getCol()) {
            return false;
        }

        // Check if target square is occupied by own piece
        Piece target = board.getPiece(to);
        if (target != null && target.getPlayer() == getPlayer()) {
            return false;
        }

        // Check if path is clear
        return isPathClear(from, to, board);
    }

    private boolean isPathClear(Position from, Position to, Board board) {
        int rowStep = Integer.compare(to.getRow(), from.getRow());
        int colStep = Integer.compare(to.getCol(), from.getCol());

        int row = from.getRow() + rowStep;
        int col = from.getCol() + colStep;

        while (row != to.getRow() || col != to.getCol()) {
            if (board.getPiece(new Position(row, col)) != null) {
                return false;
            }
            row += rowStep;
            col += colStep;
        }

        return true;
    }
}
