from Algorithms.Algorithms import Algorithm
from GameData import GameData
from RewardSystem import RewardSystem

import pickle
import os

class MachineLearningTW(Algorithm):
    def __init__(self):
        super().__init__()
        # Schritt 0: Gedächtnis auffrischen
        self.kantenlaenge = 5
        self.maske = "01110 11111 11011 11111 01110"
        self.maske = self.maske.replace(" ", "")  # Leerzeichen sind nur für Menschen interessant
        self.anzahl_richtungen = 5
        
        self.dateiname = "gehirn.data"
        self.gehirn = self.lade_gehirn_oder_lege_neu_an()
        self.lernvorgange = 0

        self.reward_system = RewardSystem()
        # Belohnungen
        self.reward_system.reward_eat_food = 1
        self.reward_system.reward_win = 1
        self.reward_system.reward_closer_function = lambda closer: 1 if closer > 0 else -1
        # Bestrafungen
        self.reward_system.reward_killed_by_wall = -1
        self.reward_system.reward_killed_by_tail = -1
        self.reward_system.reward_impossible_move = -1
        self.reward_system.reward_killed_by_starving_function = lambda step, length: 0
        
        self.trainierte_epochen = 0

    def lade_gehirn_oder_lege_neu_an(self):
        if os.path.isfile(self.dateiname):
            return self.lade_gehirn_aus_datei()
        else:
            speicherplatzanzahl = 2 ** (self.maske.count("1"))
            return self.erzeuge_leeres_gehirn(speicherplatzanzahl, self.anzahl_richtungen)

    def epochfinished(self) -> (object, float):
        print("Lernvorgänge:", self.lernvorgange)
        self.lernvorgange = 0

        self.trainierte_epochen += 1
        if self.trainierte_epochen % 100 == 0:
            self.speichere_gehirn()
        
        return None, 0.0

    def train(self, spielfeld: GameData, aktion: str, reward: float) -> None:
        situationsnummer = self.umrechnen(spielfeld)
        grobe_richtung = self.grobe_richtung(spielfeld.food_direction)
        wuerfel = self.gehirn
        scheibe = wuerfel[situationsnummer]
        saeule = scheibe[grobe_richtung]

        nachschlagewerk = {"north": 0, "east": 1, "south": 2, "west": 3}
        nummer_der_aktion = nachschlagewerk[aktion]

        self.lernvorgange += 1
        if reward < 0:
            # letzte Aktion abwerten
            saeule[nummer_der_aktion] /= 1.1  # TODO: willkürlich gewählte Zahl
        elif reward > 0:
            # letzte Aktion belohnen
            saeule[nummer_der_aktion] *= 1.1  # TODO: willkürlich gewählte Zahl
        else:
            # neutral - nix tun
            pass

    def decide(self, spielfeld: GameData) -> str:
        # Schritt 1: Situationsnummer ausrechnen
        situationsnummer = self.umrechnen(spielfeld)
        # Schritt 2: Nummer für die Richtung ausrechnen
        grobe_richtung = self.grobe_richtung(spielfeld.food_direction)
        # Schritt 3: Greife auf eine Tabelle von Entscheidungen (Gehirn) zu
        #            und suchen uns die Aktion raus, die ausgeführt werden soll
        aktion = self.entscheide(situationsnummer, grobe_richtung)
        return aktion

    def umrechnen(self, spielfeld: GameData) -> int:
        self.pruefe(self.kantenlaenge, self.maske)
        ausschnitt = self.gib_mir_einen_ausschnitt(spielfeld, self.kantenlaenge)
        situationsnummer = self.berechne_im_binaersystem(ausschnitt, self.maske)
        return situationsnummer

    def berechne_im_binaersystem(self, ausschnitt, maske):
        situationsnummer = 0  # Identitäts-Element für Addition
        wertigkeit = 1  # Identitäts-Element für Multiplikation
        anzahl_ziffern = len(ausschnitt)
        for stelle in range(0, anzahl_ziffern):
            muss_beruecksichtigt_werden = maske[stelle]
            if muss_beruecksichtigt_werden == "1":
                ziffer = ausschnitt[stelle]
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

    def grobe_richtung(self, alpha: int) -> int:
        # Die negativen Winkel stören
        if alpha < 0:
            alpha = alpha + 360

        # Wie breit ist eine grobe Einheit?
        beta = 360 / self.anzahl_richtungen
        richtung = int(alpha / beta)
        return richtung

    def erzeuge_leeres_gehirn(self, situationsanzahl, richtungsanzahl):
        wuerfel = []
        aktionsanzahl = 4
        for _ in range(situationsanzahl):  # x-achse
            scheibe = []
            for _ in range(richtungsanzahl):  # y-achse
                richtungs_saeule = []
                for _ in range(aktionsanzahl):  # z-achse
                    richtungs_saeule.append(0.5)  # TODO: das könnte auch zufällig sein
                scheibe.append(richtungs_saeule)
            wuerfel.append(scheibe)
        return wuerfel

    def entscheide(self, situationsnummer: int, grobe_richtung: int) -> str:
        wuerfel = self.gehirn
        scheibe = wuerfel[situationsnummer]
        saeule = scheibe[grobe_richtung]
        # Problem: wir bekommen Wahrscheinlichkeit / Zuversichtlichkeit
        groesster_wert = max(saeule)
        if saeule[0] == groesster_wert:
            aktion = "north"
        elif saeule[1] == groesster_wert:
            aktion = "east"
        elif saeule[2] == groesster_wert:
            aktion = "south"
        elif saeule[3] == groesster_wert:
            aktion = "west"
        else:
            raise Exception("Wie kann es sein, dass es keinen größten Wert gibt?")

        return aktion

    def lade_gehirn_aus_datei(self):
        with open(self.dateiname, "rb") as datei:
            daten = pickle.load(datei)
        return daten

    def speichere_gehirn(self):
        with open(self.dateiname, "wb") as datei:
            pickle.dump(self.gehirn, datei)
