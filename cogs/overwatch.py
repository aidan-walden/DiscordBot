import discord
from discord.ext import commands
import os
import random
import common

class Overwatch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def owlootboxfarm(self, ctx):
        await ctx.send('<@' + str(ctx.message.author.id) + '> Have that itch to gamble but don\'t feel like spending money to do it? Then use this method to farm loot boxes while AFK!\nIt is recommended to start this method before you go to sleep. Please note that you cannot use your computer while using this method.\n1. Set region to Europe in Battle.net.\n2. Go to controls and bind \'Move forwards\' to spacebar.\n3. Go to video settings and put options to lowest quality possible, including resolution. Also put the game in windowed mode.\n4. Go to custom games and search for \'XP\'. Then join one that isn\'t full. If you can\'t find one that isn\'t full, then join the one with the least amount of spectators.\n5. Put a weight on your spacebar and walk away.\nThis yields roughly 2 - 3 loot boxes per night.\nIf at any point you encounter error BN-563, DO NOT ATTEMPT TO LOGIN THROUGH THE OVERWATCH CLIENT. CLOSE OVERWATCH AND REOPEN IT.\nImage tutorial: https://imgur.com/a/TOG4LFj')

def setup(client):
    client.add_cog(Overwatch(client))
