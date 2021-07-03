import asyncio
import random
from discord.ext import commands
from discord import Embed
from database import db
from config import DAILY_ICON, DAILY_REWARD, DAILY_MAX_STARS
from lib import colors, icons
from lib.utils import fmat


class Daily(commands.Cog, name='daily'):
    def __init__(self, client):
        self.client = client
    
    async def daily_reset(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.query(
            'INSERT OR IGNORE INTO daily (Id) VALUES (?)',
            member.id,
        )

    @commands.command(name='bonus', aliases=['daily', 'pp'])
    async def daily_bonus(self, ctx):
        if not db.check_exists(ctx.message.author.id):
            return
        claimed = db.one(
            'SELECT Claimed FROM daily WHERE Id = ?',
            ctx.message.author.id,
        )
        if claimed == 1:
            return
        embed = Embed(
            title='',
            description='',
            color=colors.GOLD,
        )
        embed.set_author(name='Daily Bonus', icon_url=icons.bonus)
        msg = await ctx.send(embed=embed)

        while True:
            for i in range(random.randrange(DAILY_MAX_STARS)):
                embed2 = Embed(
                    title=f'{DAILY_ICON*i}',
                    description=f'{ctx.message.author.name} has {i} stars!',
                    color=colors.GOLD,
                )
                embed2.set_author(name='Daily Bonus', icon_url=icons.bonus)
                await msg.edit(embed=embed2)
                await asyncio.sleep(1)
            break

        embed3 = Embed(
            title=f'{DAILY_ICON*i}',
            description=f'{ctx.message.author.name} has {i} stars!',
            color=colors.GOLD,
        )
        embed3.set_author(name=f'won ${fmat(i*DAILY_REWARD)}!', icon_url=icons.bonus)
        await msg.edit(embed=embed3)

        db.query(
            'UPDATE daily SET Claimed = ? WHERE Id = ?',
            1,
            ctx.message.author.id,
        )
        db.query(
            'UPDATE economy SET Bank = (Bank + ?) WHERE Id = ?',
            i*DAILY_REWARD,
            ctx.message.author.id,
        )
        db.query(
            'UPDATE daily SET Dailies = (Dailies + ?) WHERE Id = ?',
            1,
            ctx.message.author.id,
        )  

    @commands.command(name='vote')
    async def daily_vote(self, ctx):
        pass

def setup(client):
    client.add_cog(Daily(client))