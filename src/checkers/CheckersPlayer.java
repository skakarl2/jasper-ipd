package checkers;

public enum CheckersPlayer {
    RED(-1),
    BLACK(1);

    private final int forwardStep;

    CheckersPlayer(int forwardStep) {
        this.forwardStep = forwardStep;
    }

    public int getForwardStep() {
        return forwardStep;
    }

    public CheckersPlayer opponent() {
        return this == RED ? BLACK : RED;
    }
}