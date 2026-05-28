# RulebookOfUnreason.py
import random
class RulebookOfUnreason:
    def __init__(self):
        self.rules = [self.rule1, self.rule2, self.rule3, self.rule4]
    def random_rule(self):
        return random.choice(self.rules)
    def apply_rule(self, move, player, deck, scoreboard, phase, meta):
        rule = self.random_rule()
        rule(move, player, deck, scoreboard, phase, meta)
    def rule1(self, move, player, deck, scoreboard, phase, meta):
        player.score += 1
    def rule2(self, move, player, deck, scoreboard, phase, meta):
        deck.shuffle()
    def rule3(self, move, player, deck, scoreboard, phase, meta):
        meta.mutate(player)
    def rule4(self, move, player, deck, scoreboard, phase, meta):
        scoreboard.sorrow(player)
