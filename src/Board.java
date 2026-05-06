package chess;

public class Board {
    private Piece[][] board;
    private Position whiteKingPos;
    private Position blackKingPos;

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
        blackKingPos = new Position(0, 4);
        
        board[7][3] = new Queen(Player.WHITE);
        board[7][4] = new King(Player.WHITE);
        whiteKingPos = new Position(7, 4);
    }

    public void printBoard() {
        System.out.println("  a b c d e f g h");
        for (int row = 0; row < 8; row++) {
            System.out.print((8 - row) + " ");
            for (int col = 0; col < 8; col++) {
                if (board[row][col] == null) {
                    System.out.print(".");
                } else {
                    System.out.print(board[row][col]);
                }
                System.out.print(" ");
            }
            System.out.println(8 - row);
        }
        System.out.println("  a b c d e f g h");
    }

    public boolean movePiece(Position from, Position to, Player player) {
        Piece piece = board[from.getRow()][from.getCol()];
        if (piece == null || piece.getPlayer() != player) {
            return false;
        }

        if (piece.isValidMove(from, to, this)) {
            // Perform the move
            Piece target = board[to.getRow()][to.getCol()];
            board[to.getRow()][to.getCol()] = piece;
            board[from.getRow()][from.getCol()] = null;

            // Update king position if moving a king
            if (piece instanceof King) {
                if (player == Player.WHITE) {
                    whiteKingPos = to;
                } else {
                    blackKingPos = to;
                }
            }

            // Check if the move leaves the player's own king in check
            Player opponent = player.opponent();
            if (isInCheck(player)) {
                // Undo the move
                board[from.getRow()][from.getCol()] = piece;
                board[to.getRow()][to.getCol()] = target;
                
                if (piece instanceof King) {
                    if (player == Player.WHITE) {
                        whiteKingPos = from;
                    } else {
                        blackKingPos = from;
                    }
                }
                
                System.out.println("Invalid move: Your king would be in check!");
                return false;
            }

            return true;
        }

        return false;
    }

    public boolean isInCheck(Player player) {
        Position kingPos = (player == Player.WHITE) ? whiteKingPos : blackKingPos;
        Player opponent = player.opponent();

        // Check if any opponent piece can attack the king
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                Piece piece = board[row][col];
                if (piece != null && piece.getPlayer() == opponent) {
                    if (piece.isValidMove(new Position(row, col), kingPos, this)) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    public boolean isCheckmate(Player player) {
        if (!isInCheck(player)) {
            return false;
        }

        // Check if the player has any legal moves
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                Piece piece = board[row][col];
                if (piece != null && piece.getPlayer() == player) {
                    // Try all possible moves for this piece
                    for (int toRow = 0; toRow < 8; toRow++) {
                        for (int toCol = 0; toCol < 8; toCol++) {
                            Position from = new Position(row, col);
                            Position to = new Position(toRow, toCol);

                            if (piece.isValidMove(from, to, this)) {
                                // Simulate the move
                                Piece target = board[toRow][toCol];
                                board[toRow][toCol] = piece;
                                board[row][col] = null;

                                if (piece instanceof King) {
                                    if (player == Player.WHITE) {
                                        whiteKingPos = to;
                                    } else {
                                        blackKingPos = to;
                                    }
                                }

                                boolean stillInCheck = isInCheck(player);

                                // Undo the move
                                board[row][col] = piece;
                                board[toRow][toCol] = target;

                                if (piece instanceof King) {
                                    if (player == Player.WHITE) {
                                        whiteKingPos = from;
                                    } else {
                                        blackKingPos = from;
                                    }
                                }

                                // If we found a legal move, it's not checkmate
                                if (!stillInCheck) {
                                    return false;
                                }
                            }
                        }
                    }
                }
            }
        }

        return true;
    }

    public boolean isStalemate(Player player) {
        if (isInCheck(player)) {
            return false;
        }

        // Check if the player has any legal moves
        for (int row = 0; row < 8; row++) {
            for (int col = 0; col < 8; col++) {
                Piece piece = board[row][col];
                if (piece != null && piece.getPlayer() == player) {
                    for (int toRow = 0; toRow < 8; toRow++) {
                        for (int toCol = 0; toCol < 8; toCol++) {
                            Position from = new Position(row, col);
                            Position to = new Position(toRow, toCol);

                            if (piece.isValidMove(from, to, this)) {
                                // Simulate the move
                                Piece target = board[toRow][toCol];
                                board[toRow][toCol] = piece;
                                board[row][col] = null;

                                if (piece instanceof King) {
                                    if (player == Player.WHITE) {
                                        whiteKingPos = to;
                                    } else {
                                        blackKingPos = to;
                                    }
                                }

                                boolean inCheck = isInCheck(player);

                                // Undo the move
                                board[row][col] = piece;
                                board[toRow][toCol] = target;

                                if (piece instanceof King) {
                                    if (player == Player.WHITE) {
                                        whiteKingPos = from;
                                    } else {
                                        blackKingPos = from;
                                    }
                                }

                                if (!inCheck) {
                                    return false;
                                }
                            }
                        }
                    }
                }
            }
        }

        return true;
    }

    public Piece getPiece(Position position) {
        return board[position.getRow()][position.getCol()];
    }
}