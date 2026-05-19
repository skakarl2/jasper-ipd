package holdem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.StringJoiner;

public class TexasHoldemGame {
    private static final int STARTING_CHIPS = 500;
    private static final int SMALL_BLIND = 10;
    private static final int BIG_BLIND = 20;
    private static final int MIN_PLAYERS = 2;
    private static final int MAX_PLAYERS = 8;

    private final List<Player> players;
    private final Scanner scanner;
    private int dealerIndex;
    private boolean quitRequested;

    public TexasHoldemGame(List<Player> players, Scanner scanner) {
        this.players = players;
        this.scanner = scanner;
        this.dealerIndex = -1;
    }

    public static void main(String[] args) {
        System.out.println("Welcome to Texas Hold'em!");
        System.out.println("Commands: check, call, fold, raise <amount>, all-in, status, help, quit\n");

        try (Scanner scanner = new Scanner(System.in)) {
            List<Player> players = setupPlayers(scanner);
            if (players.isEmpty()) {
                System.out.println("Setup cancelled.");
                return;
            }
            TexasHoldemGame game = new TexasHoldemGame(players, scanner);
            game.run();
        }
    }

    private static List<Player> setupPlayers(Scanner scanner) {
        int playerCount = 0;
        while (playerCount < MIN_PLAYERS || playerCount > MAX_PLAYERS) {
            System.out.print("How many players (2-8)? ");
            String input = readLine(scanner);
            if (input == null) {
                return List.of();
            }
            input = input.trim();
            try {
                playerCount = Integer.parseInt(input);
            } catch (NumberFormatException error) {
                playerCount = 0;
            }

            if (playerCount < MIN_PLAYERS || playerCount > MAX_PLAYERS) {
                System.out.println("Please enter a number from 2 to 8.\n");
            }
        }

        List<Player> players = new ArrayList<>();
        for (int index = 0; index < playerCount; index++) {
            System.out.print("Enter player " + (index + 1) + " name: ");
            String name = readLine(scanner);
            if (name == null) {
                return List.of();
            }
            name = name.trim();
            if (name.isEmpty()) {
                name = "Player" + (index + 1);
            }
            players.add(new Player(name, STARTING_CHIPS, index));
        }

        System.out.println();
        return players;
    }

    public void run() {
        while (!quitRequested && countPlayersWithChips() > 1) {
            playHand();
        }

        if (quitRequested) {
            System.out.println("Game ended by player request.");
            printChipCounts();
            return;
        }

        Player winner = lastPlayerWithChips();
        if (winner != null) {
            System.out.println("\n" + winner.name + " wins the table with " + winner.chips + " chips!");
        }
    }

