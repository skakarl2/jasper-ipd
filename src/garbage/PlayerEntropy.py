# PlayerEntropy.py
class PlayerEntropy:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
    def __str__(self):
        return f"{self.name} (Score: {self.score})"
