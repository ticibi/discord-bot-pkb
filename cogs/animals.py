import os
import json
import requests
from discord.ext import commands
from discord import Embed
from lib import colors


class Animals(commands.Cog, name='animals'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):   
        print(f'{__name__} extension loaded')

    @commands.command(name="fox")
    async def get_fox(self, ctx):
        await ctx.message.delete()
        try:
            url = "https://randomfox.ca/floof/"
            r = requests.get(url)
        except Exception as e:
            raise e

        data = json.loads(r.text)
        embed = Embed(
            title='cool Fox',
            color=colors.GREY,
            url='https://randomfox.ca'
        )
        embed.set_image(url=data['image'])
        embed.set_footer(text=f'brought to you by {url}')
        await ctx.send(embed=embed)

    @commands.command(name="cat")
    async def get_cat(self, ctx):
        await ctx.message.delete()
        try:
            url = "http://aws.random.cat/meow"
            r = requests.get(url)
        except Exception as e:
            raise e

        data = json.loads(r.text)
        embed = Embed(
            title="cute Cat",
            color=colors.GREY,
            url="http://aws.random.cat/"
        )
        embed.set_image(url=data['file'])
        embed.set_footer(text=f'brought to you by {url}')
        await ctx.send(embed=embed)


    @commands.command(name="dog")
    async def get_dog(self, ctx):
        await ctx.message.delete()
        try:
            url = "https://dog.ceo/api/breeds/image/random"
            r = requests.get(url)
        except Exception as e:
            raise e
        data = json.loads(r.text)
        embed = Embed(
            title="nice Doggo",
            color=colors.GREY,
            url="https://dog.ceo/"
        )
        embed.set_image(url=data['message'])
        embed.set_footer(text=f'brought to you by {url}')
        await ctx.send(embed=embed)

    @commands.command(name="nasa")
    async def get_nasa(self, ctx):
        await ctx.message.delete()
        try:
            url = "https://api.nasa.gov/planetary/apod?api_key=" + os.environ.get('NASA_APOD_KEY')
            r = requests.get(url)
        except Exception as e:
            raise e
        data = json.loads(r.text)
        embed = Embed(
            title=f"{data['copyright']}",
            color=colors.GREY,
            url=url
        )
        embed.set_image(url=data['url'])
        embed.set_footer(text=f'brought to you by NASA APOD')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Animals(client))