    private void playHand() {
        List<Player> seatedPlayers = playersInSeats();
        if (seatedPlayers.size() < 2) {
            return;
        }

        for (Player player : players) {
            player.resetForHand();
        }

        Deck deck = new Deck();
        List<Card> communityCards = new ArrayList<>();
        dealerIndex = nextSeatWithChips(dealerIndex);
        Player dealer = players.get(dealerIndex);
        int smallBlindIndex = seatedPlayers.size() == 2 ? dealerIndex : nextSeatWithChips(dealerIndex);
        int bigBlindIndex = nextSeatWithChips(smallBlindIndex);
        Player smallBlindPlayer = players.get(smallBlindIndex);
        Player bigBlindPlayer = players.get(bigBlindIndex);

        dealHoleCards(deck);

        int smallBlindPosted = postBlind(smallBlindPlayer, SMALL_BLIND);
        int bigBlindPosted = postBlind(bigBlindPlayer, BIG_BLIND);
        int currentBet = Math.max(smallBlindPosted, bigBlindPosted);

        System.out.println("========================================");
        System.out.println("Dealer: " + dealer.name);
        System.out.println("Small blind: " + smallBlindPlayer.name + " posts " + smallBlindPosted);
        System.out.println("Big blind: " + bigBlindPlayer.name + " posts " + bigBlindPosted);
        System.out.println();

        if (playersStillInHand() > 1) {
            bettingRound("Pre-flop", communityCards, nextSeatWithChips(bigBlindIndex), currentBet, BIG_BLIND);
        }
        if (quitRequested) {
            return;
        }
        if (playersStillInHand() <= 1) {
            awardPotToLastPlayer();
            return;
        }

        burnCard(deck);
        dealCommunity(deck, communityCards, 3);
        resetRoundBets();
        bettingRound("Flop", communityCards, nextSeatWithChips(dealerIndex), 0, BIG_BLIND);
        if (quitRequested) {
            return;
        }
        if (playersStillInHand() <= 1) {
            awardPotToLastPlayer();
            return;
        }

        burnCard(deck);
        dealCommunity(deck, communityCards, 1);
        resetRoundBets();
        bettingRound("Turn", communityCards, nextSeatWithChips(dealerIndex), 0, BIG_BLIND);
        if (quitRequested) {
            return;
        }
        if (playersStillInHand() <= 1) {
            awardPotToLastPlayer();
            return;
        }

        burnCard(deck);
        dealCommunity(deck, communityCards, 1);
        resetRoundBets();
        bettingRound("River", communityCards, nextSeatWithChips(dealerIndex), 0, BIG_BLIND);
        if (quitRequested) {
            return;
        }
        if (playersStillInHand() <= 1) {
            awardPotToLastPlayer();
            return;
        }

        showdown(communityCards, dealerIndex);
    }

    private void bettingRound(String stageName, List<Card> communityCards, int startIndex, int startingBet, int minimumRaise) {
        int currentBet = startingBet;
        int minRaise = minimumRaise;
        Map<Player, Boolean> actedSinceRaise = new HashMap<>();

        for (Player player : players) {
            if (player.canAct()) {
                actedSinceRaise.put(player, false);
            }
        }

        int currentIndex = startIndex;
        while (!quitRequested) {
            if (playersStillInHand() <= 1 || bettingRoundComplete(currentBet, actedSinceRaise)) {
                System.out.println();
                return;
            }

            Player player = players.get(currentIndex);
            currentIndex = nextSeat(currentIndex);

            if (!player.canAct()) {
                continue;
            }

            int toCall = currentBet - player.roundContribution;
            boolean actionComplete = false;

            while (!actionComplete && !quitRequested) {
                promptForPrivateTurn(player);
                if (quitRequested) {
                    return;
                }
                printTableState(stageName, communityCards, player, currentBet);
                System.out.print(player.name + " action: ");
                String input = readLine(scanner);
                if (input == null) {
                    quitRequested = true;
                    return;
                }
                input = input.trim();
                String lowerInput = input.toLowerCase();

                if (lowerInput.equals("help")) {
                    printHelp(toCall, minRaise);
                    continue;
                }
                if (lowerInput.equals("status")) {
                    printChipCounts();
                    continue;
                }
                if (lowerInput.equals("quit")) {
                    quitRequested = true;
                    return;
                }
                if (lowerInput.equals("fold")) {
                    player.folded = true;
                    actedSinceRaise.put(player, true);
                    actionComplete = true;
                    continue;
                }
                if (lowerInput.equals("check")) {
                    if (toCall != 0) {
                        System.out.println("You cannot check while facing a bet.\n");
                        continue;
                    }
                    actedSinceRaise.put(player, true);
                    actionComplete = true;
                    continue;
                }
                if (lowerInput.equals("call")) {
                    if (toCall == 0) {
                        System.out.println("Nothing to call. Use check or raise.\n");
                        continue;
                    }
                    commitChips(player, Math.min(toCall, player.chips));
                    actedSinceRaise.put(player, true);
                    actionComplete = true;
                    continue;
                }
                if (lowerInput.equals("all-in")) {
                    if (player.chips == 0) {
                        System.out.println("You have no chips left.\n");
                        continue;
                    }

                    int previousBet = player.roundContribution;
                    int wager = player.chips;
                    commitChips(player, wager);
                    int newBet = previousBet + wager;
                    boolean isRaise = newBet > currentBet;
                    boolean reopensAction = newBet - currentBet >= minRaise;
                    if (isRaise) {
                        currentBet = newBet;
                    }
                    if (reopensAction) {
                        resetActedFlags(actedSinceRaise);
                        minRaise = newBet - previousBet - toCall;
                        actedSinceRaise.put(player, true);
                    } else {
                        actedSinceRaise.put(player, true);
                    }
                    actionComplete = true;
                    continue;
                }
                if (lowerInput.startsWith("raise ")) {
                    if (player.chips <= toCall) {
                        System.out.println("You do not have enough chips to raise. Use call or all-in.\n");
                        continue;
                    }

                    Integer raiseAmount = parseTrailingNumber(input);
                    if (raiseAmount == null || raiseAmount <= 0) {
                        System.out.println("Use 'raise <amount>' with a positive number.\n");
                        continue;
                    }
                    if (raiseAmount < minRaise) {
                        System.out.println("Minimum raise is " + minRaise + ".\n");
                        continue;
                    }

                    int totalWager = toCall + raiseAmount;
                    if (totalWager > player.chips) {
                        System.out.println("You only have " + player.chips + " chips. Use a smaller raise or all-in.\n");
                        continue;
                    }

                    commitChips(player, totalWager);
                    currentBet = player.roundContribution;
                    minRaise = raiseAmount;
                    resetActedFlags(actedSinceRaise);
                    actedSinceRaise.put(player, true);
                    actionComplete = true;
                    continue;
                }

                System.out.println("Unknown command. Type 'help' for options.\n");
            }
        }
    }

