import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print("Verbunden, mit dem Namen " + str(self.user))
    async def on_message(self, message):
        print("Nachricht empfangen von " + str(message.author) + ": " + str(message.content))

client = MyClient()
client.run('NzgwNTM1OTIyMTUxNzg0NDY4.X7wguQ.dpfiFk-WlTVpw8nqfqyvma_VglQ')