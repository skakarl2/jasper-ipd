package texasholdem;

import java.util.*;

/**
 * Unit tests for Texas Hold'em poker components.
 */
public class PokerTest {
    
    public static void main(String[] args) {
        testPokerHands();
        testDeck();
        testPlayer();
        System.out.println("\n✓ All tests passed!");
    }
    
    private static void testPokerHands() {
        System.out.println("Testing Poker Hands...");
        
        // Test Royal Flush
        List<Card> royalFlush = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.KING, Card.Suit.HEARTS),
            new Card(Card.Rank.QUEEN, Card.Suit.HEARTS),
            new Card(Card.Rank.JACK, Card.Suit.HEARTS),
            new Card(Card.Rank.TEN, Card.Suit.HEARTS)
        );
        PokerHand royal = new PokerHand(royalFlush);
        assert royal.getHandRank() == PokerHand.HandRank.ROYAL_FLUSH : 
            "Failed to detect royal flush";
        System.out.println("  ✓ Royal Flush detected");
        
        // Test Straight Flush
        List<Card> straightFlush = Arrays.asList(
            new Card(Card.Rank.NINE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.EIGHT, Card.Suit.DIAMONDS),
            new Card(Card.Rank.SEVEN, Card.Suit.DIAMONDS),
            new Card(Card.Rank.SIX, Card.Suit.DIAMONDS),
            new Card(Card.Rank.FIVE, Card.Suit.DIAMONDS)
        );
        PokerHand straight = new PokerHand(straightFlush);
        assert straight.getHandRank() == PokerHand.HandRank.STRAIGHT_FLUSH : 
            "Failed to detect straight flush";
        System.out.println("  ✓ Straight Flush detected");
        
        // Test Four of a Kind
        List<Card> fourOfAKind = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.ACE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.ACE, Card.Suit.CLUBS),
            new Card(Card.Rank.ACE, Card.Suit.SPADES),
            new Card(Card.Rank.KING, Card.Suit.HEARTS)
        );
        PokerHand four = new PokerHand(fourOfAKind);
        assert four.getHandRank() == PokerHand.HandRank.FOUR_OF_A_KIND : 
            "Failed to detect four of a kind";
        System.out.println("  ✓ Four of a Kind detected");
        
        // Test Full House
        List<Card> fullHouse = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.ACE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.ACE, Card.Suit.CLUBS),
            new Card(Card.Rank.KING, Card.Suit.HEARTS),
            new Card(Card.Rank.KING, Card.Suit.DIAMONDS)
        );
        PokerHand full = new PokerHand(fullHouse);
        assert full.getHandRank() == PokerHand.HandRank.FULL_HOUSE : 
            "Failed to detect full house";
        System.out.println("  ✓ Full House detected");
        
        // Test Flush
        List<Card> flush = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.KING, Card.Suit.HEARTS),
            new Card(Card.Rank.QUEEN, Card.Suit.HEARTS),
            new Card(Card.Rank.JACK, Card.Suit.HEARTS),
            new Card(Card.Rank.NINE, Card.Suit.HEARTS)
        );
        PokerHand flushHand = new PokerHand(flush);
        assert flushHand.getHandRank() == PokerHand.HandRank.FLUSH : 
            "Failed to detect flush";
        System.out.println("  ✓ Flush detected");
        
        // Test Straight
        List<Card> straightHand = Arrays.asList(
            new Card(Card.Rank.NINE, Card.Suit.HEARTS),
            new Card(Card.Rank.EIGHT, Card.Suit.DIAMONDS),
            new Card(Card.Rank.SEVEN, Card.Suit.CLUBS),
            new Card(Card.Rank.SIX, Card.Suit.SPADES),
            new Card(Card.Rank.FIVE, Card.Suit.HEARTS)
        );
        PokerHand straightHandObj = new PokerHand(straightHand);
        assert straightHandObj.getHandRank() == PokerHand.HandRank.STRAIGHT : 
            "Failed to detect straight";
        System.out.println("  ✓ Straight detected");
        
        // Test Three of a Kind
        List<Card> threeOfAKind = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.ACE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.ACE, Card.Suit.CLUBS),
            new Card(Card.Rank.KING, Card.Suit.HEARTS),
            new Card(Card.Rank.QUEEN, Card.Suit.HEARTS)
        );
        PokerHand three = new PokerHand(threeOfAKind);
        assert three.getHandRank() == PokerHand.HandRank.THREE_OF_A_KIND : 
            "Failed to detect three of a kind";
        System.out.println("  ✓ Three of a Kind detected");
        
        // Test Two Pair
        List<Card> twoPair = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.ACE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.KING, Card.Suit.CLUBS),
            new Card(Card.Rank.KING, Card.Suit.HEARTS),
            new Card(Card.Rank.QUEEN, Card.Suit.HEARTS)
        );
        PokerHand twoPairObj = new PokerHand(twoPair);
        assert twoPairObj.getHandRank() == PokerHand.HandRank.TWO_PAIR : 
            "Failed to detect two pair";
        System.out.println("  ✓ Two Pair detected");
        
        // Test One Pair
        List<Card> onePair = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.ACE, Card.Suit.DIAMONDS),
            new Card(Card.Rank.KING, Card.Suit.CLUBS),
            new Card(Card.Rank.QUEEN, Card.Suit.HEARTS),
            new Card(Card.Rank.JACK, Card.Suit.HEARTS)
        );
        PokerHand pair = new PokerHand(onePair);
        assert pair.getHandRank() == PokerHand.HandRank.ONE_PAIR : 
            "Failed to detect one pair";
        System.out.println("  ✓ One Pair detected");
        
        // Test High Card
        List<Card> highCard = Arrays.asList(
            new Card(Card.Rank.ACE, Card.Suit.HEARTS),
            new Card(Card.Rank.KING, Card.Suit.DIAMONDS),
            new Card(Card.Rank.QUEEN, Card.Suit.CLUBS),
            new Card(Card.Rank.JACK, Card.Suit.HEARTS),
            new Card(Card.Rank.NINE, Card.Suit.HEARTS)
        );
        PokerHand high = new PokerHand(highCard);
        assert high.getHandRank() == PokerHand.HandRank.HIGH_CARD : 
            "Failed to detect high card";
        System.out.println("  ✓ High Card detected");
        
        // Test hand comparison
        assert royal.compareTo(straight) > 0 : "Royal flush should beat straight flush";
        assert straight.compareTo(four) > 0 : "Straight flush should beat four of a kind";
        System.out.println("  ✓ Hand comparison works correctly");
    }
    
    private static void testDeck() {
        System.out.println("\nTesting Deck...");
        
        Deck deck = new Deck();
        assert deck.cardsRemaining() == 52 : "New deck should have 52 cards";
        System.out.println("  ✓ Deck initialized with 52 cards");
        
        deck.shuffle();
        assert deck.cardsRemaining() == 52 : "Shuffled deck should still have 52 cards";
        System.out.println("  ✓ Deck shuffled correctly");
        
        Card card = deck.deal();
        assert card != null : "Dealt card should not be null";
        assert deck.cardsRemaining() == 51 : "Deck should have 51 cards after dealing";
        System.out.println("  ✓ Card dealt correctly");
        
        for (int i = 0; i < 51; i++) {
            deck.deal();
        }
        assert deck.cardsRemaining() == 0 : "Deck should be empty";
        System.out.println("  ✓ All cards dealt correctly");
        
        try {
            deck.deal();
            assert false : "Should throw exception when dealing from empty deck";
        } catch (IllegalStateException e) {
            System.out.println("  ✓ Exception thrown for empty deck");
        }
    }
    
    private static void testPlayer() {
        System.out.println("\nTesting Player...");
        
        Player player = new Player("TestPlayer", 1000);
        assert player.getName().equals("TestPlayer") : "Player name should match";
        assert player.getChips() == 1000 : "Starting chips should be 1000";
        System.out.println("  ✓ Player initialized correctly");
        
        player.dealCard(new Card(Card.Rank.ACE, Card.Suit.HEARTS));
        player.dealCard(new Card(Card.Rank.KING, Card.Suit.HEARTS));
        assert player.getHoleCards().size() == 2 : "Player should have 2 hole cards";
        System.out.println("  ✓ Hole cards dealt correctly");
        
        player.bet(100);
        assert player.getChips() == 900 : "Chips should be reduced by bet";
        assert player.getCurrentBet() == 100 : "Current bet should be 100";
        System.out.println("  ✓ Betting works correctly");
        
        player.fold();
        assert player.isFolded() : "Player should be folded";
        System.out.println("  ✓ Folding works correctly");
        
        player.resetForNewHand();
        assert !player.isFolded() : "Player should not be folded after reset";
        assert player.getHoleCards().isEmpty() : "Hole cards should be cleared";
        assert player.getCurrentBet() == 0 : "Current bet should be 0";
        System.out.println("  ✓ Hand reset works correctly");
    }
}