    private boolean bettingRoundComplete(int currentBet, Map<Player, Boolean> actedSinceRaise) {
        int actingPlayers = 0;
        for (Player player : players) {
            if (!player.folded && !player.allIn && player.chips > 0) {
                actingPlayers++;
                if (player.roundContribution != currentBet) {
                    return false;
                }
                if (!Boolean.TRUE.equals(actedSinceRaise.get(player))) {
                    return false;
                }
            }
        }
        return actingPlayers == 0 || actingPlayers > 0;
    }

    private void dealHoleCards(Deck deck) {
        for (int cardNumber = 0; cardNumber < 2; cardNumber++) {
            for (Player player : players) {
                if (player.chips > 0) {
                    player.holeCards.add(deck.draw());
                }
            }
        }
    }

    private void burnCard(Deck deck) {
        deck.draw();
    }

    private void dealCommunity(Deck deck, List<Card> communityCards, int count) {
        for (int index = 0; index < count; index++) {
            communityCards.add(deck.draw());
        }
    }

    private int postBlind(Player player, int blindAmount) {
        int posted = Math.min(blindAmount, player.chips);
        commitChips(player, posted);
        return posted;
    }

    private void commitChips(Player player, int amount) {
        player.chips -= amount;
        player.roundContribution += amount;
        player.totalContribution += amount;
        if (player.chips == 0) {
            player.allIn = true;
        }
    }

    private void resetRoundBets() {
        for (Player player : players) {
            player.roundContribution = 0;
        }
    }

    private void awardPotToLastPlayer() {
        Player winner = null;
        int pot = 0;
        for (Player player : players) {
            pot += player.totalContribution;
            if (!player.folded && player.totalContribution >= 0 && player.holeCards.size() == 2) {
                if (winner == null && !player.folded) {
                    winner = player;
                }
            }
        }

        if (winner != null && pot > 0) {
            winner.chips += pot;
            System.out.println();
            System.out.println(winner.name + " wins the pot of " + pot + " chips.");
            printChipCounts();
        }
    }

