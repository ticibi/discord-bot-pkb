import discord
from discord.ext import commands
from config import CUSTOM_CHANNEL_CATEGORY_ID
from database import db


class Channels(commands.Cog, name='channels'):
    """allow members to create and manage their own channels"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.command(name='createchannel', aliases=['cc'])
    async def create_channel(self, ctx, type, name):
        channel_id = db.one(
            'SELECT ChannelId FROM custom_channels WHERE OwnerId = ?',
            ctx.message.author.id,
        )
        if channel_id:
            await ctx.send('you already own a channel')
            return
        category = discord.utils.get(
            ctx.guild.categories,   
            id=CUSTOM_CHANNEL_CATEGORY_ID
        )
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=True, 
                send_messages=True
            )
        }
        if name in ctx.guild.channels:
            await ctx.send('channel already exists')
            return
        if name not in ctx.guild.channels:
            if type == 'text':
                channel = await ctx.guild.create_text_channel(
                    name,
                    category=category
                )
            elif type == 'voice':
                channel = await ctx.guild.create_voice_channel(
                    name,
                    category=category
                )
        db.query(
            'INSERT OR IGNORE INTO custom_channels (ChannelId, OwnerId) VALUES (?,?)',
            channel.id,
            ctx.message.author.id,
        )
        await ctx.send(f'created new {type} channel {name}')

    @commands.command(name='deletechannel', aliases=['dc', 'delchannel', 'delch'])
    async def delete_channel(self, ctx):
        channel_id = db.one(
            'SELECT ChannelId from custom_channels WHERE OwnerId = ?',
            ctx.message.author.id,
        )[0]
        if not channel_id:
            await ctx.send('you do not own a channel')
            return
        channel = self.client.get_channel(channel_id)
        if not channel:
            return
        await channel.delete()
        db.query(
            'DELETE FROM custom_channels WHERE ChannelId = ?',
            channel_id,
        )
        await ctx.send('deleted channel', delete_after=10)

    @commands.command(name='makeowner')
    async def tranfer_channel_owner(self, ctx, *, member:discord.Member):
        channel_id = db.one(
            'SELECT ChannelId from custom_channels WHERE OwnerId = ?',
            ctx.message.author.id,
        )[0]
        if not channel_id:
            await ctx.send('you do not own a channel')
            return
        channel = self.client.get_channel(channel_id)
        db.query(
            'UPDATE custom_channels SET OwnerId = ? WHERE ChannelId = ?',
            member.id,
            channel_id,
        )
        await ctx.send(f'{member.mention} is now the owner of {channel.mention}')


def setup(client):
    client.add_cog(Channels(client))
