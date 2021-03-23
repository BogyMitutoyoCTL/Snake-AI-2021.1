from Algorithms.Algorithms import Algorithm
from GameData import GameData


class TW(Algorithm):
    def __init__(self):
        super().__init__()

    def decide(self, info: GameData) -> str:
        # Strategie: zum Futter laufen
        if info.head_x < info.food_x:  # Liegt Futter im Osten?
            if info.can_move_to(info.head_x + 1, info.head_y):  # Kann ich nach Osten?
                return "east"

        if info.head_x > info.food_x:  # Liegt Futter im Westen?
            if info.can_move_to(info.head_x - 1, info.head_y):  # Kann ich nach Westen?
                return "west"

        if info.head_y < info.food_y:  # Liegt Futter im Süden?
            if info.can_move_to(info.head_x, info.head_y + 1):  # Kann ich nach Süden?
                return "south"

        if info.head_y > info.food_y:  # Liegt Futter im Norden?
            if info.can_move_to(info.head_x, info.head_y - 1):  # Kann ich nach Norden?
                return "north"

        # Der direkte Weg zum Futter ist wohl versperrt
        # Strategie: so weiterlaufen wie bisher
        if info.direction == "east":  # Laufe ich nach Osten?
            if info.can_move_to(info.head_x + 1, info.head_y):  # Kann ich weiter nach Osten?
                return "east"

        if info.direction == "west":  # Laufe ich nach Westen?
            if info.can_move_to(info.head_x - 1, info.head_y):  # Kann ich weiter nach Westen?
                return "west"

        if info.direction == "south":  # Laufe ich nach Süden?
            if info.can_move_to(info.head_x, info.head_y + 1):  # Kann ich weiter nach Süden?
                return "south"

        if info.direction == "north":  # Laufe ich nach Westen?
            if info.can_move_to(info.head_x, info.head_y - 1):  # Kann ich weiter nach Norden?
                return "north"

        # Weiter wie bisher geht nicht
        # Strategie: Egal wohin, bloß nicht sterben...
        if info.can_move_to(info.head_x + 1, info.head_y):  # Kann ich nach Osten?
            return "east"
        if info.can_move_to(info.head_x - 1, info.head_y):  # Kann ich nach Westen?
            return "west"
        if info.can_move_to(info.head_x, info.head_y + 1):  # Kann ich nach Süden?
            return "south"
        if info.can_move_to(info.head_x, info.head_y - 1):  # Kann ich nach Norden?
            return "north"

        # Öhm ... alle Richtungen versperrt?
        # Dann lieber auf einer Südseeinsel sterben
        return "south"
