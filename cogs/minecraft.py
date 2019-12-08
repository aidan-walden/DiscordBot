import minecrafttools
import discord
from discord.ext import commands

class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def serverinfo(self, ctx, ip):
        if len(ctx.message.content.split(' ')) > 2:
            await ctx.send('<@' + str(ctx.message.author.id) + '> Invalid usage of command.')
        else:
            msg = await ctx.send('<@' + str(ctx.message.author.id) + '> Aquiring server info, please wait...')
            result = await minecrafttools.getServerInfo(ip)
            await msg.edit(content='<@' + str(ctx.message.author.id) + '>\n' + result)

def setup(client):
    client.add_cog(Minecraft(client))
