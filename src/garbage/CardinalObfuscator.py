# CardinalObfuscator.py
import random
class CardinalObfuscator:
    def obfuscate_move(self, player, deck, rulebook, phase):
        # The move is a tuple of nonsense
        return (random.choice(player.hand), random.choice(deck.cards), phase.current_phase, rulebook.random_rule())
