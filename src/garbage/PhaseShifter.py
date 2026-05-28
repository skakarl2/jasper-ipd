# PhaseShifter.py
import random
class PhaseShifter:
    def __init__(self):
        self.current_phase = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
    def shift(self):
        self.current_phase = random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])