    private void showdown(List<Card> communityCards, int dealerSeatIndex) {
        System.out.println("Showdown!");
        Map<Player, HandRank> ranks = new LinkedHashMap<>();
        for (Player player : players) {
            if (!player.folded && player.holeCards.size() == 2) {
                List<Card> cards = new ArrayList<>(communityCards);
                cards.addAll(player.holeCards);
                ranks.put(player, HandEvaluator.bestOfSeven(cards));
            }
        }

        List<SidePot> sidePots = buildSidePots();
        for (SidePot sidePot : sidePots) {
            List<Player> eligible = new ArrayList<>();
            for (Player player : sidePot.eligiblePlayers) {
                if (!player.folded) {
                    eligible.add(player);
                }
            }
            if (eligible.isEmpty()) {
                continue;
            }

            eligible.sort((left, right) -> ranks.get(right).compareTo(ranks.get(left)));
            HandRank bestRank = ranks.get(eligible.get(0));
            List<Player> winners = new ArrayList<>();
            for (Player player : eligible) {
                if (ranks.get(player).compareTo(bestRank) == 0) {
                    winners.add(player);
                }
            }
            splitPot(sidePot.amount, winners, dealerSeatIndex);
        }

        for (Map.Entry<Player, HandRank> entry : ranks.entrySet()) {
            Player player = entry.getKey();
            System.out.println(player.name + " shows " + formatCards(player.holeCards)
                + " -> " + entry.getValue().describe());
        }

        System.out.println("Board: " + formatCards(communityCards));
        printChipCounts();
    }

    private List<SidePot> buildSidePots() {
        List<Integer> levels = new ArrayList<>();
        for (Player player : players) {
            if (player.totalContribution > 0 && !levels.contains(player.totalContribution)) {
                levels.add(player.totalContribution);
            }
        }
        Collections.sort(levels);

        List<SidePot> sidePots = new ArrayList<>();
        int previousLevel = 0;
        for (int level : levels) {
            List<Player> contributors = new ArrayList<>();
            List<Player> eligible = new ArrayList<>();
            for (Player player : players) {
                if (player.totalContribution >= level) {
                    contributors.add(player);
                    if (!player.folded) {
                        eligible.add(player);
                    }
                }
            }

            int amount = (level - previousLevel) * contributors.size();
            if (amount > 0) {
                sidePots.add(new SidePot(amount, eligible));
            }
            previousLevel = level;
        }
        return sidePots;
    }

    private void splitPot(int amount, List<Player> winners, int dealerSeatIndex) {
        int share = amount / winners.size();
        int remainder = amount % winners.size();
        winners.sort(Comparator.comparingInt(player -> distanceFromDealer(dealerSeatIndex, player.seatIndex)));

        for (Player winner : winners) {
            winner.chips += share;
        }
        for (int index = 0; index < remainder; index++) {
            winners.get(index).chips += 1;
        }

        if (winners.size() == 1) {
            System.out.println(winners.get(0).name + " wins " + amount + " chips.");
            return;
        }

        StringJoiner joiner = new StringJoiner(", ");
        for (Player winner : winners) {
            joiner.add(winner.name);
        }
        System.out.println(joiner + " split " + amount + " chips.");
    }

    private int distanceFromDealer(int dealerSeatIndex, int seatIndex) {
        int seatCount = players.size();
        return (seatIndex - dealerSeatIndex + seatCount) % seatCount;
    }

    private void printTableState(String stageName, List<Card> communityCards, Player currentPlayer, int currentBet) {
        System.out.println();
        System.out.println("--- " + stageName + " ---");
        System.out.println("Board: " + (communityCards.isEmpty() ? "(no community cards yet)" : formatCards(communityCards)));
        System.out.println("Pot: " + totalPot());
        System.out.println("Current bet: " + currentBet);
        System.out.println("Your hand: " + formatCards(currentPlayer.holeCards));
        System.out.println("Your stack: " + currentPlayer.chips + " | To call: " + (currentBet - currentPlayer.roundContribution));
        for (Player player : players) {
            if (player.chips == 0 && player.totalContribution == 0) {
                continue;
            }

            String status = player.folded ? "folded" : (player.allIn ? "all-in" : "active");
            System.out.println(player.name + ": chips=" + player.chips + ", hand bet=" + player.totalContribution
                + ", round bet=" + player.roundContribution + ", status=" + status);
        }
    }

