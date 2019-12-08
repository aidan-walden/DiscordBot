import discord
from discord.ext import commands
import asyncio

class SCP(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def getScpInfo(self, scpname):
        import aiohttp
        from bs4 import BeautifulSoup
        if sum(c.isdigit() for c in scpname) > 2 and sum(c.isdigit() for c in scpname) < 5 and scpname.lower().replace('scp', '').replace('-', '').isdigit():
            if scpname.isdigit():
                scpname = f'SCP-{scpname}'
            elif 'scp' in scpname:
                scpname = f'{scpname[:3]}-{scpname[3:]}'.upper()
            url = f'http://www.scp-wiki.net/{scpname}'
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    page = await resp.read()
            soup = BeautifulSoup(page.decode('utf-8'), 'html.parser')
            iteminfo = soup.findAll('strong')
            for p in iteminfo:
                if p.get_text() == 'Special Containment Procedures:':
                    itemcontain = p.find_parent('p').get_text().split('Special Containment Procedures: ')[1]
                elif p.get_text() == 'Description:':
                    itemdesc = p.find_parent('p').get_text().split('Description: ')[1]
            imgurl = None
            try:
                for img in soup.find('div', class_='scp-image-block block-right').findChildren('img', recursive=False):
                    if img.name == 'img':
                        imgurl = img['src']
            except:
                pass
            try:
                return itemcontain, itemdesc, imgurl, scpname
            except NameError:
                return None, None, None, None
        else:
            if scpname.isdigit() and sum(c.isdigit() for c in scpname) < 5:
                i = 0
                while i < 3 - sum(c.isdigit() for c in scpname):
                    scpname = '0' + scpname
                return f'SCP-{scpname}', None, None, None
            else:
                return 'Invalid', None, None, None

    @commands.command()
    async def scp(self, ctx, scpname):
        contain, desc, imgurl, propername = await self.getScpInfo(scpname)
        if contain == 'Invalid':
            await ctx.send("Invalid SCP name.")
            return
        elif contain == None:
            await ctx.send("This command can only get info about SCPs that use the standard document format. An example of a SCP that does not use the standard format is SCP-001.")
            return
        elif desc == None:
            await ctx.send(f'Invalid SCP name. Did you mean {contain}?')
            return
        embed = discord.Embed(colour = discord.Colour.from_rgb(0,0,0))
        embed.set_author(name=propername)
        embed.add_field(name='Special Containment Procedures', value=contain, inline=False)
        embed.add_field(name='Description', value=desc, inline=False)
        if imgurl == None:
            embed.set_thumbnail(url='https://i.redd.it/f1u2wf28nqn21.jpg')
        else:
            embed.set_thumbnail(url=imgurl)
        await ctx.send(embed=embed)

    

def setup(client):
    client.add_cog(SCP(client))