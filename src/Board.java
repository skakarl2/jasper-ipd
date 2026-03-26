package chess;

public class Board {
    private Piece[][] board;

    public Board() {
        board = new Piece[8][8];
    }

    public void initialize() {
        // Initialize pieces for both players
        for (int i = 0; i < 8; i++) {
            board[1][i] = new Pawn(Player.BLACK);
            board[6][i] = new Pawn(Player.WHITE);
        }

        board[0][0] = new Rook(Player.BLACK);
        board[0][7] = new Rook(Player.BLACK);
        board[7][0] = new Rook(Player.WHITE);
        board[7][7] = new Rook(Player.WHITE);

        board[0][1] = new Knight(Player.BLACK);
        board[0][6] = new Knight(Player.BLACK);
        board[7][1] = new Knight(Player.WHITE);
        board[7][6] = new Knight(Player.WHITE);

        board[0][2] = new Bishop(Player.BLACK);
        board[0][5] = new Bishop(Player.BLACK);
        board[7][2] = new Bishop(Player.WHITE);
        board[7][5] = new Bishop(Player.WHITE);

        board[0][3] = new Queen(Player.BLACK);
        board[0][4] = new King(Player.BLACK);
        board[7][3] = new Queen(Player.WHITE);
        board[7][4] = new King(Player.WHITE);
    }

    public void printBoard() {
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                if (board[row][col] == null) {
                    System.out.print(".");
                } else {
                    System.out.print(board[row][col]);
                }
                System.out.print(" ");
            }
            System.out.println();
        }
    }

    public boolean movePiece(Position from, Position to, Player player) {
        Piece piece = board[from.getRow()][from.getCol()];
        if (piece == null || piece.getPlayer() != player) {
            return false;
        }

        if (piece.isValidMove(from, to, this)) {
            board[to.getRow()][to.getCol()] = piece;
            board[from.getRow()][from.getCol()] = null;
            return true;
        }

        return false;
    }

    public boolean isCheckmate(Player player) {
        // Simplified checkmate logic for demonstration
        return false;
    }

    public Piece getPiece(Position position) {
        return board[position.getRow()][position.getCol()];
    }
}