package chess;

public class Position {
    private int row;
    private int col;
    private static final int BOARD_SIZE = 8;

    public Position(int row, int col) {
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

    public static Position fromString(String pos) throws IllegalArgumentException {
        if (pos == null || pos.length() != 2) {
            throw new IllegalArgumentException("Invalid position format: " + pos);
        }
        
        char file = pos.charAt(0);
        char rank = pos.charAt(1);
        
        if (file < 'a' || file > 'h' || rank < '1' || rank > '8') {
            throw new IllegalArgumentException("Position out of valid range: " + pos);
        }
        
        int col = file - 'a';
        int row = 8 - (rank - '1' + 1);
        return new Position(row, col);
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Position)) {
            return false;
        }
        Position other = (Position) obj;
        return this.row == other.row && this.col == other.col;
    }

    @Override
    public int hashCode() {
        return row * 8 + col;
    }
}