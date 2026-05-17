package othello;

public class OthelloMoveResult {
    private final boolean success;
    private final boolean gameOver;
    private final String message;

    private OthelloMoveResult(boolean success, boolean gameOver, String message) {
        this.success = success;
        this.gameOver = gameOver;
        this.message = message;
    }

    public static OthelloMoveResult success(boolean gameOver, String message) {
        return new OthelloMoveResult(true, gameOver, message);
    }

    public static OthelloMoveResult failure(String message) {
        return new OthelloMoveResult(false, false, message);
    }

    public boolean isSuccess() {
        return success;
    }

    public boolean isGameOver() {
        return gameOver;
    }

    public String getMessage() {
        return message;
    }
}