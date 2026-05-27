package src;

import java.util.*;

public class CanastaGame {
    private final Deck deck = new Deck();
    private final List<Card> discardPile = new ArrayList<>();
    private final CanastaPlayer[] players = { new CanastaPlayer("You"), new CanastaPlayer("Computer") };
    private int currentPlayer = 0;
    private static final int HAND_SIZE = 11;

    public void start() {
        // Deal hands
        for (int i = 0; i < HAND_SIZE; i++) {
            for (CanastaPlayer p : players) p.draw(deck.draw());
        }
        discardPile.add(deck.draw());
        Scanner scanner = new Scanner(System.in);
        while (!isGameOver()) {
            CanastaPlayer p = players[currentPlayer];
            System.out.println("\n" + p.name + "'s turn. Score: " + p.score);
            System.out.println("Hand: " + p.hand);
            System.out.println("Top of discard: " + discardPile.get(discardPile.size() - 1));
            // Draw
            if (p.name.equals("You")) {
                System.out.print("Draw from (1) Deck or (2) Discard? ");
                int choice = scanner.nextInt();
                if (choice == 2 && !discardPile.isEmpty()) {
                    p.draw(discardPile.remove(discardPile.size() - 1));
                } else {
                    p.draw(deck.draw());
                }
            } else {
                // Simple AI: always draw from deck
                p.draw(deck.draw());
            }
            // Discard
            Card toDiscard = p.hand.get(0); // Always discard first card (simplified)
            p.discard(toDiscard);
            discardPile.add(toDiscard);
            System.out.println(p.name + " discards: " + toDiscard);
            // End turn
            currentPlayer = 1 - currentPlayer;
        }
        // Scoring (simplified)
        for (CanastaPlayer p : players) {
            p.score += p.hand.size() * -5;
            System.out.println(p.name + " final score: " + p.score);
        }
        System.out.println("Game over!");
    }
    private boolean isGameOver() {
        for (CanastaPlayer p : players) {
            if (p.hand.isEmpty()) return true;
        }
        return deck.isEmpty();
    }
    public static void main(String[] args) {
        new CanastaGame().start();
    }
}
