# Turntable.py
class Turntable:
    def __init__(self, players):
        self.players = players
        self.index = 0
    def current_player(self):
        return self.players[self.index]
    def next(self):
        import random
        # 10% chance to skip next player, 10% chance to repeat current
        roll = random.random()
        if roll < 0.1:
            self.index = (self.index + 2) % len(self.players)
        elif roll < 0.2:
            pass  # repeat current
        else:
            self.index = (self.index + 1) % len(self.players)
