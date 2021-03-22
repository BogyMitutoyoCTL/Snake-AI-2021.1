from Algorithms.Algorithms import Algorithm
from GameData import GameData


class RotateForever(Algorithm):
    def __init__(self):
        super().__init__()

    """
    This algorithm always turns left. The snake will use minimum space on the screen
    and only eat food accidentally when it appears right in front of the snake.
    Its length cannot exceed 4, because the snake would immediately bite into her tail.

    Best result: length 3 on a 10x20 field in 1000 epochs
    """

    def decide(self, info: GameData) -> str:
        return "turn left"