from discord import Embed, utils
from discord.ext import commands
from database import db
from lib import colors, icons
from lib.utils import read_json, write_json


class Admin(commands.Cog, name='admin'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):   
        print(f'{__name__} extension loaded')

    @commands.has_permissions(administrator=True)
    @commands.command(name='setprefix')
    async def set_guild_prefix(self, ctx, prefix):
        if len(prefix) > 5:
            await ctx.send('prefix must be 5 or less characters', delete_after=60)
            return
        current_prefix = db.one(
            'SELECT Prefix FROM guilds WHERE Id = ?', 
            ctx.guild.id
        )
        db.query(
            'UPDATE guilds SET Prefix = ? WHERE Id = ?', 
            prefix, 
            ctx.guild.id
        )
        await ctx.send(
            f'Guild prefix changed from {current_prefix} to {prefix}'
        )

    @commands.is_owner()
    @commands.command(name="load")
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        await ctx.send(f"`loading:` {extension} ", delete_after=5)

    @commands.is_owner()
    @commands.command(name="unload")
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"`unloading:` {extension} ", delete_after=5)

    @commands.is_owner()
    @commands.command(name="reload")
    async def reload(self, ctx, extension):
        if extension != "all":
            self.client.reload_extension(f"cogs.{extension}")
            await ctx.send(f"`reloading:` {extension}", delete_after=5)
            return

        for cog in self.client.cogs:
            self.client.reload_extension(f"cogs.{cog}")
        await ctx.send("`reloaded {len(self.client.cogs)} extensions`", delete_after=5)

    @commands.has_permissions(administrator=True)
    @commands.command(name="clear", aliases=['clr', 'delete', 'del'])
    async def clear_messages(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"deleted {amount} messages", delete_after=1)

    @commands.is_owner()
    @commands.command(name='global')
    async def global_broadcast(self, ctx, *, message):
        for guild in self.client.guilds:
            try:
                channel_name = db.one(
                    'SELECT Broadcast FROM guilds WHERE Id = ?',
                    guild.id,
                )
                channel = utils.get(guild.channels, name=channel_name)
            except Exception as e:
                await ctx.send(f'unable to broadcast {e}')
        embed = Embed(
            title='',
            description=message,
            color=colors.BLURPLE,
        )
        embed.set_author(name='PKB GLOBAL BROADCAST', icon_url=icons.info)
        await channel.send(embed=embed)   

    @commands.is_owner()
    @commands.command(name='updatecmds')
    async def update_commands_list(self, ctx):
        _commands = read_json('data/commands')
        _commands['commands'] = []
        for cmd in self.client.commands:
            if cmd not in _commands:
                _commands['commands'].append(str(cmd))
        write_json(_commands, 'data/commands')
        await ctx.send(f'updated {len(self.client.commands)} commands')

    @commands.is_owner()
    @commands.command(name='addall')
    async def add_all_members_to_db(self, ctx):
        for member in ctx.guild.members:
            db.insert_all(member)
        await ctx.send('added all members to db')

def setup(client):
    client.add_cog(Admin(client))
