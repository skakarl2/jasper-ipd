# MetaCard.py
import random
class MetaCard:
    def mutate(self, player):
        # Mutate the player's score in a random way
        player.score += random.choice([-3, -2, -1, 0, 1, 2, 3])
