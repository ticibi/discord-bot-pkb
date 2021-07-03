from discord.ext import commands
from discord import Embed, Member, utils


class LogEntry():
    def __init__(self, mod, member, message, duration, remarks):
        self.mod = mod
        self.member = member
        self.message = message
        self.duration = duration
        self.remarks = remarks


class AutoMod(commands.Cog, name='automod'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
    
    @commands.command(name='report')
    async def report_member(self, ctx, *, member:Member):
        try:
            channel = utils.get(ctx.guild.channels, name='pkb-modlog')
        except Exception as e:
            return
        embed = Embed(
            title='',
            description=f'{member}\nreported by:{ctx.message.author}'
        )
        embed.set_author(name='Member Report')
        await channel.send(embed=embed)
        await ctx.message.delete()
        await ctx.send('report received', delete_after=5)

def setup(client):
    client.add_cog(AutoMod(client))
