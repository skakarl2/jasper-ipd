# CardinalObfuscator.py
import random
class CardinalObfuscator:
    def obfuscate_move(self, player, deck, rulebook, phase):
        # The move is a tuple of nonsense
        card_from_hand = random.choice(player.hand) if player.hand else None
        card_from_deck = random.choice(deck.cards) if deck.cards else None
        return (card_from_hand, card_from_deck, phase.current_phase, rulebook.random_rule())
