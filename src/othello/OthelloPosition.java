package othello;

public class OthelloPosition {
    private static final int BOARD_SIZE = 8;

    private final int row;
    private final int col;

    public OthelloPosition(int row, int col) {
        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
            throw new IllegalArgumentException("Position out of bounds: (" + row + ", " + col + ")");
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

    public static OthelloPosition fromString(String value) {
        if (value == null || value.length() != 2) {
            throw new IllegalArgumentException("Invalid move format: " + value);
        }

        char file = Character.toLowerCase(value.charAt(0));
        char rank = value.charAt(1);
        if (file < 'a' || file > 'h' || rank < '1' || rank > '8') {
            throw new IllegalArgumentException("Move must be between a1 and h8: " + value);
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
    public boolean equals(Object obj) {
        if (!(obj instanceof OthelloPosition)) {
            return false;
        }

        OthelloPosition other = (OthelloPosition) obj;
        return row == other.row && col == other.col;
    }

    @Override
    public int hashCode() {
        return row * BOARD_SIZE + col;
    }
}