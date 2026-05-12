package checkers;

public class CheckersMoveResult {
    private final boolean success;
    private final boolean turnComplete;
    private final boolean gameOver;
    private final String message;

    private CheckersMoveResult(boolean success, boolean turnComplete, boolean gameOver, String message) {
        this.success = success;
        this.turnComplete = turnComplete;
        this.gameOver = gameOver;
        this.message = message;
    }

    public static CheckersMoveResult success(boolean turnComplete, boolean gameOver, String message) {
        return new CheckersMoveResult(true, turnComplete, gameOver, message);
    }

    public static CheckersMoveResult failure(String message) {
        return new CheckersMoveResult(false, false, false, message);
    }

    public boolean isSuccess() {
        return success;
    }

    public boolean isTurnComplete() {
        return turnComplete;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public String getMessage() {
        return message;
    }
}