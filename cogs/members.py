from discord import Embed
from discord.ext import commands
from database import db


class Members(commands.Cog, name='members'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.insert_all(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass


def setup(client):
    client.add_cog(Members(client))
