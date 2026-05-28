# DeckOfManyFaces.py
import random
class DeckOfManyFaces:
    def __init__(self):
        self.cards = [f"Card_{i}" for i in range(1, 53)] + [f"Meta_{i}" for i in range(1, 5)]
        random.shuffle(self.cards)
    def draw(self):
        return self.cards.pop() if self.cards else None
    def shuffle(self):
        random.shuffle(self.cards)
