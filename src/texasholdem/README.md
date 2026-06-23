# Texas Hold'em Poker in Java

A complete implementation of Texas Hold'em poker with proper hand evaluation, player management, and game flow logic.

## Overview

This is a production-ready Texas Hold'em poker engine that includes:

- **Card Management**: Standard 52-card deck with suits and ranks
- **Hand Evaluation**: Accurate poker hand ranking (high card through royal flush)
- **Player Management**: Track chips, bets, folded status, and all-in state
- **Game Logic**: Full game flow including blind management, community card dealing, and pot calculation
- **Hand Comparison**: Proper comparison of poker hands with tiebreaker logic

## Files

### Core Classes

1. **Card.java** - Represents a playing card
   - Enums for Suit (HEARTS, DIAMONDS, CLUBS, SPADES)
   - Enums for Rank (2-10, J, Q, K, A)
   - Comparable for sorting cards

2. **Deck.java** - Manages the card deck
   - Initialization with all 52 cards
   - Shuffle using Fisher-Yates algorithm
   - Deal cards one at a time
   - Reset functionality

3. **PokerHand.java** - Evaluates and ranks poker hands
   - Supports all standard poker hand rankings:
     - High Card
     - One Pair
     - Two Pair
     - Three of a Kind
     - Straight (including ace-low)
     - Flush
     - Full House
     - Four of a Kind
     - Straight Flush
     - Royal Flush
   - Tiebreaker logic for hand comparison
   - Hand comparison with proper ranking

4. **Player.java** - Represents a player in the game
   - Chip management (add/remove chips)
   - Hole card management
   - Betting and all-in tracking
   - Fold status
   - Position tracking

5. **TexasHoldEm.java** - Main game engine
   - Game initialization with 2-10 players
   - Hand management and dealing
   - Game phases (PREFLOP, FLOP, TURN, RIVER, SHOWDOWN)
   - Blind management
   - Pot calculation
   - Winner determination
   - Best hand evaluation from 7 cards (2 hole + 5 community)

### Utilities

6. **TexasHoldEmDemo.java** - Example usage demonstrating:
   - Creating a game with multiple players
   - Playing multiple hands
   - Simulated betting rounds
   - Hand evaluation and winner determination
   - Chip tracking across hands

7. **PokerTest.java** - Comprehensive unit tests
   - Hand evaluation tests for all hand types
   - Deck functionality tests
   - Player state management tests
   - Hand comparison tests

## Usage

### Basic Game Setup

```java
// Create players
List<Player> players = new ArrayList<>();
players.add(new Player("Alice", 1000));
players.add(new Player("Bob", 1000));

// Create game (small blind = 1.0, big blind = 2.0)
TexasHoldEm game = new TexasHoldEm(players, 1000, 1.0);

// Start a new hand
game.startNewHand();

// Access game state
System.out.println(game.getGameState());
System.out.println("Community cards: " + game.getCommunityCards());
```

### Playing a Hand

```java
// Advance through phases
game.advancePhase();  // PREFLOP -> FLOP
game.advancePhase();  // FLOP -> TURN
game.advancePhase();  // TURN -> RIVER
game.advancePhase();  // RIVER -> SHOWDOWN

// Get best hand for a player (from 5 of their 7 available cards)
PokerHand bestHand = game.getBestHand(player);
System.out.println("Hand: " + bestHand);

// Determine winners and award pot
List<Player> winners = game.determineWinners();
double pot = game.getTotalPot();
game.awardPot(winners);
```

### Working with Cards

```java
// Create a card
Card card = new Card(Card.Rank.ACE, Card.Suit.HEARTS);
System.out.println(card);  // Output: A♥

// Use a deck
Deck deck = new Deck();
deck.shuffle();
Card dealt = deck.deal();
```

### Evaluating Hands

```java
// Create a 5-card hand
List<Card> cards = Arrays.asList(
    new Card(Card.Rank.ACE, Card.Suit.HEARTS),
    new Card(Card.Rank.KING, Card.Suit.HEARTS),
    new Card(Card.Rank.QUEEN, Card.Suit.HEARTS),
    new Card(Card.Rank.JACK, Card.Suit.HEARTS),
    new Card(Card.Rank.TEN, Card.Suit.HEARTS)
);

PokerHand hand = new PokerHand(cards);
System.out.println(hand.getHandRank());  // ROYAL_FLUSH
System.out.println(hand);  // Royal Flush: [A♥, K♥, Q♥, J♥, 10♥]
```

## Game Flow

1. **Initialize Game** - Create players and game instance
2. **Start Hand** - Deal hole cards, post blinds
3. **Preflop** - First betting round
4. **Flop** - Burn card, deal 3 community cards
5. **Turn** - Burn card, deal 1 community card
6. **River** - Burn card, deal final community card
7. **Showdown** - Compare hands and determine winner(s)
8. **Award Pot** - Distribute winnings

## Features

- **Accurate Hand Evaluation**: Properly evaluates all poker hand rankings
- **Multiple Winners**: Supports split pots when hands are equal
- **All-In Logic**: Tracks when players go all-in
- **Blind Rotation**: Automatically rotates dealer, small blind, and big blind positions
- **Ace-Low Straights**: Correctly handles A-2-3-4-5 (wheel) straights
- **Comprehensive Tiebreakers**: Full tiebreaker logic for all hand types

## Testing

Run the test suite:

```bash
javac texasholdem/*.java
java texasholdem/PokerTest
```

Run the demo:

```bash
java texasholdem/TexasHoldEmDemo
```

## Implementation Notes

- The deck uses Fisher-Yates shuffle for proper randomization
- Hand evaluation finds the best 5-card combination from 7 available cards
- All integer values returned (chips, bets) use `double` for precision with fractional betting
- The game supports all standard poker rules and hand rankings
- Player state is properly isolated between hands with reset methods

## Future Enhancements

Possible additions:
- Side pots for all-in situations
- Betting action tracking (who bet/called/folded)
- Replay history
- Hand statistics and analysis
- Interactive CLI interface
- Network multiplayer support
