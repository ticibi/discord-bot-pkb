import discord
from discord.ext import commands


class Events(commands.Cog, name='events'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client:
            return
        channel = discord.utils.get(member.guild.channels, name='🐀tarkov')
        #await channel.send(f'{member.name} joined', tts=True, delete_after=2)
        #await channel.send(f'{member.name} joined {after.channel.name}', delete_after=60)
    
def setup(client):
    client.add_cog(Events(client))