    private int totalPot() {
        int total = 0;
        for (Player player : players) {
            total += player.totalContribution;
        }
        return total;
    }

    private void promptForPrivateTurn(Player player) {
        if (countPlayersWithChips() <= 1) {
            return;
        }

        System.out.println();
        System.out.println("Pass the terminal to " + player.name + ". Press Enter when ready.");
        if (readLine(scanner) == null) {
            quitRequested = true;
            return;
        }
        for (int index = 0; index < 20; index++) {
            System.out.println();
        }
    }

    private static String readLine(Scanner scanner) {
        return scanner.hasNextLine() ? scanner.nextLine() : null;
    }

    private void printHelp(int toCall, int minRaise) {
        System.out.println("check         - pass when no bet is facing you");
        System.out.println("call          - match the current bet (" + toCall + " chips right now)");
        System.out.println("fold          - give up the hand");
        System.out.println("raise <n>     - add at least " + minRaise + " chips beyond the call");
        System.out.println("all-in        - bet your remaining stack");
        System.out.println("status        - print chip counts");
        System.out.println("quit          - end the game\n");
    }

    private void printChipCounts() {
        System.out.println();
        System.out.println("Chip counts:");
        for (Player player : players) {
            System.out.println(player.name + ": " + player.chips);
        }
        System.out.println();
    }

    private int countPlayersWithChips() {
        int count = 0;
        for (Player player : players) {
            if (player.chips > 0) {
                count++;
            }
        }
        return count;
    }

    private Player lastPlayerWithChips() {
        for (Player player : players) {
            if (player.chips > 0) {
                return player;
            }
        }
        return null;
    }

    private int playersStillInHand() {
        int count = 0;
        for (Player player : players) {
            if (!player.folded && player.holeCards.size() == 2) {
                count++;
            }
        }
        return count;
    }

    private List<Player> playersInSeats() {
        List<Player> seated = new ArrayList<>();
        for (Player player : players) {
            if (player.chips > 0) {
                seated.add(player);
            }
        }
        return seated;
    }

    private int nextSeatWithChips(int currentIndex) {
        int candidate = currentIndex;
        do {
            candidate = nextSeat(candidate);
        } while (players.get(candidate).chips == 0);
        return candidate;
    }

    private int nextSeat(int currentIndex) {
        return (currentIndex + 1) % players.size();
    }

    private static String formatCards(List<Card> cards) {
        StringJoiner joiner = new StringJoiner(" ");
        for (Card card : cards) {
            joiner.add(card.toString());
        }
        return joiner.toString();
    }

    private static Integer parseTrailingNumber(String input) {
        String[] parts = input.trim().split("\\s+");
        if (parts.length != 2) {
            return null;
        }
        try {
            return Integer.parseInt(parts[1]);
        } catch (NumberFormatException error) {
            return null;
        }
    }

    private static void resetActedFlags(Map<Player, Boolean> actedSinceRaise) {
        for (Map.Entry<Player, Boolean> entry : actedSinceRaise.entrySet()) {
            Player player = entry.getKey();
            if (player.canAct()) {
                entry.setValue(false);
            }
        }
    }
}

class Player {
    final String name;
    final int seatIndex;
    int chips;
    boolean folded;
    boolean allIn;
    int roundContribution;
    int totalContribution;
    final List<Card> holeCards;

    Player(String name, int chips, int seatIndex) {
        this.name = name;
        this.chips = chips;
        this.seatIndex = seatIndex;
        this.holeCards = new ArrayList<>();
    }

