import discord
import json
import datetime
import random
import math

#JSON öffnen

with open('config.json') as config_file:
    einstellungen = json.load(config_file)
    
def zeit():
    return str(datetime.datetime.now())

def finde(name):
    #In dieser Funktion soll nach einem Spiel gesucht werden, damit der Bot
    #einen Befehl dem richtigen laufendem spiel zuordnen kann.
    index = 0
    for i in laufende_spiele:
        if i.spieler == name:
            return index
        else:
            index += 1 #index wird angehoben und nächster listenplaytz durchsucht
    return "nichtvorhanden"

def distanz(index, x, y):
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
    if index == "nichtvorhanden":
        print("[ERROR] Ein Move für ein nicht existentes Spiel wurde an gewonnen() gereicht. Zeit: " + zeit())
    if (int(x) - laufende_spiele[index].x == 0) and (int(y) - laufende_spiele[index].y == 0):
        print("[WIN]   Das Spiel mit Index " + str(index) + " wurde gewonnen um " + zeit() + ".")
        return True
    else:
        return False
hilfetext = "Wie benutzt man diesen Bot? \n \nDas Spiel funktioniert wie folgt: ein Zielpunkt in einem zweidimensionalen Koordinatensystem wird zufällig bestimmt. Jetzt kann der Spieler Punkte angeben, deren Entfernung zum Ziel angegeben wird \(+/- eine Einheit\). Das Spiel ist gewonnen, wenn der Spieler genau auf den Punkt setzt. \n \n Befehle \(immer mit dem Präfix \"" + einstellungen["prefix"] + "\"\): \n \n\"start\": beginnt ein neues Spiel. Die Feldgröße ist 20 mal 20. \n\"quit\": beendet ein gerade laufendes Spiel.\n\"move\": einen Punkt angeben. Syntax: " + einstellungen["prefix"] + "move \[xKoordinate\] \[yKoordinate\].\n\"check\": anzeigen lassen, ob du ein Spiel am laufen hast.\n\"help\": diesen Text anzeigen lassen.\n\nViel Spaß!"


class Spiel:
    def __init__(self, spieler, xmax, ymax, verzerrung):
        self.spieler = spieler
        self.xmax = xmax
        self.ymax = ymax
        self.x = random.randint(0, xmax)
        self.y = random.randint(0, ymax)
        self.versuche = 0
        self.verzerrung = verzerrung
        
laufende_spiele = []

class MyClient(discord.Client):
    async def on_ready(self):
        print("[INIT]  Verbunden, mit dem Namen " + str(self.user))
        print("[INIT]  Verbunden ab " + zeit())
        random.seed()
        print("[INIT]  Zufallsgenerator erfolgreich initialisiert.")
    async def on_message(self, message):
        if message.author == client.user:
            print("[SYS]   Der Bot hat eine Nachricht geschrieben um " + zeit() + ".")
            return
        if message.content.startswith(einstellungen["prefix"]):
            print("[SYS]   \"" + str(message.content) + "\" ist ein Befehl, eingegangen um " + zeit() + " von " + str(message.author) + ".")
            if message.content == (einstellungen["prefix"] + "start"):
                if finde(message.author) == "nichtvorhanden":
                    print("[SPIEL] Der Spieler hat noch kein Spiel. Daher wird ein neues erstellt.")    
                    laufende_spiele.append( Spiel(message.author, 20, 20, 1))
                    print("[SPIEL] Neues Spiel erstellt für " + str(message.author) + " um " + zeit())
                    print("[SPIEL] Index: " + str(finde(message.author)) + " ; Zielpunkt liegt bei: (" + str(laufende_spiele[finde(message.author)].x) + "|" + str(laufende_spiele[finde(message.author)].y) + ").") 
                else:
                    print("[SPIEL] Der Spieler hat schon ein Spiel am laufen.")
                    await message.channel.send("Es konnte kein Spiel erstellt werden, da unter Deinem Namen schon eins erstellt wurde. Beende ein Spiel mit " + einstellungen["prefix"] + "quit.")
            elif message.content.startswith(einstellungen["prefix"] + "move"):
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
            else:
                print("[SYS]   Diese Nachricht konnte vom Bot nicht interpretiert werden.")
                await message.channel.send("Das habe ich nicht verstanden. Benutze \"" + str(einstellungen["prefix"]) + "help\", um eine Hilfeseite zu sehen.")
        
        
client = MyClient()
client.run(einstellungen['token'])