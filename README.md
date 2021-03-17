# Snake AI 2021.1
Dieses Projekt dokumentiert die Entwicklung eines Machine Learning Algorithmus im Rahmen einer Berufsorientierung für Gymnasien (BOGY) für das [Leibnitz-Gymnasium in Rottweil](https://lg.rw.schule-bw.de/home/?page_id=11268) im Schuljahr 2020/2021. Als Firmenpartner stand [Mitutoyo CTL in Oberndorf](http://www.mitutoyo-ctl.de/de/karriere/ausbildungundstudium) mit Hardware und Ansprechpartnern zur Verfügung.

Es handelt sich um eine erweiterte Berufsorientierung, d.h. zusätzlich zur üblichen BOGY-Woche stehen noch sechs Nachmittage zur Verfügung, um die Schüler auf das Praktikum vorzubereiten. Aufgrund von CODIV-19 finden diese Nachmittage online statt. Wir danken [Discord](https://discord.com/) für die Nutzungserlaubnis.

## Inspiration

Inspiration für dieses Projekt war das [Leibniz Forschungszentrum](https://lg.rw.schule-bw.de/home/?cat=120) mit einer Idee, die Bewegung von Ameisen vom Computer vorherzusagen. Die Original-Idee beinhaltete ein Terrarium mit echten Ameisen, Kamera usw. Eine solch reale Umgebung birgt jedoch Schwierigkeiten, die mit den Rahmenbedingungen eines Praktikums schlecht vereinbar sind, z.B.:

* wer kümmert sich um die Ameisen? Möglicherweise sterben sie ausgerechnet alle am ersten Tag der Praktikumswoche.
* wie nehmen die Teilnehmer das Ergebnis samt Ameisen mit nach Hause, um es Eltern und Freunden zu zeigen?
* sind die Ergebnisse reproduzierbar? Wir können bei einer fehlerhaften Umsetzung nicht nochmal am gleichen Startpunkt beginnen.
* passt das Projekt in den Zeitrahmen?

Aus diesem Grund haben wir uns entschlossen, zwar ein Machine Learning Projekt durchzuführen, aber die Bedingungen zu unseren Gunsten anzupassen. Entstanden ist ein Snake-Spiel, bei dem der Computer selbst die Spielregeln erlernen soll und dann die richtigen Aktionen durchführt.

# Projekt-Umgebung

## Software

Wir verwenden kostenlose Software: 

* das Betriebssystem [Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspbian/) für den Raspberry Pi 4.  Wir verwenden die Version mit 4 GB Speicher, da wir für ein Experiment viel RAM benötigen.
* [Kitty](http://www.9bis.net/kitty/#!index.md) für den Zugriff auf den Raspberry per SSH
* [Bash](https://www.gnu.org/software/bash/) als Kommandozeile
* [xRDP](http://xrdp.org/) für den Zugriff auf die Benutzeroberfläche des Raspberry
* die Programmiersprache [Python](https://www.python.org/)
* die Entwicklungsumgebung [PyCharm von JetBrains](https://www.jetbrains.com/de-de/pycharm/) (Community Edition)
* die Bibliothek [OpenAI Gym](https://gym.openai.com/)
* die Versionsverwaltung [Git](https://git-scm.com/) mit dem Provider [Github](https://github.com/)
* ggf. unter Windows den [Editor Notepad++](https://notepad-plus-plus.org/) und das Difftool [Winmerge](https://winmerge.org/?lang=de)

## Daten

Im Rahmen des Projekts erzeugen sich die Daten aus dem Spielverlauf selbst.

# Vorbereitung / Einführung

An den sechs vorbereitenden Nachmittagen können Grundlagen vermittelt werden. Dadurch läuft die Praktikumswoche einfach flüssiger und die Schüler erreichen auch echte Ergebnisse.

## Erster Nachmittag, 3.2.2021

Am ersten Nachmittag haben wir uns vorgestellt. Normalerweise führen wir am ersten Tag durch unser Gebäude, um die Räumlichkeiten kennenzulernen. Dies werden wir nachholen, falls wir uns zur Praktikumswoche vor Ort sein können.

Die [Firmenpräsentation](presentation/Firmenpräsentation.pptx) erklärt unser Firmen-Motto, nennt die von uns entwickelte Software, erklärt das duale Studium und zeigt Beispiele von Praktikumsprojekten.

Wir arbeiten mit der [DHBW Stuttgart](https://www.dhbw-stuttgart.de/) zusammen und stellen den Studenten eine [Studentenwohnung](presentation/Studentenwohnung.pptx) zur Verfügung, um die Fahrtzeiten während den Theoriephasen zu verkürzen, so dass sie sich auf das Studium vorbereiten können.

Dann haben wir uns mit dem Thema der Berufsorientierung  auseinandergesetzt. Das Spielprinzip ist vermutlich hinreichend bekannt: es handelt sich um ein Snake-Spiel. Die Schlange (grün) frisst mit  ihrem Kopf (blau) einen Apfel (rot) und wächst dabei.

Zum Glück sind wir hier nicht an fächerübergreifenden Unterricht gebunden, ansonsten  müsste man sich fragen, seit wann Schlangen vegetarisch sind (Biologie), ob nicht Adam und Eva den Apfel gegessen haben, anstatt der Schlange  (Religion) und ob Schlangen mit künstlicher Intelligenz ein Bewusstsein  haben, und somit überhaupt in Tierversuchen einsetzbar sind (Ethik).

Die von uns bereitgestellte Spieleumgebung ist bereits auf  KI-Experimente vorbereitet, d.h. ein beliebiger Algorithmus kann in der  Umgebung mehrere Spiele nacheinander ohne menschliches Zutun spielen.  Zur Spieleumgebung gibt es eine Visualisierung, die folgendermaßen  aufgebaut ist:

- der linke Bereich liefert statistische Daten
  - grün: Daten zur Visualisierung, derzeit nur die aktuelle  Visualisierungsgeschwindigkeit in Bildern pro Sekunde (fps; frames per  second)
  - hellblau: Daten zum Training, d.h. mehrere Spiele übergreifend
  - violett: Daten zum aktuell laufenden Spiel. Ein Teil dieser Daten könnte als Input für Neuronen dienen.
- der rechte Bereich visualisiert das Spielfeld
  - rot: das Futter (angeblich ein Apfel)
  - blau: der Kopf der Schlange
  - grün: Körper der Schlange, wobei die hellere Teile früher verschwinden als dunklere Teile

Im Bild sieht man einen von Mitutoyo programmierten Algorithmus, der  noch keine künstliche Intelligenz nutzt. Dabei handelt es sich bewusst  um einen Algorithmus, der nicht mathematisch als perfekt bewiesen ist.  Unsere KI wird sich mit diesem Algorithmus messen müssen. Bei 1000  Spielen erreicht er eine Länge von bis zu 80 Kästchen, was einer  Abdeckung von 40% der Fläche entspricht.

![Snake Beispiel](presentation/Snake.png)

Die Hardware, ein [Raspberry Pi 4](presentation/Raspberry%20Hardware.pptx), haben wir uns zunächst nur auf Bildern angeschaut. Die echte Hardware ist bereits verschickt, wird aber erst im Laufe der Woche eintreffen. Dank der Speichererweiterung auf 4 GB können auch größere Datenmengen verarbeitet werden, wie sie bei Machine Learning auftreten.

Um auf den Raspberry zugreifen zu können, wenn er zugestellt wurde, haben wir SSH grob erklärt und [Kitty](http://www.9bis.net/kitty/#!pages/download.md) installiert.

Um für eine spätere Zusammenarbeit vorbereitet zu sein, haben wir Accounts bei [Github](https://github.com/) angelegt und Zugriff auf dieses Repository gewährt.

## Zweiter Nachmittag, 10.2.2021

### Raspberry Pis anschließen und finden

Ein Raspberry Pi kam bereits im Laufe der letzten Woche an. Nach dem Anschluss im LAN gab es zunächst Schwierigkeiten, diesen aufzufinden. Selbst der [Advanced IP Scanner](https://www.advanced-ip-scanner.com/de/) half nicht. 

Beim Einsatz solcher Tools ist eine Aufklärung über [§202c StGB](https://www.gesetze-im-internet.de/stgb/__202c.html) angebracht, auch bekannt als "Hackerparagraph". Für private Zwecke im eigenen Netzwerk sind solche Tools zulässig. In fremden Netzwerken, z.B. dem Schulnetz, könnte die Ausführung als Vorbereitung des Ausspähens von Daten gewertet werden und damit strafbar sein. 

Wo wir gerade beim Thema Recht sind: "Unwissenheit schützt vor Strafe nicht" sagt man. Das ergibt sich aus [§17 StGB](https://www.gesetze-im-internet.de/stgb/__17.html). Dort heißt es "*[...] handelt er ohne Schuld, wenn er diesen Irrtum nicht vermeiden konnte*". Allerdings lassen sich durch das Lesen von Gesetzen Irrtümer vermeiden, so dass man wahrscheinlich schlechte Karten hat.

Letztlich konnte der Raspberry Pi dann doch noch gefunden werden. Grund war, dass der Raspberry lediglich eine IPv6 Adresse und keine IPv4 Adresse bekommen hatte. Damit haben wir nicht gerechnet, sonst hätten wir den Raspberry so konfiguriert, dass er nur IPv4 Adressen akzeptiert.

Allerdings war der Raspberry Pi über seinen Namen ansprechbar, so dass die Suche nach der IPv6-Adresse gar nicht erforderlich war. Wir haben Euch den Raspberry mit seinem Standard-Namen `raspberry` zugeschickt. Unter "Host Name (or IP address)" trägt man daher `raspberry` ein.

![Kitty Zugriff über den Namen](presentation/kitty_find_by_name.png)

Die Nutzung von Kitty ist [in manchen Ländern](http://www.cryptolaw.org/cls-sum.htm) übrigens auch reglementiert, da es Verschlüsselung beinhaltet. In Deutschland ist es jedoch unproblematisch.

Sobald die Verbindung vom Computer mittels Kitty zum Raspberry hergestellt ist, haben wir einen wichtigen Schritt erreicht: wir haben jetzt Zugriff auf einen Linux-Computer mit Hilfe der Bash. Beides erklären wir am heutigen Nachmittag.

### Linux

Linux ist ein Betriebssystem für Computer, also eine Alternative für Windows. Die [Linux-Präsentation](presentation/Linux.pptx) geht auf einige Unterschiede ein. Die Folien sind eher theoretischer Natur, weswegen wir viele Folien ausgeblendet haben. Wer mehr Interesse am Dateisystem hat, kann sich gern die versteckten Folien ansehen.

Wer sich langfristig mit dem Thema Software-Entwicklung auseinandersetzen möchte, kommt unserer Meinung nach nicht um Linux herum.

### Bash

Die Bash ist eine Kommandozeile von Linux. Sie ähnelt der Eingabeaufforderung von Windows, ist jedoch wesentlich mächtiger. Die [Bash-Präsentation](presentation/Bash.pptx) ist weniger theoretisch und enthält viele praktische Übungen.

## Dritter Nachmittag, 24.2.2021

### Remote Desktop

Nachdem wir am letzten Nachmittag eine Verbindung per SSH zur Bash aufgebaut hatten, haben wir heute eine Verbindung zur grafischen Oberfläche mittels Remote Desktop verwendet. 

![Remote desktop](presentation/rdp.png)

Dies hat leider nicht auf Anhieb bei allen Systemen geklappt, so dass wir Fehlersuche betreiben mussten. Ursache war in diesem Fall, dass der Raspberry per LAN und der PC per WLAN angebunden waren, diese beiden Netze jedoch vom Router aus Sicherheitsgründen separiert wurden, so dass ein gegenseitiger Zugriff nicht möglich war.

Ein Zugriff per Remote Desktop ist bei Raspberry Pi OS nicht automatisch möglich. Damit es klappt, musste vorher auf der Shell der entsprechende Dienst installiert werden mit `sudo apt install xrpd`. Dies bestätigt wieder einmal, wie wichtig die Shell (in unserem Fall die Bash) bei Linux ist.

### PyCharm

Pycharm hatten wir bereits für Euch heruntergeladen und abgelegt. Wir haben dann gemeinsam PyCharm installiert und uns [einen ersten Überblick](presentation/Pycharm.pptx) verschafft.

Danach haben wir es auch [für Windows heruntergeladen](https://www.jetbrains.com/de-de/pycharm/download/#section=windows) und ebenfalls installiert, so dass ihr es auch mal ohne Raspberry benutzen könnt.

### Python

Wir haben dann eine [Einführung in Python](presentation/Python%20Einführung.pptx) durchgearbeitet, die viele Möglichkeiten für eigenes Ausprobieren bot. Wir sind bis Folie 31 gekommen und machen da nächste Woche weiter.

### Hausaufgaben

Bei Interesse könnt ihr ein paar Aufgaben von [Project Euler](https://projecteuler.net/archives) lösen.

## Vierter Nachmittag, 3.3.2021

Wir haben die [Einführung in Python](presentation/Python%20Einführung.pptx) durchgearbeitet.

## Fünfter Nachmittag, 10.3.2021

Wir haben uns das Programmierparadigma [Objektorientierung](presentation/Python%20Objektorientierung.pptx) angeschaut, inklusive Übungen zur Umsetzung in Python.

## Sechster Nachmittag, 17.3.2021

Bei umfangreichen Softwareprojekten ist es nicht mehr möglich, allein an einem Programm zu arbeiten, da es sonst nicht oder nicht schnell genug fertig wird. Daher arbeiten mehrere Programmierer in einem Team zusammen. Dann wiederum muss jeder Programmierer Zugriff auf den Code seiner Teammitglieder haben. Dieses Aufgabe (und noch ein paar mehr) löst ein Versionskontrollsystem.

Wir haben den Nutzen von [Versionskontrolle allgemein](presentation/Versionskontrolle.pptx) allgemein erklärt. Danach sind wir die [Grundlagen von Git](presentation/Git%20Grundlagen.pptx) erklärt, einem von mehreren kostenlosen Versionsverwaltungssystemen.