    void resetForHand() {
        folded = false;
        allIn = false;
        roundContribution = 0;
        totalContribution = 0;
        holeCards.clear();
    }

    boolean canAct() {
        return !folded && !allIn && chips > 0 && holeCards.size() == 2;
    }
}

class SidePot {
    final int amount;
    final List<Player> eligiblePlayers;

    SidePot(int amount, List<Player> eligiblePlayers) {
        this.amount = amount;
        this.eligiblePlayers = eligiblePlayers;
    }
}

class Deck {
    private final List<Card> cards;
    private int index;

    Deck() {
        cards = new ArrayList<>();
        for (Suit suit : Suit.values()) {
            for (Rank rank : Rank.values()) {
                cards.add(new Card(rank, suit));
            }
        }
        Collections.shuffle(cards);
    }

    Card draw() {
        if (index >= cards.size()) {
            throw new IllegalStateException("The deck is empty.");
        }
        return cards.get(index++);
    }
}

class Card {
    final Rank rank;
    final Suit suit;

    Card(Rank rank, Suit suit) {
        this.rank = rank;
        this.suit = suit;
    }

    @Override
    public String toString() {
        return rank.symbol + suit.symbol;
    }
}

enum Suit {
    CLUBS("C"),
    DIAMONDS("D"),
    HEARTS("H"),
    SPADES("S");

    final String symbol;

    Suit(String symbol) {
        this.symbol = symbol;
    }
}

enum Rank {
    TWO(2, "2"),
    THREE(3, "3"),
    FOUR(4, "4"),
    FIVE(5, "5"),
    SIX(6, "6"),
    SEVEN(7, "7"),
    EIGHT(8, "8"),
    NINE(9, "9"),
    TEN(10, "T"),
    JACK(11, "J"),
    QUEEN(12, "Q"),
    KING(13, "K"),
    ACE(14, "A");

    final int value;
    final String symbol;

    Rank(int value, String symbol) {
        this.value = value;
        this.symbol = symbol;
    }
}

class HandEvaluator {
    static HandRank bestOfSeven(List<Card> cards) {
        if (cards.size() != 7) {
            throw new IllegalArgumentException("Texas Hold'em hands must evaluate exactly seven cards.");
        }

        HandRank best = null;
        for (int first = 0; first < cards.size() - 4; first++) {
            for (int second = first + 1; second < cards.size() - 3; second++) {
                for (int third = second + 1; third < cards.size() - 2; third++) {
                    for (int fourth = third + 1; fourth < cards.size() - 1; fourth++) {
                        for (int fifth = fourth + 1; fifth < cards.size(); fifth++) {
                            List<Card> combination = new ArrayList<>(5);
                            combination.add(cards.get(first));
                            combination.add(cards.get(second));
                            combination.add(cards.get(third));
                            combination.add(cards.get(fourth));
                            combination.add(cards.get(fifth));

                            HandRank candidate = evaluateFive(combination);
                            if (best == null || candidate.compareTo(best) > 0) {
                                best = candidate;
                            }
                        }
                    }
                }
            }
        }
        return best;
    }

