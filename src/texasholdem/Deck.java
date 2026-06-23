package texasholdem;

import java.util.*;

/**
 * Represents a standard 52-card deck used in poker.
 */
public class Deck {
    private final List<Card> cards;
    private final Random random;
    
    /**
     * Creates a new deck with all 52 standard cards.
     */
    public Deck() {
        this.cards = new ArrayList<>();
        this.random = new Random();
        initializeDeck();
    }
    
    /**
     * Initializes the deck with all 52 standard cards.
     */
    private void initializeDeck() {
        for (Card.Suit suit : Card.Suit.values()) {
            for (Card.Rank rank : Card.Rank.values()) {
                cards.add(new Card(rank, suit));
            }
        }
    }
    
    /**
     * Shuffles the deck using Fisher-Yates algorithm.
     */
    public void shuffle() {
        for (int i = cards.size() - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            Collections.swap(cards, i, j);
        }
    }
    
    /**
     * Deals (removes and returns) the top card from the deck.
     * 
     * @return the top card
     * @throws IllegalStateException if the deck is empty
     */
    public Card deal() {
        if (cards.isEmpty()) {
            throw new IllegalStateException("No cards left in deck");
        }
        return cards.remove(0);
    }
    
    /**
     * Returns the number of cards remaining in the deck.
     */
    public int cardsRemaining() {
        return cards.size();
    }
    
    /**
     * Checks if the deck has cards remaining.
     */
    public boolean hasCards() {
        return !cards.isEmpty();
    }
    
    /**
     * Resets the deck to a full 52 cards.
     */
    public void reset() {
        cards.clear();
        initializeDeck();
    }
    
    @Override
    public String toString() {
        return "Deck with " + cards.size() + " cards";
    }
}
