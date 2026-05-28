# EntropicDealer.py
import random
class EntropicDealer:
    def __init__(self):
        self.entropy = random.random()
    def deal(self, deck, players):
        for _ in range(int(self.entropy * 10) + 1):
            for p in players:
                if deck.cards:
                    p.hand.append(deck.cards.pop(random.randint(0, len(deck.cards)-1)))
