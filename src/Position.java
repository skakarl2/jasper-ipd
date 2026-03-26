package chess;

public class Position {
    private int row;
    private int col;

    public Position(int row, int col) {
        this.row = row;
        this.col = col;
    }

    public int getRow() {
        return row;
    }

    public int getCol() {
        return col;
    }

    public static Position fromString(String pos) {
        int col = pos.charAt(0) - 'a';
        int row = 8 - (pos.charAt(1) - '1' + 1);
        return new Position(row, col);
    }
}