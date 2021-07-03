import subprocess
from discord.ext import commands
from config import LAVALINK


class Lavalink(commands.Cog, name='lavalink'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.is_owner()
    @commands.command(name="runll")
    async def run_lavalink(self, ctx):
        subprocess.call(
            "java -jar lavalink.jar",
            shell=True,
            cwd=LAVALINK,
        )

def setup(client):
    client.add_cog(Lavalink(client))
