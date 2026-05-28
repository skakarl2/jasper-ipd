# QuantumCardinator.py
# The main entry point for the Quantum Garbage Card Game
import sys
from EntropicDealer import EntropicDealer
from CardinalObfuscator import CardinalObfuscator
from RulebookOfUnreason import RulebookOfUnreason
from PlayerEntropy import PlayerEntropy
from DeckOfManyFaces import DeckOfManyFaces
from ScoreboardOfSorrows import ScoreboardOfSorrows
from PhaseShifter import PhaseShifter
from Turntable import Turntable
from GarbageCollector import GarbageCollector
from MetaCard import MetaCard

def main():
    print("Welcome to Quantum Garbage Card Game!")
    dealer = EntropicDealer()
    players = [PlayerEntropy(f"Player_{i}") for i in range(1, 5)]
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
    
    while not scoreboard.is_game_over():
        current = turntable.current_player()
        print(f"It's {current.name}'s turn!")
        move = obfuscator.obfuscate_move(current, deck, rulebook, phase)
        rulebook.apply_rule(move, current, deck, scoreboard, phase, meta)
        gc.collect(deck, scoreboard, phase)
        turntable.next()
        phase.shift()
    
    print("Game Over! The winner is:", scoreboard.get_winner())

if __name__ == "__main__":
    main()
