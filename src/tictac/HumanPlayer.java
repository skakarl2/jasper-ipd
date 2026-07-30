package tictac;

import java.util.Scanner;

public class HumanPlayer implements Player {
    private final String name;
    private final Mark mark;

    public HumanPlayer(String name, Mark mark) {
        this.name = name;
        this.mark = mark;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public Mark getMark() {
        return mark;
    }

    @Override
    public boolean isComputer() {
        return false;
    }

    @Override
    public Move chooseMove(TicTacToeBoard board, Scanner scanner) {
        while (true) {
            System.out.print(name + " (" + mark + "), enter move (A1, B3, or row col). Type quit to stop: ");
            String input = scanner.nextLine().trim();

            if (input.equalsIgnoreCase("quit") || input.equalsIgnoreCase("exit")) {
                return new Move(-1, -1);
            }

            Move parsed = parseMove(input);
            if (parsed == null) {
                System.out.println("Invalid format. Try A1 or 2 3.");
                continue;
            }

            if (!board.isInBounds(parsed.getRow(), parsed.getCol())) {
                System.out.println("Move out of bounds. Use rows A-C and cols 1-3.");
                continue;
            }

            if (!board.isCellEmpty(parsed.getRow(), parsed.getCol())) {
                System.out.println("That square is already occupied. Choose another.");
                continue;
            }

            return parsed;
        }
    }

    private Move parseMove(String input) {
        if (input.isEmpty()) {
            return null;
        }

        String compact = input.replace(",", " ").trim();
        String[] parts = compact.split("\\s+");
        if (parts.length == 2) {
            Integer row = parseIndex(parts[0]);
            Integer col = parseIndex(parts[1]);
            if (row != null && col != null) {
                return new Move(row, col);
            }
        }

        if (input.length() >= 2) {
            char first = Character.toUpperCase(input.charAt(0));
            char second = input.charAt(1);

            if (first >= 'A' && first <= 'C' && Character.isDigit(second)) {
                int row = first - 'A';
                int col = Character.getNumericValue(second) - 1;
                return new Move(row, col);
            }
            if (Character.isDigit(first) && Character.isLetter(second)) {
                int row = Character.getNumericValue(first) - 1;
                int col = Character.toUpperCase(second) - 'A';
                return new Move(row, col);
            }
        }

        return null;
    }

    private Integer parseIndex(String token) {
        if (token.length() == 1 && Character.isLetter(token.charAt(0))) {
            char c = Character.toUpperCase(token.charAt(0));
            if (c >= 'A' && c <= 'C') {
                return c - 'A';
            }
            return null;
        }
        try {
            int oneBased = Integer.parseInt(token);
            return oneBased - 1;
        } catch (NumberFormatException ex) {
            return null;
        }
    }
}
