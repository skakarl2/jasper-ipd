package tictac;

public enum Mark {
    EMPTY(' '),
    X('X'),
    O('O');

    private final char symbol;

    Mark(char symbol) {
        this.symbol = symbol;
    }

    public char getSymbol() {
        return symbol;
    }

    public Mark opposite() {
        if (this == X) {
            return O;
        }
        if (this == O) {
            return X;
        }
        return EMPTY;
    }
}
