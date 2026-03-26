package chess;

public class Pawn extends Piece {
    public Pawn(Player player) {
        super(player);
    }

    @Override
    public boolean isValidMove(Position from, Position to, Board board) {
        int direction = getPlayer() == Player.WHITE ? -1 : 1;
        int startRow = getPlayer() == Player.WHITE ? 6 : 1;

        if (from.getCol() == to.getCol()) {
            // Move forward
            if (to.getRow() == from.getRow() + direction && board.getPiece(to) == null) {
                return true;
            }
            // Move two squares from starting position
            if (from.getRow() == startRow && to.getRow() == from.getRow() + 2 * direction && board.getPiece(to) == null) {
                return true;
            }
        } else if (Math.abs(from.getCol() - to.getCol()) == 1 && to.getRow() == from.getRow() + direction) {
            // Capture diagonally
            Piece target = board.getPiece(to);
            if (target != null && target.getPlayer() != getPlayer()) {
                return true;
            }
        }

        return false;
    }
}