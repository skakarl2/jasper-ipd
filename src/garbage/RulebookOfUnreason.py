# RulebookOfUnreason.py
import random
class RulebookOfUnreason:
    def __init__(self):
        self.rules = [self.rule1, self.rule2, self.rule3, self.rule4, self.rule5, self.rule6, self.rule7, self.rule8]
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
    def rule5(self, move, player, deck, scoreboard, phase, meta):
        # Swap hands with a random player
        import random
        others = [p for p in scoreboard.players if p != player]
        if others:
            target = random.choice(others)
            player.hand, target.hand = target.hand, player.hand
    def rule6(self, move, player, deck, scoreboard, phase, meta):
        # Force discard half hand
        import random
        if player.hand:
            for _ in range(len(player.hand)//2):
                player.hand.pop(random.randint(0, len(player.hand)-1))
    def rule7(self, move, player, deck, scoreboard, phase, meta):
        # Negative scoring event
        player.score -= 2
    def rule8(self, move, player, deck, scoreboard, phase, meta):
        # Schrödinger card: random card in hand mutates
        import random
        if player.hand:
            idx = random.randint(0, len(player.hand)-1)
            player.hand[idx] = f"Schrodinger_{random.randint(1,9999)}"
