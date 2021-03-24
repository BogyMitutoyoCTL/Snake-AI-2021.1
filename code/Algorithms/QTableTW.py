from Algorithms.Algorithms import Algorithm
from GameData import GameData


class QTableTW(Algorithm):
    def __init__(self):
        super().__init__()

    def decide(self, info: GameData) -> str:
        # Schritt 1: Situationsnummer ausrechnen
        situationsnummer = self.umrechnen(info, 3, "111 101 111")
        # Schritt 2: Nummer für die Richtung ausrechnen
        # Schritt 3: Greife auf eine Tabelle von Entscheidungen zu
        #            und suchen uns die Aktion raus, die ausgeführt werden soll
        return "north"

    def umrechnen(self, spielfeld: GameData, kantenlaenge: int, maske: str) -> int:
        maske = maske.replace(" ", "")  # Leerzeichen sind nur für Menschen interessant
        self.pruefe(kantenlaenge, maske)
        ausschnitt = self.gib_mir_einen_ausschnitt(spielfeld, kantenlaenge)
        situationsnummer = self.berechne_im_binaersystem(ausschnitt, maske)
        return situationsnummer

    def berechne_im_binaersystem(self, ausschnitt, maske):
        situationsnummer = 0  # Identitäts-Element für Addition
        wertigkeit = 1  # Identitäts-Element für Multiplikation
        anzahl_ziffern = len(ausschnitt)
        for stelle in range(0, anzahl_ziffern):
            muss_beruecksichtigt_werden = maske[stelle]
            ziffer = ausschnitt[stelle]
            if muss_beruecksichtigt_werden == "1":
                situationsnummer += ziffer * wertigkeit
                wertigkeit *= 2  # Binärsystem
        return situationsnummer

    def gib_mir_einen_ausschnitt(self, info, kantenlaenge):
        xfrom = -(kantenlaenge - 1) // 2
        xto = -xfrom
        yfrom = xfrom
        yto = xto
        ausschnitt = []
        for dy in range(yfrom, yto + 1):
            for dx in range(xfrom, xto + 1):
                if info.can_move_to(info.head_x + dx, info.head_y + dy):
                    ausschnitt.append(0)
                else:
                    ausschnitt.append(1)
        return ausschnitt

    def pruefe(self, kantenlaenge, maske):
        # Prüfen, ob Dinge auch sinnvoll sind
        if kantenlaenge < 3:
            raise Exception("Die Kantenlänge muss mindestens 3 sein.")
        if kantenlaenge % 2 == 0:  # gerade Zahl
            raise Exception("Die Kantenlänge muss ungerade sein, damit der Kopf in der Mitte liegt.")
        if len(maske) != kantenlaenge ** 2:
            raise Exception("Die Maske passt nicht zur Kantenlänge")
        if len(maske.replace("1", "").replace("0", "")) > 0:
            raise Exception("Da sind Zeichen in der Maske die ich nicht kenne.")
