import discord
import asyncio
import random
from discord.ext import commands



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description='description', intents=intents)

# NOTE: to get this to run you must create a file called "key.txt" in this folder and put your token into it
# bets = {}
# { @Vu : [
#   ([0], 100), ([1], 100)
# ] }

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

# ?bet <type of bet> <amount of money>
# ?info
# ?roll
def roll_roulette():
    return random.randint(0, 36)

@bot.group()
async def bet(ctx):
    pass

@bet.command()
async def single(ctx, n: int):
    if n <= 36 and n >= 0:
        roll = roll_roulette()
        if roll == n:
            await ctx.send("You won!")
        else:
            await ctx.send(f"Rolled a {roll}, you lost!")
    else:
        await ctx.send("Bet must be between 0 and 36")

@bet.command()
async def pair(ctx, n: str):
    if n == "even" or "odd":
        roll = roll_roulette()
        if roll == n:
            await ctx.send("You won!")
        else:
            await ctx.send(f"Rolled a {roll}, you lost!")
    else:
        await ctx.send("Bet must be between 0 and 36")

# HW: you are to write the "dozen" command
# It should be in the group "bet" (look at the decorator on the pair commmand and single command)
# This takes a number from 1-3, which determines the range the roulette result must be in to win
# for 1, it must be in 1-12, 2 it must be 13-24, and 3 it must be 25-36
# If the user enters a number outside this range, correct them
# If the rolled number is in the correct range, they've won, otherwise they've lost

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