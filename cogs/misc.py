import random
from discord import Embed
from discord.ext import commands
from lib import icons


class MiscCommands(commands.Cog, name='misc'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.command(name='info')
    async def bot_info(self, ctx):
        desc = ''
        embed = Embed(
            title='',
            description=desc,
        )
        embed.set_author(name='PudgeyKitty Bot Info', icon_url=icons.info)
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        member = ctx.author.mention
        await ctx.send(f'{member}, your ping is {latency}ms',)

    @commands.command(name='flipcoin', aliases=['coinfip', 'coin'])
    async def flip_coin(self, ctx):
        result = random.choice(['heads', 'tails'])
        await ctx.send(result)

    @commands.command(name='random', aliases=['randomnumber', 'randnum', 'randn', 'rand'])
    async def random_number(self, ctx, min, max):
        number = random.randrange(min, max)
        await ctx.send(number)

def setup(client):
    client.add_cog(MiscCommands(client))
        