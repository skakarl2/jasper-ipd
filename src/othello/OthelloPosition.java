package othello;

public class OthelloPosition {
    private final int row;
    private final int col;

    public OthelloPosition(int row, int col) {
        if (row < 0 || row > 7 || col < 0 || col > 7) {
            throw new IllegalArgumentException("Position must stay within the 8x8 board.");
        }
        this.row = row;
        this.col = col;
    }

    public int getRow() {
        return row;
    }

    public int getCol() {
        return col;
    }

    public static OthelloPosition fromString(String notation) {
        if (notation == null || notation.length() != 2) {
            throw new IllegalArgumentException("Use coordinates like d3 or f6.");
        }

        char file = Character.toLowerCase(notation.charAt(0));
        char rank = notation.charAt(1);
        if (file < 'a' || file > 'h' || rank < '1' || rank > '8') {
            throw new IllegalArgumentException("Coordinates must be between a1 and h8.");
        }

        int col = file - 'a';
        int row = 8 - Character.getNumericValue(rank);
        return new OthelloPosition(row, col);
    }

    @Override
    public String toString() {
        return String.valueOf((char) ('a' + col)) + (8 - row);
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (!(other instanceof OthelloPosition)) {
            return false;
        }
        OthelloPosition that = (OthelloPosition) other;
        return row == that.row && col == that.col;
    }

    @Override
    public int hashCode() {
        return 31 * row + col;
    }
}