import random
from discord import Embed, utils
from discord.ext import commands
from database import db
from config import LOTTO_TICKET_PRICE
from lib import icons
from lib.utils import fmat


class Lottery(commands.Cog, name='lottery'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):   
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.query(
            'INSERT OR IGNORE INTO lottery (Id) VALUES (?)', 
            member.id,
        )

    @commands.command(name='lottery', aliases=['lotto'])
    async def lottery(self, ctx):
        participants = db.all('SELECT Id, Tickets FROM lottery')
        pot = len(participants)*LOTTO_TICKET_PRICE if participants else 0
        embed = Embed(
            title=f'current pot is: ${fmat(pot)}',
            description='',
        )
        embed.set_author(name='PKB LOTTERY')
        await ctx.send(embed=embed)

    @commands.command(name='joinlotto', aliases=[])
    async def join_lottery(self, ctx):
        db.query(
            'UPDATE lottery SET Tickets = ? WHERE Id = ?',
            1,
            ctx.message.author.id,
        )

    @commands.has_permissions(administrator=True)
    @commands.command(name='drawlotto', aliases=[])
    async def draw_lottery(self, ctx):
        participants = db.all('SELECT Id, Tickets FROM lottery')
        pot = len(participants)*LOTTO_TICKET_PRICE if participants else 0
        winner_id = random.choice(participants)
        winner = self.client.get_user(winner_id)
        channel = utils.get(ctx.guild.channels, name='pkb-broadcast')
        embed = Embed(
            title=f'{winner} has won ${fmat(pot)}',
            description='',
        )
        embed.set_author(name='PKB LOTTERY DRAWING', icon_url=icons.moneybag)
        channel.send(embed=embed)

def setup(client):
    client.add_cog(Lottery(client))
