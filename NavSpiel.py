import discord
import json
import datetime
import random

#JSON öffnen

with open('config.json') as config_file:
    einstellungen = json.load(config_file)

class Spiel:
    def __init__(self, spieler, xmax, ymax):
        self.spieler = spieler
        self.xmax = xmax
        self.ymax = ymax
        self.x = random.randint(0, xmax)
        self.y = random.randint(0, ymax)
        self.versuche = 0

laufende_spiele = []

class MyClient(discord.Client):
    async def on_ready(self):
        print("Verbunden, mit dem Namen " + str(self.user))
        print("Verbunden ab " + str(datetime.datetime.now()))
        random.seed()
        print("Zufallsgenerator erfolgreich initialisiert.")
        laufende_spiele.append( Spiel("Testspieler", 20, 20))
    async def on_message(self, message):
        print("Nachricht empfangen von " + str(message.author) + ": " + str(message.content))
        if message.author == client.user:
            print("Diese Nachricht wurde vom Bot geschrieben und wird daher ignoriert.")
            return
        if message.content.startswith(einstellungen["prefix"]):
            print("Diese Nachricht ist ein Befehl, eingegangen um " + str(datetime.datetime.now()))
            if message.content == (einstellungen["prefix"] + "start"):
                laufende_spiele.append( Spiel(message.author, 20, 20))
                print("Neues Spiel erstellt für " + str(message.author) + " um " + str(datetime.datetime.now()))
            if message.content.startswith(einstellungen["prefix"] + "move"):
                print("Spieler möchete einen !move machen")
                index = laufende_spiele.spieler.index(message.author)
                eingabe = message.content.split()
                xguess = eingabe[2]
                yguess = eingabe[3]
                print("Neuer Versuch von " + str(message.author) + " um " + str(datetime.datetime.now()) + ": " + xguess + " " + yguess)
                
                
client = MyClient()
client.run(einstellungen['token'])