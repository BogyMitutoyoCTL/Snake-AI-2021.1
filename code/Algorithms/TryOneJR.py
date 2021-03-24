from Algorithms.Algorithms import Algorithm
from GameData import GameData


class TryOneJR(Algorithm):
    def __init__(self):
        super().__init__()

    def decide(self, info: GameData) -> str:
        if info.head_x < info.food_x:
            if info.can_move_to(info.head_x + 1,info.head_y):
                return "east"
        if info.head_x > info.food_x:
            if info.can_move_to(info.head_x - 1, info.head_y):
                return "west"
        if info.head_y < info.food_y:
            if info.can_move_to(info.head_x, info.head_y + 1):
                return "south"
        if info.head_y > info.food_y:
            if info.can_move_to(info.head_x, info.head_y - 1):
                return "north"

        return "north"
