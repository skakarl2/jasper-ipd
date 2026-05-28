# Turntable.py
class Turntable:
    def __init__(self, players):
        self.players = players
        self.index = 0
    def current_player(self):
        return self.players[self.index]
    def next(self):
        self.index = (self.index + 1) % len(self.players)
