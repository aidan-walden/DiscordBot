import discord
from discord.ext import commands
import detectAnime
import json

class Maintenance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def delanime(self, ctx, *, title):
        if ctx.message.author.id == ownerid:
            import sqlite3
            from sqlite3 import Error

            conn = sqlite3.connect("./assets/animes.db")
            cursor = conn.cursor()
            cursor.execute('DELETE FROM animes WHERE LOWER(name)=?', (title.lower(),))
            conn.commit()
            conn.close()
            detectAnime.topAnimes = detectAnime.getAnimesFromDisk()
            await ctx.send(f"Deleted {title} from database and reloaded database.")
        else:
            await ctx.send("You do not have access to that command.")

    @commands.command()
    async def addanime(self, ctx, title):
        if ctx.message.author.id == ownerid:
            import sqlite3
            from sqlite3 import Error

            conn = sqlite3.connect("./assets/animes.db")
            cursor = conn.cursor()
            print(len(detectAnime.topAnimes))
            cursor.execute('INSERT INTO animes VALUES(?,?)', (len(detectAnime.topAnimes) + 1, title))
            conn.commit()
            conn.close()
            detectAnime.topAnimes = detectAnime.getAnimesFromDisk()
            await ctx.send(f"Added {title} to database and reloaded database.")
        else:
            await ctx.send("You do not have access to that command.")

    @commands.command()
    async def blacklist(self, ctx, user):
        if ctx.message.author.id == ownerid:
            import sqlite3
            from sqlite3 import Error

            conn = sqlite3.connect("./assets/blacklist.db")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users(userid) VALUES(?)', (str(ctx.message.mentions[0].id),))
            await ctx.send("Blacklisted specified user. The bot will now ignore any message they send.")
            conn.commit()
            conn.close()
        else:
            await ctx.send("You do not have access to that command.")
    

    @commands.command()
    async def pardon(self, ctx, user):
        if ctx.message.author.id == ownerid:
            import sqlite3
            from sqlite3 import Error

            conn = sqlite3.connect("./assets/blacklist.db")
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE userid=?', (str(ctx.message.mentions[0].id),))
            conn.commit()
            conn.close()
            await ctx.send("Pardoned specified user. The bot will now recognize any message they send.")
        else:
            await ctx.send("You do not have access to that command.")

    @commands.command()
    async def myactivity(self, ctx):
        activityType = str(ctx.message.author.activity.type).split('.')[1]
        state = None
        details = None
        assets = None
        try:
            state = ctx.message.author.activity.state
            details = ctx.message.author.activity.details
            assets = ctx.message.author.activity.assets
        except:
            pass

        await ctx.send(f'You are currently {activityType} {ctx.message.author.activity.name}, with state {state}. Details: {details}. Assets: {assets}')

    @commands.command()
    async def changenick(self, ctx, *, newnick):
        if ctx.message.author.id == ownerid:
            if newnick == '[[NONE]]':
                await ctx.message.guild.get_member(self.client.user.id).edit(nick=None)
                await ctx.send('Cleared nickname.')
            else:
                await ctx.message.guild.get_member(self.client.user.id).edit(nick=newnick)
                await ctx.send(f'Changed nickname to "{newnick}".')
            
        else:
            await ctx.send('You do not have access to that command.')

    @commands.command()
    async def delprev(self, ctx, msglimit=1):
        if ctx.message.author.id == ownerid:
            async for message in ctx.message.channel.history(limit=msglimit + 1):
                if message.author.id == self.client.user.id:
                    await message.delete()
        else:
            await ctx.send('You do not have access to that command.')

def setup(client):
    client.add_cog(Maintenance(client))
