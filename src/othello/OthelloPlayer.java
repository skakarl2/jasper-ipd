package othello;

public enum OthelloPlayer {
    BLACK('B'),
    WHITE('W');

    private final char symbol;

    OthelloPlayer(char symbol) {
        this.symbol = symbol;
    }

    public char getSymbol() {
        return symbol;
    }

    public OthelloPlayer opponent() {
        return this == BLACK ? WHITE : BLACK;
    }
}