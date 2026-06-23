package texasholdem;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Evaluates and ranks poker hands.
 */
public class PokerHand {
    public enum HandRank {
        HIGH_CARD(1, "High Card"),
        ONE_PAIR(2, "One Pair"),
        TWO_PAIR(3, "Two Pair"),
        THREE_OF_A_KIND(4, "Three of a Kind"),
        STRAIGHT(5, "Straight"),
        FLUSH(6, "Flush"),
        FULL_HOUSE(7, "Full House"),
        FOUR_OF_A_KIND(8, "Four of a Kind"),
        STRAIGHT_FLUSH(9, "Straight Flush"),
        ROYAL_FLUSH(10, "Royal Flush");
        
        private final int rank;
        private final String name;
        
        HandRank(int rank, String name) {
            this.rank = rank;
            this.name = name;
        }
        
        public int getRank() {
            return rank;
        }
        
        public String getName() {
            return name;
        }
    }
    
    private final List<Card> cards;
    private HandRank handRank;
    private List<Integer> tiebreakers;
    
    /**
     * Creates a poker hand from a list of 5 cards (best 5 from 7 in Texas Hold'em).
     */
    public PokerHand(List<Card> cards) {
        if (cards.size() != 5) {
            throw new IllegalArgumentException("A poker hand must contain exactly 5 cards");
        }
        this.cards = new ArrayList<>(cards);
        this.cards.sort(Collections.reverseOrder());
        evaluate();
    }
    
    /**
     * Evaluates the hand and determines its rank and tiebreakers.
     */
    private void evaluate() {
        if (isRoyalFlush()) {
            handRank = HandRank.ROYAL_FLUSH;
            tiebreakers = List.of(14); // Ace high
        } else if (isStraightFlush()) {
            handRank = HandRank.STRAIGHT_FLUSH;
            tiebreakers = getStraightHighCard();
        } else if (isFourOfAKind()) {
            handRank = HandRank.FOUR_OF_A_KIND;
            tiebreakers = getFourOfAKindTiebreaker();
        } else if (isFullHouse()) {
            handRank = HandRank.FULL_HOUSE;
            tiebreakers = getFullHouseTiebreaker();
        } else if (isFlush()) {
            handRank = HandRank.FLUSH;
            tiebreakers = getFlushTiebreaker();
        } else if (isStraight()) {
            handRank = HandRank.STRAIGHT;
            tiebreakers = getStraightHighCard();
        } else if (isThreeOfAKind()) {
            handRank = HandRank.THREE_OF_A_KIND;
            tiebreakers = getThreeOfAKindTiebreaker();
        } else if (isTwoPair()) {
            handRank = HandRank.TWO_PAIR;
            tiebreakers = getTwoPairTiebreaker();
        } else if (isOnePair()) {
            handRank = HandRank.ONE_PAIR;
            tiebreakers = getOnePairTiebreaker();
        } else {
            handRank = HandRank.HIGH_CARD;
            tiebreakers = getHighCardTiebreaker();
        }
    }
    
    private boolean isRoyalFlush() {
        return isStraightFlush() && cards.get(0).getRank() == Card.Rank.ACE;
    }
    
    private boolean isStraightFlush() {
        return isStraight() && isFlush();
    }
    
