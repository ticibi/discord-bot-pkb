from discord import Embed
from discord.ext import commands
from database import db
from lib.utils import read_json


class Badges(commands.Cog, name='badges'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.command(name='badges', aliases=['mybadges'])
    async def display_badges(self, ctx):
        badges_raw = db.one(
            'SELECT Badges FROM badges WHERE Id = ?',
            ctx.message.author.id,
        )[0]
        badges_split = badges_raw.split()
        badges = read_json('data/badges')
        desc = ''
        if 'Y' not in badges_split:
            desc = 'you have not earned any badges'
        else:
            for i in range(len(badges_split)):
                if badges_split[i] == 'Y':
                    data = badges[str(i)]
                    desc += data['name'] + '\n - ' + data['description'] + '\n'
        embed = Embed(
            title='',
            description=desc,
        )
        embed.set_author(name=f'{ctx.message.author.name}\'s Badges')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Badges(client))
