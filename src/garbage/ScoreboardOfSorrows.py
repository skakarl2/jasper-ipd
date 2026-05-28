# ScoreboardOfSorrows.py
import random
class ScoreboardOfSorrows:
    import random
    def __init__(self, players):
        self.scores = {p: 0 for p in players}
        self.players = players
        self.sorrow_threshold = -random.randint(3, 10)
    def sorrow(self, player):
        self.scores[player] -= 1
        # Reverse Entropy: 5% chance to reset all scores
        import random
        if random.random() < 0.05:
            for p in self.players:
                self.scores[p] = 0
    def is_game_over(self):
        import random
        # 2% chance to end game instantly
        if random.random() < 0.02:
            return True
        return any(score < self.sorrow_threshold for score in self.scores.values())
    def get_winner(self):
        return max(self.scores, key=self.scores.get).name
