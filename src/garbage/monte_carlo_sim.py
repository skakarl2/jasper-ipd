# monte_carlo_sim.py
import sys
import os
import statistics
sys.path.append(os.path.dirname(__file__))
from QuantumCardinator import PlayerEntropy, DeckOfManyFaces, ScoreboardOfSorrows, Turntable, RulebookOfUnreason, PhaseShifter, CardinalObfuscator, GarbageCollector, MetaCard

NUM_GAMES = 100000
num_players = 4
final_scores = []
winners = []
turn_counts = []

for _ in range(NUM_GAMES):
    players = [PlayerEntropy(f"Player_{i}") for i in range(1, num_players+1)]
    deck = DeckOfManyFaces()
    scoreboard = ScoreboardOfSorrows(players)
    turntable = Turntable(players)
    rulebook = RulebookOfUnreason()
    phase = PhaseShifter()
    obfuscator = CardinalObfuscator()
    gc = GarbageCollector()
    meta = MetaCard()
    for _ in range(7):
        for p in players:
            p.hand.append(deck.draw())
    turns = 0
    while not scoreboard.is_game_over():
        current = turntable.current_player()
        move = obfuscator.obfuscate_move(current, deck, rulebook, phase)
        rulebook.apply_rule(move, current, deck, scoreboard, phase, meta)
        gc.collect(deck, scoreboard, phase)
        turntable.next()
        phase.shift()
        turns += 1
        # Prevent infinite loops
        if turns > 500:
            break
    turn_counts.append(turns)
    scores = [p.score for p in players]
    final_scores.append(scores)
    winners.append(scoreboard.get_winner())

# Aggregate stats
avg_turns = statistics.mean(turn_counts)
min_turns = min(turn_counts)
max_turns = max(turn_counts)
score_means = [statistics.mean([fs[i] for fs in final_scores]) for i in range(num_players)]
score_stds = [statistics.stdev([fs[i] for fs in final_scores]) for i in range(num_players)]
winner_counts = {f"Player_{i+1}": winners.count(f"Player_{i+1}") for i in range(num_players)}

print(f"Quantum Garbage Card Game Monte Carlo Simulation ({NUM_GAMES} games)")
print(f"Average turns per game: {avg_turns:.2f} (min: {min_turns}, max: {max_turns})")
for i in range(num_players):
    print(f"Player_{i+1} avg score: {score_means[i]:.2f} (std: {score_stds[i]:.2f})")
print("Win counts:", winner_counts)
