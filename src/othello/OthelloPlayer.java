package othello;

public enum OthelloPlayer {
    BLACK("B"),
    WHITE("W");

    private final String symbol;

    OthelloPlayer(String symbol) {
        this.symbol = symbol;
    }

    public OthelloPlayer opponent() {
        return this == BLACK ? WHITE : BLACK;
    }

    public String getSymbol() {
        return symbol;
    }

    @Override
    public String toString() {
        return this == BLACK ? "Black" : "White";
    }
}