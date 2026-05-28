# GarbageCollector.py
import random
class GarbageCollector:
    def collect(self, deck, scoreboard, phase):
        # Randomly remove cards and adjust scores
        if random.random() > 0.5 and deck.cards:
            deck.cards.pop()
        for player in scoreboard.players:
            if random.random() > 0.7:
                scoreboard.sorrow(player)
