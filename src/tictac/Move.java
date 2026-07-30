package tictac;

public class Move {
    private final int row;
    private final int col;

    public Move(int row, int col) {
        this.row = row;
        this.col = col;
    }

    public int getRow() {
        return row;
    }

    public int getCol() {
        return col;
    }

    public boolean isQuitCommand() {
        return row < 0 || col < 0;
    }

    @Override
    public String toString() {
        return "(" + (row + 1) + ", " + (col + 1) + ")";
    }
}
