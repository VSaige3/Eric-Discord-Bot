import discord
import asyncio
import random
from discord.ext import commands



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description='description', intents=intents)

# NOTE: to get this to run you must create a file called "key.txt" in this folder and put your token into it

direction = "left"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name="countdown")
async def count_down(ctx, n: int, msg):
    """Counts down from a given number"""
    m = await ctx.send(f"counting down from {n}")
    while n > 0:
        n -= 1
        await asyncio.sleep(1)
        await m.edit(content=f"counting down from {n}")
    await m.edit(content=msg)

# HW1: create a new command here named "is_parity" that takes 2 arguments: an integer and a string
# If the string is not one of "even" or "odd", send a message to the effect that these are the only allowed values and stop
# If the string is "even" and the integer is even, or the string is "odd" and the integer is odd, send the message "yes"
# otherwise, send the message "no"; for example
# ?is_parity 10 green --> parity must be "even" or "odd"
# ?is_parity 10 odd --> no
# ?is_parity 12 even --> yes
@bot.command()
async def is_parity(ctx, n: int, parity):
    result = False
    if parity == "even":
        result = n % 2 == 0
    elif parity == "odd":
        result = n % 2 == 1
    else:
        await ctx.send("parity must be \"even\" or \"odd\"")
        return
    if result:
        await ctx.send("yes")
    else:
        await ctx.send("no")

# HW2: create a new command called "decay" which takes 2 numbers
# until the first number reaches 0, wait a number of seconds equal to the second number, then divide the first number by 2
# Send out the value of the first number each time you divide it
# Note that the first number should be an integer, but the second should be a float
# REMEMBER TO USE INTEGER DIVISION
@bot.command()
async def decay(ctx, a: int, b: float):
    while a > 0:
        a //= 2
        await ctx.send(a)
        await asyncio.sleep(b)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def create_channel(ctx, name: str):
    guild = ctx.message.guild
    await guild.create_text_channel(name)

@bot.command()
async def get_distance(ctx, x1: int, y1: int, x2: int, y2: int):
    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    await ctx.send(f'The distance is {d}')

@bot.command()
async def add(ctx, x: int, y: int):
    await ctx.send(f'The sum is {x + y}')

keyfile = open("key.txt")
token = keyfile.read()
keyfile.close()
bot.run(token)