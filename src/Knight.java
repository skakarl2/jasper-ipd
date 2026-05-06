package chess;

public class Knight extends Piece {
    public Knight(Player player) {
        super(player);
    }

    @Override
    public boolean isValidMove(Position from, Position to, Board board) {
        // Knight moves in L-shape: 2 squares in one direction, 1 in perpendicular
        int rowDiff = Math.abs(to.getRow() - from.getRow());
        int colDiff = Math.abs(to.getCol() - from.getCol());

        // Valid L-shapes: (2,1) or (1,2)
        if (!((rowDiff == 2 && colDiff == 1) || (rowDiff == 1 && colDiff == 2))) {
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
