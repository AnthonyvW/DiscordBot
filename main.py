import random
import discord
import re

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

def modifier_check(input):
    global_mod = False
    explode_positive = False
    explode_negative = False

    # Modifier to all dice rolls
    if not input.find("i") == -1:
        global_mod = True
        input = input.replace("i", "")

    # Exploding positive
    if not input.find("e") == -1:
        explode_positive = True
        input = input.replace("e", "")

    # Exploding Negative
    if not input.find("l") == -1:
        explode_negative = True
        input = input.replace("l", "")

    return input, global_mod, explode_positive, explode_negative

def explode(input, max, num):
    total = []
    num_rolls = 0

    # This prevents 2 sided dice from being rolled with being set to explode on both 1 and 2
    if max == 1 or (1 in num and 2 in num and 2 == max):
        return total, num_rolls
    
    while input in num:
        input = random.randint(1, max)
        total.append(input)
        num_rolls += 1
    return total, num_rolls

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!r help"):
        await message.channel.send("""
## Bot Help
To roll dice use `!r ndm` to roll n m sided dice. The following are various suffixes you can add to change how dice are rolled. Make sure to add any letter suffixes after math.

You can add or subtract to the sum of the dice; for example `!r 2d6+3` will roll 2 six sided dice and then add 3 to the sum.

You can also add a modifier to all dice with the `i` suffix for example `!r 2d6+3i` will roll 2 six sided dice and add 3 to each roll.

You can explode dice with the `e` and `l` suffixes for example `!r 2d6+2e` will roll 2 six sided dice exploding the first die and then add 3 to the result. With each suffix if you roll the maximum and minimum possible rolls for the first die, it will keep rerolling the dice until a different roll is obtained adding each result to the total each time the dice is rerolled.
                                   """)

    else:
        if message.content.find('!r') > -1:
            try:
                # Combine message into one string for easy handling
                # This removes everything before !r and sets content equal to everything after the word containing !r combined together into one string without spaces
                content = "".join((message.content[message.content.index("!r"):]).split()[1:])
                total = 0
                modifier = 0
                global_modifier = False
                explode_positive = False
                explode_negative = False
                num_explodes = 0
                result = []
                content, global_modifier, explode_positive, explode_negative =  modifier_check(content)
                amounts = content.split('d')

                # Addition
                if not amounts[1].find("+") == -1:
                    temp = amounts[1].split("+")
                    modifier = int(temp[1])
                    amounts[1] = temp[0]

                # Subtraction
                if not amounts[1].find("-") == -1:
                    temp = amounts[1].split("-")
                    modifier = -(int(temp[1]))
                    amounts[1] = temp[0]

                # Generate Random Numbers
                if int(amounts[0]) == 0:
                    await message.channel.send("Please enter a number of dice greater than 0")
                    raise ValueError("User Entered 0 Dice")
                if int(amounts[1]) == 0:
                    await message.channel.send("Please enter a number of sides greater than 0")
                    raise ValueError("User Entered 0 Sides")

                temp = 0
                result.append(random.randint(1,int(amounts[1])))
                if(explode_positive and explode_negative):
                    temp, num_explodes = explode(result[-1], int(amounts[1]), [1, int(amounts[1])])
                    result.extend(temp)
                elif(explode_positive):
                    temp, num_explodes = explode(result[-1], int(amounts[1]), [int(amounts[1])])
                    result.extend(temp)
                elif(explode_negative):
                    temp, num_explodes = explode(result[-1], int(amounts[1]), [1])
                    result.extend(temp)

                if global_modifier:
                    result[-1] += modifier

                if int(amounts[0]) > 1:
                    for i in range(int(amounts[0]) - 1):
                        if global_modifier:
                            result.append(random.randint(1,int(amounts[1])) + modifier)
                        else:
                            result.append(random.randint(1,int(amounts[1])))

                # Output
                #response = f"Bot is Currently being Worked on if a feature doesn't work properly try again later\nYou rolled {content} "
                response = f"You rolled {content} "

                # Sum up and output list
                if not global_modifier:
                    total += modifier
                response += f"for a total of {total + sum(result)} : "

                response += "["

                explode_mod_symbol = ""
                if explode_positive:
                    explode_mod_symbol = "**"
                elif explode_negative:
                    explode_mod_symbol = "__"

                if num_explodes > 0:
                    response += explode_mod_symbol + str(result[0]) + explode_mod_symbol
                else:
                    response += str(result[0])

                for i in range(num_explodes):
                    response += ", " + explode_mod_symbol + str(result[i+1]) + explode_mod_symbol

                for i in range(len(result) - 1 - num_explodes):
                    response += ", " + str(result[i+1+num_explodes])
                
                response += "]"
                await message.channel.send(response)

            except Exception as e:
                # Make bot do nothing if message is in wrong format
                print(e)
                pass

client.run(token)