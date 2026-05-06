package chess;

public class King extends Piece {
    public King(Player player) {
        super(player);
    }

    @Override
    public boolean isValidMove(Position from, Position to, Board board) {
        // King moves one square in any direction
        int rowDiff = Math.abs(to.getRow() - from.getRow());
        int colDiff = Math.abs(to.getCol() - from.getCol());

        // Must move exactly one square
        if (rowDiff > 1 || colDiff > 1 || (rowDiff == 0 && colDiff == 0)) {
            return false;
        }

        // Check if target square is occupied by own piece
        Piece target = board.getPiece(to);
        if (target != null && target.getPlayer() == getPlayer()) {
            return false;
        }

        return true;
    }
}