    private static HandRank evaluateFive(List<Card> cards) {
        List<Integer> values = new ArrayList<>();
        Map<Integer, Integer> counts = new HashMap<>();
        boolean flush = true;
        Suit suit = cards.get(0).suit;
        for (Card card : cards) {
            values.add(card.rank.value);
            counts.put(card.rank.value, counts.getOrDefault(card.rank.value, 0) + 1);
            if (card.suit != suit) {
                flush = false;
            }
        }
        values.sort(Collections.reverseOrder());

        int straightHigh = straightHigh(values);
        List<Map.Entry<Integer, Integer>> grouped = new ArrayList<>(counts.entrySet());
        grouped.sort((left, right) -> {
            int countCompare = Integer.compare(right.getValue(), left.getValue());
            if (countCompare != 0) {
                return countCompare;
            }
            return Integer.compare(right.getKey(), left.getKey());
        });

        if (flush && straightHigh > 0) {
            return new HandRank(8, "Straight flush", List.of(straightHigh));
        }
        if (grouped.get(0).getValue() == 4) {
            int four = grouped.get(0).getKey();
            int kicker = grouped.get(1).getKey();
            return new HandRank(7, "Four of a kind", List.of(four, kicker));
        }
        if (grouped.get(0).getValue() == 3 && grouped.get(1).getValue() == 2) {
            return new HandRank(6, "Full house", List.of(grouped.get(0).getKey(), grouped.get(1).getKey()));
        }
        if (flush) {
            return new HandRank(5, "Flush", values);
        }
        if (straightHigh > 0) {
            return new HandRank(4, "Straight", List.of(straightHigh));
        }
        if (grouped.get(0).getValue() == 3) {
            List<Integer> tieBreakers = new ArrayList<>();
            tieBreakers.add(grouped.get(0).getKey());
            addKickers(tieBreakers, grouped, 1);
            return new HandRank(3, "Three of a kind", tieBreakers);
        }
        if (grouped.get(0).getValue() == 2 && grouped.get(1).getValue() == 2) {
            int highPair = Math.max(grouped.get(0).getKey(), grouped.get(1).getKey());
            int lowPair = Math.min(grouped.get(0).getKey(), grouped.get(1).getKey());
            int kicker = grouped.get(2).getKey();
            return new HandRank(2, "Two pair", List.of(highPair, lowPair, kicker));
        }
        if (grouped.get(0).getValue() == 2) {
            List<Integer> tieBreakers = new ArrayList<>();
            tieBreakers.add(grouped.get(0).getKey());
            addKickers(tieBreakers, grouped, 1);
            return new HandRank(1, "One pair", tieBreakers);
        }
        return new HandRank(0, "High card", values);
    }

    private static void addKickers(List<Integer> tieBreakers, List<Map.Entry<Integer, Integer>> grouped, int startIndex) {
        List<Integer> kickers = new ArrayList<>();
        for (int index = startIndex; index < grouped.size(); index++) {
            for (int repeat = 0; repeat < grouped.get(index).getValue(); repeat++) {
                kickers.add(grouped.get(index).getKey());
            }
        }
        kickers.sort(Collections.reverseOrder());
        tieBreakers.addAll(kickers);
    }

    private static int straightHigh(List<Integer> values) {
        List<Integer> unique = new ArrayList<>();
        for (int value : values) {
            if (!unique.contains(value)) {
                unique.add(value);
            }
        }
        Collections.sort(unique);
        if (unique.equals(List.of(2, 3, 4, 5, 14))) {
            return 5;
        }
        if (unique.size() != 5) {
            return 0;
        }
        for (int index = 1; index < unique.size(); index++) {
            if (unique.get(index) != unique.get(index - 1) + 1) {
                return 0;
            }
        }
        return unique.get(unique.size() - 1);
    }
}

class HandRank implements Comparable<HandRank> {
    private final int category;
    private final String label;
    private final List<Integer> tieBreakers;

    HandRank(int category, String label, List<Integer> tieBreakers) {
        this.category = category;
        this.label = label;
        this.tieBreakers = new ArrayList<>(tieBreakers);
    }

    String describe() {
        return label + " (" + tieBreakers + ")";
    }

    @Override
    public int compareTo(HandRank other) {
        if (category != other.category) {
            return Integer.compare(category, other.category);
        }
        for (int index = 0; index < Math.min(tieBreakers.size(), other.tieBreakers.size()); index++) {
            int compare = Integer.compare(tieBreakers.get(index), other.tieBreakers.get(index));
            if (compare != 0) {
                return compare;
            }
        }
        return Integer.compare(tieBreakers.size(), other.tieBreakers.size());
    }
}