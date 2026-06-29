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

# { 
#   @Vu : 100
# }

class Bet:
    def __init__(self, winning_spaces, wager):
        self.winning_spaces = winning_spaces
        self.wager = wager

    def wins_on_roll(self, roll: int):
        if roll in self.winning_spaces:
            return True
        else:
            return False
    
    def get_payout(self):
        return (36 // len(self.winning_spaces)) - 1
    
    def get_wager(self):
        return self.wager
    
    def get_winnings(self, roll):
        if self.wins_on_roll(roll):
            return self.get_wager() * (self.get_payout() + 1)
        else:
            return 0


class BetManager:
    def __init__(self, starting_money=100, minimum_bet=10, max_players=500, max_bets=100, max_debt=0):
        self.starting_money = starting_money
        self.minimum_bet = minimum_bet
        self.max_players = max_players
        self.max_bets = max_bets
        self.max_debt = max_debt
        self.bets = {}
        self.money = {}
    
    def add_user(self, user: discord.User):
        """
        Registers a user of our bot, and gives them starting cash.
        If the addition of the user would go over our maximum player count, returns false.
        If the addition of the user succeeds, returns true.
        """
        if user in self.money:
            return False
        if len(self.money) + 1 >= self.max_players:
            return False
        self.money[user] = self.starting_money
        return True
    
    def place_bet(self, user: discord.User, wager: int, winning_spaces):
        """
        Attempts to place a bet for a given user, wager, and winning spaces.
        Returns false if the bet is invalid or would voilate the constraints of our manager.
        """
        if user not in self.money:
            return False
        if wager < self.minimum_bet:
            return False
        new_balance = self.money[user] - wager
        if new_balance < -self.max_debt:
            return False
        self.money[user] = new_balance
        bet = Bet(winning_spaces, wager)
        if user in self.bets:
            if len(self.bets[user]) >= self.max_bets:
                return False
            self.bets[user].append(bet)
        else:
            if self.max_bets < 1:
                return False
            self.bets[user] = [bet]
        return True
    
    def get_results_from_roll(self, roll):
        """
        Updates user's accounts according to their bets and the result of the roll.
        Returns a dictionary of profits for each user
        """
        profits = {} # keep track of the change in money for each person
        for user in self.bets:
            profits[user] = 0
            for bet in self.bets[user]:
                # get stats
                winnings = bet.get_winnings(roll)
                profit = winnings - bet.get_wager()
                profits[user] += profit
                # change money
                self.money[user] += winnings
        return profits
    
    def clear_bets(self):
        """
        Clears all bets. To be used after getting the result of a roll
        """
        self.bets = {}

    def get_accounts(self):
        """
        Returns a dictionary of each user with their current account balance.
        """
        return self.money
    
    def get_bets(self, user: discord.User):
        """
        Returns a list of bets a user has placed, or an empty list if they haven't placed any.
        """
        # using the get method!!
        return self.bets.get(user, [])

manager = BetManager(max_debt=100)

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

# HW3.0: write the roll command. The part that rolls a random number has been provided, but you must use the
# "manager.get_results_from_roll" method to apply the roll, and then clear the bets with "manager.clear_bets"
@bot.command()
async def roll(ctx):
    roll = roll_roulette()
    result = manager.get_results_from_roll(roll)
    manager.clear_bets()
    await ctx.send(f"Rolled a {roll}!")
    await ctx.send(str(result)) # Not nice, but works for debugging

# HW3.1: This command should use the manager "get_accounts" method to get information about each person's account
# and then print them to the chat in a nice manner (subjective). Remember you can use format strings
# It may also help to print your messages using "print" in order to debug them
@bot.command()
async def balances(ctx):
    """
    Prints current balances for all players
    """
    msg = "Current Balances:\n"
    accounts = manager.get_accounts()
    for user in accounts:
        msg += f"\t{user.display_name}: {accounts[user]} points\n"
    await ctx.send(msg)

# HW3.2: I've begun this command for you. This should use the "add_user" feature of our manager to register a new user
# If registration fails, print out a message informing them that it failed. To get the current user, use ctx.author
@bot.command()
async def register(ctx):
    """
    Registers a user
    """
    if manager.add_user(ctx.author):
        await ctx.send("User added!")
    else:
        await ctx.send("Could not add user!")

# LOOK HERE: I've modified this function so that it uses our new bet interface
# HW3.3 is to modify one of the other commands to use our new interface
# Note how I've had to add a new parameter for the wager
@bet.command()
async def dozen(ctx, doz: int, wager: int):
    winning_range = []
    # create the range of numbers that let us win
    if doz == 1:
        winning_range = range(1, 13)
    elif doz == 2:
        winning_range = range(13, 25)
    elif doz == 3:
        winning_range = range(25, 37)
    else:
        # If they enter an invalid dozen, tell them off
        await ctx.send("Bet must be 1, 2 or 3")
        return
    user = ctx.author
    if manager.place_bet(user, wager, winning_range):
        await ctx.send("Bet placed!")
    else:
        await ctx.send("Invalid bet!")

# This is the one I've chosen to modify
@bet.command()
async def pair(ctx, n: str, wager: int):
    winning_range = []
    if n == "even":
        winning_range = range(2, 37, 2)
    elif n == "odd":
        winning_range = range(1, 37, 2)
    else:
        await ctx.send("Bet must be even or odd")
        return
    user = ctx.author
    if manager.place_bet(user, wager, winning_range):
        await ctx.send("Bet placed!")
    else:
        await ctx.send("Invalid bet!")

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
async def red(ctx):
    red_set = [1, 3, 5, 7, 9, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    roll = roll_roulette() # run the table
    if roll in red_set:
        await ctx.send(f"Rolled a {roll}, you won!")
    else: # otherwise, lose
        await ctx.send(f"Rolled a {roll}, you lost!")

@bet.command()
async def black(ctx):
    black_set = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    roll = roll_roulette() # run the table
    if roll in black_set:
        await ctx.send(f"Rolled a {roll}, you won!")
    else: # otherwise, lose
        await ctx.send(f"Rolled a {roll}, you lost!")

keyfile = open("key.txt")
token = keyfile.read()
keyfile.close()
bot.run(token)