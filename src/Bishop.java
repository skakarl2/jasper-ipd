package chess;

public class Bishop extends Piece {
    public Bishop(Player player) {
        super(player);
    }

    @Override
    public boolean isValidMove(Position from, Position to, Board board) {
        // Bishop moves diagonally
        int rowDiff = Math.abs(to.getRow() - from.getRow());
        int colDiff = Math.abs(to.getCol() - from.getCol());

        // Must move diagonally (equal distance in both directions)
        if (rowDiff != colDiff || rowDiff == 0) {
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
