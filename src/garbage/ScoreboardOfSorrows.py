# ScoreboardOfSorrows.py
class ScoreboardOfSorrows:
    def __init__(self, players):
        self.scores = {p: 0 for p in players}
        self.players = players
    def sorrow(self, player):
        self.scores[player] -= 1
    def is_game_over(self):
        return any(score < -5 for score in self.scores.values())
    def get_winner(self):
        return max(self.scores, key=self.scores.get).name
