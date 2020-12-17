import discord
import json
import datetime
import random
import math
import sys

#JSON öffnen

with open('config.json') as config_file:
    einstellungen = json.load(config_file)
    
def zeit():
    #Diese Funktion gibt einfach nur die Zeit als string zurück.
    return str(datetime.datetime.now())

def finde(name):
    #In dieser Funktion soll nach einem Spiel gesucht werden, damit der Bot
    #einen Befehl dem richtigen laufendem spiel zuordnen kann.
    #name bezeichnet dabei den Namen des SPielers, angegeben durch message.sender
    index = 0 # die Indexinteger, die nur für das return benutzt wird, wird initialisiert
    for i in laufende_spiele:
        #Als Methode werden hier einfach nur die .spieler-Felder jedes Objekts in laufende_spiele
        #mit dem angegebenen Namen verglichen
        if i.spieler == name:
            #Einfach die Indexnummer
            return index
        else:
            index += 1 #index wird angehoben und nächster listenplatz durchsucht
    #Dieser teil wird nur erreicht, wenn in der for-schleife nichts gefunden wurde
    #Daher also dieser String
    return "nichtvorhanden" 

def distanz(index, x, y):
    #In dieser Funktion soll der auszugebende Abstand zwischen einem Spielzug
    #(Variablen x und y) und den Daten eines Spiels (mit dem Index "index")
    if index == "nichtvorhanden":
        print("[ERROR] Ein Move für ein nicht existentes Spiel wurde an distanz() gereicht. Zeit: " + zeit())
    xdiff = int(x) - laufende_spiele[index].x
    ydiff = int(y) - laufende_spiele[index].y
    #Satz des Pythagoras
    diff = math.sqrt((xdiff * xdiff) + (ydiff * ydiff))
    #diff ist jetzt die genaue distanz zwischen geratenem Punkt des spielers und dem Zielpunkt
    #Jetzt soll das ergebnis etwas verzerrt werden
    verzerrer = (random.random() * (laufende_spiele[index].verzerrung * 2)) - laufende_spiele[index].verzerrung
    #Zurückgegeben wird ein integer, der bis zu dem Verzerrungslevel des Spiels vom tatsächlichen gerundeten wert entfernt ist.
    return round(diff + verzerrer)

def gewonnen(index, x, y):
    #Diese Funktion schaut, ob der SPieler mit seinem move (x, y) das Spiel (index) gewonnen hat.
    #Für weitere verarbeitung wird ein boolean ausgegeben, aber die Funktion schreibt auch selbst
    #schon in den Log.
    if index == "nichtvorhanden":
        print("[ERROR] Ein Move für ein nicht existentes Spiel wurde an gewonnen() gereicht. Zeit: " + zeit())
    if (int(x) - laufende_spiele[index].x == 0) and (int(y) - laufende_spiele[index].y == 0):
        print("[WIN]   Das Spiel mit Index " + str(index) + " wurde gewonnen um " + zeit() + ".")
        return True
    else:
        return False
    
#Dier String wird als Antwort auf den "help"-Befehl ausgegeben.
hilfetext = "Wie benutzt man diesen Bot? \n \nDas Spiel funktioniert wie folgt: ein Zielpunkt in einem zweidimensionalen Koordinatensystem wird zufällig bestimmt. Jetzt kann der Spieler Punkte angeben, deren Entfernung zum Ziel angegeben wird \(+/- eine Einheit\). Das Spiel ist gewonnen, wenn der Spieler genau auf den Punkt setzt. \n \n Befehle \(immer mit dem Präfix \"" + einstellungen["prefix"] + "\"\): \n \n\"start\": beginnt ein neues Spiel. Die Feldgröße ist 20 mal 20. \n\"quit\": beendet ein gerade laufendes Spiel.\n\"move\": einen Punkt angeben. Syntax: " + einstellungen["prefix"] + "move \[xKoordinate\] \[yKoordinate\].\n\"check\": anzeigen lassen, ob du ein Spiel am laufen hast.\n\"help\": diesen Text anzeigen lassen.\n\nViel Spaß!"


