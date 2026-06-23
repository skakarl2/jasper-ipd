package texasholdem;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Manages a Texas Hold'em poker game.
 */
public class TexasHoldEm {
    private final List<Player> players;
    private final Deck deck;
    private List<Card> communityCards;
    private int buttonPosition;
    private int smallBlindPosition;
    private int bigBlindPosition;
    private double smallBlind;
    private double bigBlind;
    private int handNumber;
    
    public enum GamePhase {
        PREFLOP, FLOP, TURN, RIVER, SHOWDOWN, ENDED
    }
    
    private GamePhase currentPhase;
    
    /**
     * Creates a new Texas Hold'em game with the given players.
     * @param players List of players (minimum 2, maximum 10)
     * @param startingChips Starting chip count for each player
     * @param smallBlind Small blind amount
     */
    public TexasHoldEm(List<Player> players, double startingChips, double smallBlind) {
        if (players.size() < 2 || players.size() > 10) {
            throw new IllegalArgumentException("Game requires 2-10 players");
        }
        
        this.players = new ArrayList<>(players);
        this.deck = new Deck();
        this.communityCards = new ArrayList<>();
        this.smallBlind = smallBlind;
        this.bigBlind = smallBlind * 2;
        this.buttonPosition = 0;
        this.handNumber = 0;
        this.currentPhase = GamePhase.PREFLOP;
    }
    
    /**
     * Initializes a new hand of poker.
     */
    public void startNewHand() {
        handNumber++;
        
        // Reset players
        players.forEach(Player::resetForNewHand);
        
        // Reset deck and community cards
        deck.reset();
        deck.shuffle();
        communityCards.clear();
        currentPhase = GamePhase.PREFLOP;
        
        // Update positions
        advancePositions();
        
        // Post blinds
        players.get(smallBlindPosition).bet(smallBlind);
        players.get(bigBlindPosition).bet(bigBlind);
        
        // Deal hole cards
        for (int i = 0; i < 2; i++) {
            for (Player player : players) {
                if (deck.hasCards()) {
                    player.dealCard(deck.deal());
                }
            }
        }
    }
    
    /**
     * Advances to the next game phase and deals community cards.
     */
    public void advancePhase() {
        switch (currentPhase) {
            case PREFLOP:
                currentPhase = GamePhase.FLOP;
                dealFlop();
                break;
            case FLOP:
                currentPhase = GamePhase.TURN;
                dealTurn();
                break;
            case TURN:
                currentPhase = GamePhase.RIVER;
                dealRiver();
                break;
            case RIVER:
                currentPhase = GamePhase.SHOWDOWN;
                break;
            case SHOWDOWN:
                currentPhase = GamePhase.ENDED;
                break;
        }
        
        // Reset bets for new phase
        for (Player player : players) {
            if (!player.isAllIn()) {
                player.resetCurrentBet();
            }
        }
    }
    
    private void dealFlop() {
        deck.deal(); // Burn card
        for (int i = 0; i < 3; i++) {
            communityCards.add(deck.deal());
        }
    }
    
    private void dealTurn() {
        deck.deal(); // Burn card
        communityCards.add(deck.deal());
    }
    
    private void dealRiver() {
        deck.deal(); // Burn card
        communityCards.add(deck.deal());
    }
    
    /**
     * Gets the best 5-card hand from 7 available cards (2 hole + 5 community).
     */
    public PokerHand getBestHand(Player player) {
        List<Card> allCards = new ArrayList<>(player.getHoleCards());
        allCards.addAll(communityCards);
        
        if (allCards.size() < 5) {
            return null; // Not enough cards yet
        }
        
        // Generate all combinations of 5 cards from 7
        List<PokerHand> possibleHands = new ArrayList<>();
        for (int i = 0; i < allCards.size(); i++) {
            for (int j = i + 1; j < allCards.size(); j++) {
                List<Card> temp = new ArrayList<>(allCards);
                temp.remove(Math.max(i, j));
                temp.remove(Math.min(i, j));
                possibleHands.add(new PokerHand(temp));
            }
        }
        
        return possibleHands.stream()
            .max(Comparator.reverseOrder())
            .orElse(null);
    }
    
    /**
     * Determines the winner(s) of the hand and awards the pot.
     */
    public List<Player> determineWinners() {
        List<Player> activePlayers = players.stream()
            .filter(p -> !p.isFolded())
            .collect(Collectors.toList());
        
        if (activePlayers.size() == 1) {
            // Everyone else folded
            return activePlayers;
        }
        
        // Compare hands
        PokerHand bestHand = null;
        List<Player> winners = new ArrayList<>();
        
        for (Player player : activePlayers) {
            PokerHand hand = getBestHand(player);
            if (bestHand == null || hand.compareTo(bestHand) > 0) {
                bestHand = hand;
                winners.clear();
                winners.add(player);
            } else if (bestHand != null && hand.compareTo(bestHand) == 0) {
                winners.add(player);
            }
        }
        
        return winners;
    }
    
    /**
     * Gets the total pot (sum of all player current bets).
     */
    public double getTotalPot() {
        return players.stream()
            .mapToDouble(Player::getCurrentBet)
            .sum();
    }
    
    /**
     * Awards chips from the pot to the winner(s).
     */
    public void awardPot(List<Player> winners) {
        if (winners.isEmpty()) {
            return;
        }
        
        double pot = getTotalPot();
        double winningShare = pot / winners.size();
        
        for (Player winner : winners) {
            winner.addChips(winningShare);
        }
    }
    
    private void advancePositions() {
        buttonPosition = (buttonPosition + 1) % players.size();
        smallBlindPosition = (buttonPosition + 1) % players.size();
        bigBlindPosition = (bigBlindPosition + 1) % players.size();
    }
    
    public GamePhase getCurrentPhase() {
        return currentPhase;
    }
    
    public List<Player> getPlayers() {
        return new ArrayList<>(players);
    }
    
    public List<Card> getCommunityCards() {
        return new ArrayList<>(communityCards);
    }
    
    public int getButtonPosition() {
        return buttonPosition;
    }
    
    public int getSmallBlindPosition() {
        return smallBlindPosition;
    }
    
    public int getBigBlindPosition() {
        return bigBlindPosition;
    }
    
    public int getHandNumber() {
        return handNumber;
    }
    
    public double getTotalChipsInGame() {
        return players.stream()
            .mapToDouble(Player::getChips)
            .sum() + getTotalPot();
    }
    
    /**
     * Returns a string representation of the current game state.
     */
    public String getGameState() {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Hand #").append(handNumber).append(" ===\n");
        sb.append("Phase: ").append(currentPhase).append("\n");
        sb.append("Pot: $").append(getTotalPot()).append("\n");
        sb.append("Community Cards: ").append(communityCards).append("\n");
        sb.append("\nPlayers:\n");
        
        for (int i = 0; i < players.size(); i++) {
            Player player = players.get(i);
            String position = "";
            if (i == buttonPosition) position += " (BUTTON)";
            if (i == smallBlindPosition) position += " (SMALL BLIND)";
            if (i == bigBlindPosition) position += " (BIG BLIND)";
            
            sb.append(player).append(position).append("\n");
        }
        
        return sb.toString();
    }
}
