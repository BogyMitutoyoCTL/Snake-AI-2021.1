from Algorithms.Algorithms import Algorithm
from GameData import GameData

import glob
import json


class QTableTW(Algorithm):
    def __init__(self):
        super().__init__()
        # Schritt 0: Gedächtnis auffrischen
        dateinamen = glob.glob("./decisionrecorder/[A-D].json")
        self.gehirn = self.erzeuge_leeres_gehirn(256, 5)
        for dateiname in dateinamen:
            self.lese_eine_datei(dateiname)

    def lese_eine_datei(self, dateiname: str):
        with open(dateiname, "r") as datei:
            liste_von_entscheidungen = json.load(datei)
            for entscheidung in liste_von_entscheidungen:
                situationsnummer = entscheidung["field"]
                grobe_richtung = entscheidung["food"]
                aktion = entscheidung["decision"]
                gemerkt = self.gehirn[situationsnummer][grobe_richtung]
                if gemerkt is None:
                    self.gehirn[situationsnummer][grobe_richtung] = aktion
                else:
                    if (gemerkt == "-" or aktion == "-") and gemerkt != aktion:
                        raise Exception("Diskrepanz in Situation", situationsnummer, "und in Richtung", grobe_richtung,": ", gemerkt, " versus", aktion)


    def decide(self, info: GameData) -> str:
        # Schritt 1: Situationsnummer ausrechnen
        situationsnummer = self.umrechnen(info, 3, "111 101 111")
        # Schritt 2: Nummer für die Richtung ausrechnen
        # TODO: grobe Richtung bestimmen
        # Schritt 3: Greife auf eine Tabelle von Entscheidungen zu
        #            und suchen uns die Aktion raus, die ausgeführt werden soll
        # TODO: Entscheidung raussuchen
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

    def grobe_richtung(self, winkel: int) -> int:
        pass

    def daten_einlesen(self) -> list:
        pass

    def erzeuge_leeres_gehirn(self, aktionsanzahl, richtungsanzahl):
        gehirn = []
        for a in range(aktionsanzahl):
            liste = []
            for r in range(richtungsanzahl):
                liste.append(None)
            gehirn.append(liste)
        return gehirn
