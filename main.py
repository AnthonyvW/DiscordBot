# This example requires the 'message_content' intent.

import discord

token = ""
# First line of secrets should be token
with open("secrets.txt", "r") as f:
    token = f.readline()

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print(f"{message.author} : {message.content}")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)