# This example requires the 'message_content' intent.
import random
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
    
    if message.content.startswith('$hi'):
        await message.channel.send(f"Hello {message.author}")

    if message.content.startswith('$ping'):
        await message.channel.send('pong')

    if message.content.startswith('$roll'):
        content = message.content.split()[1]
        amounts = content.split('d')
        total = 0
        try:
            for i in range(int(amounts[0])):
                total += random.randint(1,int(amounts[1]))
            await message.channel.send(f"You rolled {amounts[0]} {amounts[1]} sided dice for a total of {total}")
        except Exception as e:
            # Make bot do nothing if message is in wrong format
            print(e)
            pass
    
    if message.content.startswith('$rps'):
        content = (message.content.split()[1]).lower()
        if content == 'scissors' or content == 'rock' or content == 'paper':
            result = random.randint(0,2) == 1
            if result == 0:
                await message.channel.send(f"You won!")
            elif result == 1:
                await message.channel.send(f"Tie!")
            else:
                await message.channel.send(f"You Lost!")

client.run(token)