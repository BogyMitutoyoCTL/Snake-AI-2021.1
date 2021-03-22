from Algorithms.Algorithms import Algorithm
from GameData import GameData


class ZickZack(Algorithm):
    def __init__(self):
        super().__init__()
        self.fahre = ["north"] * 10 + ["west"] * 5 + 9 * (["south"] + ["east"] * 8 + ["south"] + ["west"] * 8) + ["south"] + 9 * ["east"] + 19 * ["north"] + 9 * ["west"]

    def decide(self, info: GameData) -> str:
        if len(self.fahre) > 0:
            action = self.fahre[0]
        del self.fahre[0]
        if len(self.fahre) == 0:
            self.fahre = ["south"] + 9 * (["east"] * 8 + ["south"] + ["west"] * 8 + ["south"]) + 9 * ["east"] + 19 * ["north"] + 9 * [
                             "west"]

        return action



