package checkers;

public class CheckersPiece {
    private final CheckersPlayer owner;
    private boolean king;

    public CheckersPiece(CheckersPlayer owner) {
        this.owner = owner;
        this.king = false;
    }

    public CheckersPlayer getOwner() {
        return owner;
    }

    public boolean isKing() {
        return king;
    }

    public void crown() {
        king = true;
    }

    public boolean canMoveByRowDelta(int rowDelta) {
        if (king) {
            return Math.abs(rowDelta) == 1 || Math.abs(rowDelta) == 2;
        }
        return rowDelta == owner.getForwardStep() || rowDelta == owner.getForwardStep() * 2;
    }

    @Override
    public String toString() {
        if (owner == CheckersPlayer.RED) {
            return king ? "R" : "r";
        }
        return king ? "B" : "b";
    }
}