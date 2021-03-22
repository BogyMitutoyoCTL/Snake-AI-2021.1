from Algorithms.Algorithms import Algorithm
from GameData import GameData


class TryTwoJR(Algorithm):
    def __init__(self):
        super().__init__()
        self.fahre = ["north"] * 10 + ["west"] * 5 + ((["south"] + ["east"] * 8 + ["south"] + ["west"] * 8) * 9 + ["south"] + ["east"] * 9 + ["north"] * 19 + ["west"] * 9) * 1000

    def decide(self, info: GameData) -> str:
        action = self.fahre[0]
        del self.fahre[0]
        return action
