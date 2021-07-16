import discord
from discord.ext import commands
from database import db
from config import CATEGORY, GENERAL, BROADCAST, LOG, MESSAGES, BASIC_ROLE


class Guilds(commands.Cog, name='guilds'):
    def __init__(self, client):
        self.client = client

    async def create_channels(self, guild):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True, 
                send_messages=True
            )
        }
        log_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        category = await guild.create_category(
            CATEGORY, 
            overwrites=overwrites
        )
        if GENERAL not in guild.channels:
            general_channel = await guild.create_text_channel(
                GENERAL, 
                category=category
            )
            await general_channel.send(MESSAGES['welcome_general_channel'])
        if BROADCAST not in guild.channels:
            broadcast_channel = await guild.create_text_channel(
                BROADCAST,
                overwrites=overwrites,
                category=category,
            )
            await broadcast_channel.send(MESSAGES['welcome_broadcast_channel'])
        if LOG not in guild.channels:
            log_channel = await guild.create_text_channel(
                LOG,
                overwrites=log_overwrites,
                category=category,
            )
            await log_channel.send(MESSAGES['welcome_log_channel'])

    async def create_roles(self, guild):
        await guild.create_role(name=BASIC_ROLE)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.query(
            'INSERT OR IGNORE INTO guilds (Id) VALUES (?)',
            guild.id,
        )
        
        await self.create_channels(guild)
        await self.create_roles(guild)

        for member in guild.members:
            try:
                db.insert_all(member)
            except Exception as e:
                raise e
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.query(
            'DELETE FROM guilds WHERE Id = ?',
            guild.id,
        )
                

def setup(client):
    client.add_cog(Guilds(client))
