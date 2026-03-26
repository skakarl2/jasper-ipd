package chess;

public abstract class Piece {
    private Player player;

    public Piece(Player player) {
        this.player = player;
    }

    public Player getPlayer() {
        return player;
    }

    public abstract boolean isValidMove(Position from, Position to, Board board);

    @Override
    public String toString() {
        return this.getClass().getSimpleName().charAt(0) + (player == Player.WHITE ? "W" : "B");
    }
}