class Spiel:
    def __init__(self, spieler, spielerid, xmax, ymax, verzerrung):
        #Hier wird jedes neue erschaffene Spiel initialisiert
        self.spieler = spieler
        self.spielerid = spielerid
        self.xmax = xmax
        self.ymax = ymax
        #Hier wird das Ziel des Spiels festgelegt
        self.x = random.randint(0, xmax)
        self.y = random.randint(0, ymax)
        self.versuche = 0
        self.verzerrung = verzerrung
        
#Initiierung des Arrays, welches die Spiele halten soll
laufende_spiele = []

class MyClient(discord.Client):
    async def on_ready(self):
        #Wird ausgeführt, wenn der Bot verbunden ist.
        print("[INIT]  Verbunden, mit dem Namen " + str(self.user))
        print("[INIT]  Verbunden ab " + zeit())
        #Bot-Status auf Online setzen
        await client.change_presence(status = discord.Status.online)
        print("[INIT]  Status gesetzt auf online.")
        #Der zufallsgenerator wird initialisiert
        random.seed()
        print("[INIT]  Zufallsgenerator erfolgreich initialisiert.")
    
    async def on_message(self, message):
        #Wenn der bot in einem Kanal eine Nachricht sieht oder eine DM bekommt
        if message.author == client.user:
            #Wenn der Bot die nachricht selbst geschriben hat
            #message.author ist immer der Name des Autors der Nachricht, egal in welchem kanal
            print("[SYS]   Der Bot hat eine Nachricht geschrieben um " + zeit() + ".")
            return
            #Damit der Bot nicht seine eigenen Nachrichten interpretiert, wird hier aus der
            #gesamten on_message()-Funktion gesprungen
        if message.content.startswith(einstellungen["prefix"]):
            print("[SYS]   \"" + str(message.content) + "\" ist ein Befehl, eingegangen um " + zeit() + " von " + str(message.author) + ".")
            if message.content == (einstellungen["prefix"] + "start"):
                if finde(message.author) == "nichtvorhanden":
                    print("[SPIEL] Der Spieler hat noch kein Spiel. Daher wird ein neues erstellt.")    
                    laufende_spiele.append( Spiel(message.author, message.author.id, 20, 20, 1))
                    await message.channel.send("Spiel gestartet. Viel Glück!")
                    print("[SPIEL] Neues Spiel erstellt für " + str(message.author) + " um " + zeit())
                    print("[SPIEL] Index: " + str(finde(message.author)) + " ; Zielpunkt liegt bei: (" + str(laufende_spiele[finde(message.author)].x) + "|" + str(laufende_spiele[finde(message.author)].y) + ").") 
                else:
                    print("[SPIEL] Der Spieler hat schon ein Spiel am laufen.")
                    await message.channel.send("Es konnte kein Spiel erstellt werden, da unter Deinem Namen schon eins erstellt wurde. Beende ein Spiel mit " + einstellungen["prefix"] + "quit.")
            elif message.content.startswith(einstellungen["prefix"] + "move"):
                #Dieser Befehl ist komplizierter: nach dem Anfang der Nachricht müssen noch weitere
                #teile der Message interpretiert werden
                spielzug = message.content.split()
                diff = distanz(finde(message.author), spielzug[1], spielzug[2])
                laufende_spiele[finde(message.author)].versuche += 1
                print("[MOVE]  Spieler " + str(message.author) + " macht einen Zug auf (" + str(spielzug[1]) + "|" + str(spielzug[2]) + "). Abstand (verzerrt): " + str(diff))
                if gewonnen(finde(message.author), spielzug[1], spielzug[2]):
                    await message.channel.send("Du hast im " + str(laufende_spiele[finde(message.author)].versuche) + ". Zug gewonnen! Herzlichen Glückwunsch!")
                    laufende_spiele.pop(finde(message.author))
                    print("[WIN]   Spieler " + str(message.author) + " wurde von seinem gewinn Benachrichtigt.")
                    print("[SPIEL] Das Spiel von " + str(message.author) + " wurde um " + zeit() + " beendet.")
                else:
                    await message.channel.send("Dein Zug wurde angenommen. Du lagst ungefähr " +  str(diff) + " Einheiten daneben. Dies war dein " + str(laufende_spiele[finde(message.author)].versuche) + ". Versuch.")
            elif message.content.startswith(einstellungen["prefix"] + "help"):
                print("[HELP]  " + str(message.author) + " hat die Hilfe erbeten.")
                await message.channel.send(hilfetext)
                print("[HELP]  Hilfe gesendet.")
            elif message.content.startswith(einstellungen["prefix"] + "quit"):
                print("[SPIEL] " + str(message.author) + " möchte sein Spiel beenden.")
                if finde(message.author) == "nichtvorhanden":
                    print("[SPIEL] " + str(message.author) + " wollte ein nicht vorhandenes Spiel beenden.")
                    await message.channel.send("Du hast kein Spiel, starte eines mit " + einstellungen["prefix"] + "start.")
                else:
                    laufende_spiele.pop(finde(message.author))
                    print("[SPIEL] Das Spiel von " + str(message.author) + " wurde um " + zeit() + " beendet.")
                    await message.channel.send("Dein Spiel wurde gelöscht. Starte ein neues mit " + einstellungen["prefix"] + "start.")
            elif message.content.startswith(einstellungen["prefix"] + "check"):
                print("[CHECK] " + str(message.author) + " möchte wissen, ob er ein Spiel besitzt")
                if finde(message.author) == "nichtvorhanden":
                    print("[CHECK] " + str(message.author) + " hat kein Spiel.")
                    await message.channel.send("Du hast gerade kein Spiel, starte eines mit " + einstellungen["prefix"] + "start.")
                else:
                    print("[CHECK] " + str(message.author) + " hat ein Spiel.")
                    await message.channel.send("Du hast gerade ein Spiel, und hast bereits " + str(laufende_spiele[finde(message.author)].versuche) + " Versuche gemacht.")
            elif message.content.startswith(einstellungen["prefix"] + "shutdown"):
                #Der Benutzer möchte das Programm beenden
                print("[EXIT]  " + str(message.author) + " möchte den Bot schliessen.")
                #Passwort-Check
                if message.content.split()[1] == einstellungen["passwort"]:
                    print("[EXIT]  Hat das korrekte Passwort eingegeben. Das Spiel wird geschlossen...")
                    await message.channel.send("Befehl Akzeptiert. Exit-Verfahren wird eingeleitet...")
                    print("[EXIT]  Das Programm wird geschlossen. Exit-Verfahren eingeleitet um " + zeit())
                    #Jeder Spieler mit einem laufenden Spiel wird informiert, dass sein Spiel endet
                    for i in laufende_spiele:
                        await client.get_user(i.spielerid).send("Dein Spiel wurde beendet, da das Botprogramm geschlossen wurde. Wenn ich wieder zur Verfügung stehe, setze ich meinen Status auf \"online\" und reagiere wieder auf Nachrichten von Dir. Bis dann!")
                        print("[EXIT]  Der Spieler " + str(i.spieler) + " wurde über den Exit informiert.")
                    #Status des Bots setzen
                    print("[EXIT]  Alle Spieler wurden Informiert. Neuen Status setzten...")
                    await client.change_presence(status = discord.Status.offline)
                    print("[EXIT]  Der Status des Bots wurde auf offline gesetzt. Nachricht an Auslöser...")
                    await message.channel.send("Exit-Verfahren beendet. Programm wird geschlossen. Tschüss!")
                    print("[EXIT]  Exit-Verfahren beendet um " + zeit() + ". Tschüss!")
                    sys.exit(0)

                else:
                    print("[EXIT]  Der Benutzer hat ein falsches Passwort angegeben.")
                    await message.channel.send("Falsches Passwort.")
            else:
                print("[SYS]   Der Befehl konnte nicht verstanden werden. Rückmeldung wird an Benutzer geschickt...")
                await message.channel.send("Das habe ich nicht verstanden. Benutze \"" + str(einstellungen["prefix"]) + "help\", um eine Hilfeseite anzeigen zu lassen.")        
#Initialisierung
client = MyClient()
#Der Token wird aus der json-Datei übernommen
client.run(einstellungen['token'])