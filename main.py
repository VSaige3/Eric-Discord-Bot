import discord
import asyncio
import random
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description='description', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# HW: modify this command so that it is called "greet", and gives the user a welcome message when they use the command
@bot.command()
async def empty(ctx):
    await asyncio.sleep(1)

@bot.command()
async def echo(ctx, message: str):
    await ctx.send(message)

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