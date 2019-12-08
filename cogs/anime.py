import discord
from discord.ext import commands
from jikanpy import AioJikan
import asyncio

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mal(self, ctx, *, anime):
        jikan = AioJikan(loop=asyncio.get_event_loop())
        result = await jikan.search(search_type='anime', query=anime)
        await jikan.close()
        img_url = result['results'][0]['image_url']
        title = result['results'][0]['title']
        desc = result['results'][0]['synopsis']
        episode_count = result['results'][0]['episodes']
        score = result['results'][0]['score']
        url = result['results'][0]['url']
        embed = discord.Embed(colour = discord.Colour.from_rgb(46,81,162), url = url, title = title, description = desc)
        embed.add_field(name='Episodes:', value=episode_count, inline=False)
        embed.add_field(name='Score:', value=score, inline=False)
        embed.set_thumbnail(url=img_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Anime(client))