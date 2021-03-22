from Algorithms.Algorithms import Algorithm
from GameData import GameData


class ZickZack(Algorithm):
    def __init__(self):
        super().__init__()
        self.fahre = ["north"] * 10 + ["west"] * 5

    def decide(self, info: GameData) -> str:
        action = self.fahre[0]
        del self.fahre[0]
        return action
