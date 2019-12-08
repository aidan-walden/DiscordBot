import asyncio
import discord
from discord.ext import commands
#import socket
#import json
#import threading
import random
import os
#import traceback

ownerid = ''

client = commands.Bot(command_prefix = '~')
client.remove_command('help')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    


@client.command()
async def loadext(ctx, extension):
    if ctx.message.author.id == ownerid:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}')
    else:
        ctx.send(f'<@{ctx.message.author.id}> You do not have access to that command.')
@client.command()
async def unloadext(ctx, extension):
    if ctx.message.author.id == ownerid:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}')
    else:
        ctx.send(f'<@{ctx.message.author.id}> You do not have access to that command.')
@client.command()
async def reloadext(ctx, extension):
    if ctx.message.author.id == ownerid:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}')
    else:
        ctx.send(f'<@{ctx.message.author.id}> You do not have access to that command.')


@client.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.red())
    embed.set_author(name='Help')
    embed.add_field(name=client.command_prefix + 'help', value='Shows this message.', inline=False)
    embed.add_field(name=client.command_prefix + 'changelog', value='View recent changes to the bot.', inline=False)
    embed.add_field(name=client.command_prefix + 'serverinfo <server IP>', value='Gets the Minecraft server info for IP specified.', inline=False)
    embed.add_field(name=client.command_prefix + 'owlootboxfarm', value='Sends a text tutorial on how to farm loot boxes while AFK in Overwatch.', inline=False)
    embed.add_field(name=client.command_prefix + 'scp <SCP number, either including or not including the "SCP-" prefix>', value='Sends info about the specified SCP article.', inline=False)
    await ctx.send(embed=embed)

@client.command()
async def changelog(ctx):
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.set_author(name='Recent changes')
    embed.add_field(name='SCP info grabber commands', value=f'The bot can now show information about most SCP articles. Use the {client.command_prefix}scp command and try it out for yourself!', inline=False)
    await ctx.send(embed=embed)

@loadext.error
@unloadext.error
@reloadext.error
async def ext_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('That cog could not be found.')
    else:
        print(type(error))

@client.check
def is_blacklisted(ctx):
    import sqlite3
    from sqlite3 import Error

    conn = sqlite3.connect("./assets/blacklist.db")
    cursor = conn.cursor()
    cursor.execute('SELECT userid FROM users')
    blacklist = [x[0] for x in cursor.fetchall()]
    conn.close()
    return str(ctx.message.author.id) not in blacklist

async def changeActivity():
    newActivity = random.choice(activities)
    print(f'Changing activity to {newActivity.name}...')
    await client.change_presence(activity=newActivity)


client.run('', bot=False)
