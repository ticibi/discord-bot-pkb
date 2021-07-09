from discord import Embed
from discord.ext import commands
from database import db
from config import POINTS_RATE


class Leaderboards(commands.Cog, name='leaderboards'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):   
        print(f'{__name__} extension loaded')

    @commands.command(name='toppoints', aliases=['pointsleaderboard'])
    async def points_leaderboard(self, ctx):
        leaderboard = []
        for member in ctx.guild.members:
            points = db.one(
                'SELECT Points FROM members WHERE Id = ?', 
                member.id
            )
            leaderboard.append([member, points])
        
        if len(leaderboard) < 1:
            await ctx.send('not enough members to display leaderboard')
            return
        text = ''
        for member in leaderboard:
            text += f'{member[0]}: {member[1][0]}pts\n'
        
        embed = Embed(
            title='',
            description=text,
        )
        embed.set_author(name=f'{ctx.guild.name} POINTS LEADERBOARD')
        await ctx.send(embed=embed)

    @commands.command(name='topbank', aliases=['bankleaderboard'])
    async def bank_leaderboard(self, ctx):
        leaderboard = []
        for member in ctx.guild.members:
            points = db.one(
                'SELECT Bank FROM economy WHERE Id = ?', 
                member.id
            )
            leaderboard.append([member, points])
        
        if len(leaderboard) < 1:
            await ctx.send('not enough members to display leaderboard')
            return
        text = ''
        for member in leaderboard:
            text += f'{member[0]}: {member[1][0]}pts\n'
        
        embed = Embed(
            title='',
            description=text,
        )
        embed.set_author(name=f'{ctx.guild.name} POINTS LEADERBOARD')
        await ctx.send(embed=embed)

    @commands.command(name='exchangepoints')
    async def exchange_points(self, ctx, amount):
        _id = ctx.message.author.id
        points = db.one(
            'SELECT Points FROM members WHERE Id = ?', 
            _id,
        )[0]
        if not points:
            await ctx.send('not enough points')
            return
        if amount > points:
            await ctx.send('you cannot exchange more points than you have')
            return
        db.query(
            'UPDATE members SET Points = (Points - ?) WHERE Id = ?',
            amount,
            _id,
        )
        db.query(
            'UPDATE economy SET Bank = (Bank + ?) WHERE Id = ?',
            amount//POINTS_RATE,
            _id,
        )
        name = ctx.message.author.name
        await ctx.send(
            f'{name} exchanged {amount} pts for ${amount//POINTS_RATE}!'
        )

def setup(client):
    client.add_cog(Leaderboards(client))
