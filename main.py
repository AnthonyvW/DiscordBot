# This example requires the 'message_content' intent.

import discord

token = ""
# First line of secrets should be token
with open("secrets.txt", "r") as f:
    token = f.readline()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.all()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)