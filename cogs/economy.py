from datetime import datetime
from discord import Embed, Member
from discord.ext import commands
from database import db
from config import POINTS_RATE


class Economy(commands.Cog, name='economy'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} extension loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.query(
            'INSERT OR IGNORE INTO members (Id, DateJoined) VALUES (?,?)', 
            member.id, 
            datetime.utcnow(),
        )

    @commands.command(name='points', aliases=['mypoints', 'mypts', 'pts'])
    async def check_points(self, ctx):
        points = db.one(
            'SELECT Points FROM members WHERE Id = ?', 
            ctx.message.author.id
        )[0]
        embed = Embed(
            title='',
            description=f'points: {points}'
        )
        embed.set_author(name=f'{ctx.message.author.name}')
        await ctx.send(embed=embed)

    @commands.command(name='bank', aliases=['money', 'mybank', 'mymoney'])
    async def check_bank(self, ctx):
        bank = db.one(
            'SELECT Bank FROM economy WHERE Id = ?',
            ctx.message.author.id,
        )[0]
        if not bank:
            return
        embed = Embed(
            title='',
            description=f'${bank}'
        )
        embed.set_author(name=f'{ctx.message.author}\'s Bank Account')
        await ctx.send(embed=embed)

    @commands.command(name='exchangebank')
    async def exchange_bank(self, ctx, amount):
        _id = ctx.message.author.id
        bank = db.one(
            'SELECT Bank FROM economy WHERE Id = ?', 
            _id,
        )[0]
        if not bank:
            return
        if amount > bank:
            await ctx.send('you cannot exchange more money than you have')
            return
        db.query(
            'UPDATE members SET Bank = (Bank - ?) WHERE Id = ?',
            amount,
            _id,
        )
        db.query(
            'UPDATE members SET Points = (Points + ?) WHERE Id = ?',
            amount*POINTS_RATE,
            _id,
        )
        name = ctx.message.author.name
        await ctx.send(
            f'{name} exchanged ${amount} for {amount*POINTS_RATE} pts!'
        )

    @commands.command(name='transfer')
    async def transfer_bank(self, ctx, amount, *, member:Member):
        bank = db.one(
            'SELECT Bank FROM economy WHERE Id = ?',
            ctx.message.author.id,
        )[0]
        if amount < 0:
            await ctx.send('you cannot send a negative amount')
            return
        if amount > bank:
            await ctx.send('insufficient funds')
            return
        if not member:
            return
        db.query(
            'UPDATE economy SET Bank = (Bank - ?) WHERE Id = ?',
            amount,
            ctx.message.author.id,
        )
        db.query(
            'UPDATE economy SET Bank = (Bank + ?) WHERE Id = ?',
            amount,
            member.id,
        )
        name = ctx.message.author.name
        await ctx.send(f'{name} transfered ${amount} to {member.name}')

def setup(client):
    client.add_cog(Economy(client))
