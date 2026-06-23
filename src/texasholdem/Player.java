package texasholdem;

import java.util.*;

/**
 * Represents a player in a Texas Hold'em poker game.
 */
public class Player {
    private final String name;
    private double chips;
    private List<Card> holeCards;
    private double currentBet;
    private boolean folded;
    private boolean allIn;
    
    /**
     * Creates a new player with the given name and starting chips.
     */
    public Player(String name, double startingChips) {
        this.name = name;
        this.chips = startingChips;
        this.holeCards = new ArrayList<>();
        this.currentBet = 0;
        this.folded = false;
        this.allIn = false;
    }
    
    public String getName() {
        return name;
    }
    
    public double getChips() {
        return chips;
    }
    
    public void addChips(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Cannot add negative chips");
        }
        this.chips += amount;
    }
    
    public void removeChips(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Cannot remove negative chips");
        }
        if (amount > chips) {
            throw new IllegalArgumentException("Not enough chips");
        }
        this.chips -= amount;
    }
    
    public void dealCard(Card card) {
        if (holeCards.size() >= 2) {
            throw new IllegalStateException("Player already has 2 hole cards");
        }
        holeCards.add(card);
    }
    
    public List<Card> getHoleCards() {
        return new ArrayList<>(holeCards);
    }
    
    public void clearHoleCards() {
        holeCards.clear();
    }
    
    public double getCurrentBet() {
        return currentBet;
    }
    
    public void setCurrentBet(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Bet cannot be negative");
        }
        this.currentBet = amount;
    }
    
    public void resetCurrentBet() {
        this.currentBet = 0;
    }
    
    public boolean isFolded() {
        return folded;
    }
    
    public void fold() {
        this.folded = true;
    }
    
    public void unfold() {
        this.folded = false;
    }
    
    public boolean isAllIn() {
        return allIn;
    }
    
    public void setAllIn(boolean allIn) {
        this.allIn = allIn;
    }
    
    public void resetForNewHand() {
        clearHoleCards();
        currentBet = 0;
        folded = false;
        allIn = false;
    }
    
    public boolean canBet(double amount) {
        return chips >= amount;
    }
    
    /**
     * Makes a bet. If the amount exceeds available chips, goes all-in.
     * Returns the actual amount bet.
     */
    public double bet(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Bet amount cannot be negative");
        }
        
        double actualBet = Math.min(amount, chips);
        removeChips(actualBet);
        currentBet += actualBet;
        
        if (chips == 0) {
            allIn = true;
        }
        
        return actualBet;
    }
    
    public boolean isActive() {
        return !folded && chips >= 0;
    }
    
    public boolean canActInRound() {
        return !folded && !allIn && chips > 0;
    }
    
    @Override
    public String toString() {
        return name + " [Chips: " + chips + ", Bet: " + currentBet + 
               (folded ? ", FOLDED" : "") + (allIn ? ", ALL-IN" : "") + "]";
    }
}
