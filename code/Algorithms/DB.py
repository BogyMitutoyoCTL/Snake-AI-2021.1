from Algorithms.Algorithms import Algorithm
from GameData import GameData


class DB(Algorithm):
    def __init__(self):
        super().__init__()

    def decide(self, info: GameData) -> str:
        zahl = self.umrechnen(info, 3, "111 101 111")
        print("Head x:" + str(info.head_x) + " y:" + str(info.head_y) + " Zahl:" + str(zahl))
        return "north"

    def umrechnen(self, info, kantenlaenge, maske):
        start_x = info.head_x - kantenlaenge // 2
        start_y = info.head_y - kantenlaenge // 2
        act_x = 0
        act_y = 0
        wertigkeit = 0
        ergebnis = 0
        for character in maske:
            if character == "1" or character == "0":
                if character == "1":
                    if not info.can_move_to(start_x + act_x, start_y + act_y):
                        tmp = pow(2, wertigkeit)
                        ergebnis += tmp
                    else:
                        pass
                    wertigkeit += 1
                act_x += 1
                if act_x >= kantenlaenge:
                    act_x = 0
                    act_y += 1
        return ergebnis
