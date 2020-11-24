import discord
import json

#JSON öffnen

with open('config.json') as config_file:
    einstellungen = json.load(config_file)


class MyClient(discord.Client):
    async def on_ready(self):
        print("Verbunden, mit dem Namen " + str(self.user))
    async def on_message(self, message):
        print("Nachricht empfangen von " + str(message.author) + ": " + str(message.content))

client = MyClient()
client.run(einstellungen['token'])