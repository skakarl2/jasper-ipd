package texasholdem;

import java.util.*;

/**
 * Example usage of Texas Hold'em poker game.
 * Demonstrates a simple game with AI players making random decisions.
 */
public class TexasHoldEmDemo {
    
    public static void main(String[] args) {
        // Create players
        List<Player> players = new ArrayList<>();
        players.add(new Player("Alice", 1000));
        players.add(new Player("Bob", 1000));
        players.add(new Player("Charlie", 1000));
        
        // Create game
        TexasHoldEm game = new TexasHoldEm(players, 1000, 1.0);
        
        // Play a few hands
        for (int hand = 0; hand < 3; hand++) {
            System.out.println("\n" + "=".repeat(60));
            System.out.println("STARTING HAND " + (hand + 1));
            System.out.println("=".repeat(60));
            
            game.startNewHand();
            System.out.println(game.getGameState());
            
            // Show hole cards for demo
            for (Player player : game.getPlayers()) {
                if (!player.getHoleCards().isEmpty()) {
                    System.out.println(player.getName() + " has: " + player.getHoleCards());
                }
            }
            
            // Simulate betting rounds (simplified)
            simulateBettingRound(game);
            
            // Play out the hand
            game.advancePhase(); // FLOP
            System.out.println("\nFLOP: " + game.getCommunityCards());
            
            game.advancePhase(); // TURN
            System.out.println("TURN: " + game.getCommunityCards());
            
            game.advancePhase(); // RIVER
            System.out.println("RIVER: " + game.getCommunityCards());
            
            game.advancePhase(); // SHOWDOWN
            System.out.println("\n--- SHOWDOWN ---");
            
            // Show all hands
            for (Player player : game.getPlayers()) {
                if (!player.isFolded()) {
                    PokerHand bestHand = game.getBestHand(player);
                    System.out.println(player.getName() + ": " + bestHand);
                }
            }
            
            // Determine winner
            List<Player> winners = game.determineWinners();
            double pot = game.getTotalPot();
            game.awardPot(winners);
            
            System.out.println("\nPot: $" + pot);
            for (Player winner : winners) {
                System.out.println("Winner: " + winner.getName() + " wins $" + (pot / winners.size()));
            }
            
            // Show final chip counts
            System.out.println("\n--- CHIP COUNTS ---");
            for (Player player : game.getPlayers()) {
                System.out.println(player.getName() + ": $" + player.getChips());
            }
        }
    }
    
    /**
     * Simulates a simplified betting round where players randomly fold or call.
     */
    private static void simulateBettingRound(TexasHoldEm game) {
        Random rand = new Random();
        
        for (Player player : game.getPlayers()) {
            if (!player.canActInRound()) {
                continue;
            }
            
            // 40% chance to fold, 60% chance to call/check
            if (rand.nextDouble() < 0.4) {
                player.fold();
                System.out.println(player.getName() + " folds");
            } else {
                double amountToCall = game.getPlayers().stream()
                    .mapToDouble(Player::getCurrentBet)
                    .max()
                    .orElse(0);
                
                double needsToBet = amountToCall - player.getCurrentBet();
                if (needsToBet > 0 && player.canBet(needsToBet)) {
                    player.bet(needsToBet);
                    System.out.println(player.getName() + " calls $" + needsToBet);
                } else {
                    System.out.println(player.getName() + " checks");
                }
            }
        }
    }
}