    private boolean isFourOfAKind() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        return rankCounts.containsValue(4);
    }
    
    private boolean isFullHouse() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        return rankCounts.containsValue(3) && rankCounts.containsValue(2);
    }
    
    private boolean isFlush() {
        Card.Suit firstSuit = cards.get(0).getSuit();
        return cards.stream().allMatch(c -> c.getSuit() == firstSuit);
    }
    
    private boolean isStraight() {
        // Handle ace-low straight (A,2,3,4,5)
        List<Integer> values = cards.stream()
            .map(c -> c.getRank().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        
        // Check for regular straight
        boolean isRegularStraight = true;
        for (int i = 0; i < 4; i++) {
            if (values.get(i) - values.get(i + 1) != 1) {
                isRegularStraight = false;
                break;
            }
        }
        
        if (isRegularStraight) {
            return true;
        }
        
        // Check for ace-low straight (14, 5, 4, 3, 2)
        if (values.equals(List.of(14, 5, 4, 3, 2))) {
            return true;
        }
        
        return false;
    }
    
    private boolean isThreeOfAKind() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        return rankCounts.containsValue(3) && !rankCounts.containsValue(2);
    }
    
    private boolean isTwoPair() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        long pairCount = rankCounts.values().stream().filter(v -> v == 2).count();
        return pairCount == 2;
    }
    
    private boolean isOnePair() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        return rankCounts.containsValue(2);
    }
    
    private Map<Card.Rank, Integer> countRanks() {
        Map<Card.Rank, Integer> counts = new HashMap<>();
        for (Card card : cards) {
            counts.put(card.getRank(), counts.getOrDefault(card.getRank(), 0) + 1);
        }
        return counts;
    }
    
    private List<Integer> getStraightHighCard() {
        List<Integer> values = cards.stream()
            .map(c -> c.getRank().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        
        // Check for ace-low straight
        if (values.equals(List.of(14, 5, 4, 3, 2))) {
            return List.of(5); // In ace-low straight, 5 is high
        }
        
        return List.of(values.get(0));
    }
    
    private List<Integer> getFourOfAKindTiebreaker() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        int fourKind = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 4)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        int kicker = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 1)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        return List.of(fourKind, kicker);
    }
    
    private List<Integer> getFullHouseTiebreaker() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        int threeKind = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 3)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        int pair = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 2)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        return List.of(threeKind, pair);
    }
    
    private List<Integer> getFlushTiebreaker() {
        return cards.stream()
            .map(c -> c.getRank().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
    }
    
    private List<Integer> getThreeOfAKindTiebreaker() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        int threeKind = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 3)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        List<Integer> kickers = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 1)
            .map(e -> e.getKey().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        List<Integer> result = new ArrayList<>();
        result.add(threeKind);
        result.addAll(kickers);
        return result;
    }
    
    private List<Integer> getTwoPairTiebreaker() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        List<Integer> pairs = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 2)
            .map(e -> e.getKey().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        int kicker = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 1)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        List<Integer> result = new ArrayList<>(pairs);
        result.add(kicker);
        return result;
    }
    
    private List<Integer> getOnePairTiebreaker() {
        Map<Card.Rank, Integer> rankCounts = countRanks();
        int pair = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 2)
            .map(e -> e.getKey().getValue())
            .findFirst()
            .orElse(0);
        List<Integer> kickers = rankCounts.entrySet().stream()
            .filter(e -> e.getValue() == 1)
            .map(e -> e.getKey().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
        List<Integer> result = new ArrayList<>();
        result.add(pair);
        result.addAll(kickers);
        return result;
    }
    
    private List<Integer> getHighCardTiebreaker() {
        return cards.stream()
            .map(c -> c.getRank().getValue())
            .sorted(Comparator.reverseOrder())
            .collect(Collectors.toList());
    }
    
    public HandRank getHandRank() {
        return handRank;
    }
    
    public List<Integer> getTiebreakers() {
        return tiebreakers;
    }
    
    /**
     * Compares this hand with another hand.
     * Returns positive if this hand is better, negative if other is better, 0 if equal.
     */
    public int compareTo(PokerHand other) {
        if (this.handRank.getRank() != other.handRank.getRank()) {
            return this.handRank.getRank() - other.handRank.getRank();
        }
        
        // Same hand rank, check tiebreakers
        List<Integer> thisTiebreakers = this.tiebreakers;
        List<Integer> otherTiebreakers = other.tiebreakers;
        
        for (int i = 0; i < Math.min(thisTiebreakers.size(), otherTiebreakers.size()); i++) {
            if (!thisTiebreakers.get(i).equals(otherTiebreakers.get(i))) {
                return thisTiebreakers.get(i) - otherTiebreakers.get(i);
            }
        }
        
        return 0; // Hands are equal
    }
    
    @Override
    public String toString() {
        return handRank.getName() + ": " + cards;
    }
}
