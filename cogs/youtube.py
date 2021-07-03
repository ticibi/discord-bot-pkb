from discord import Embed
from discord.ext import commands
from youtube_search import YoutubeSearch


URL = 'https://www.youtube.com'

class Youtube(commands.Cog, name='youtube'):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):   
        print(f'{__name__} extension loaded')

    @commands.command(name='youtube', aliases=['yt'])
    async def search_youtube(self, ctx, *, search):
        terms = search.replace(" ", "_")
        result = YoutubeSearch(terms, max_results=8).to_dict()
        message = await ctx.send(f'searching {search} on YouTube...')
        embed = Embed(
            title='',
            description=''
        )
        for i in range(len(result)):
            text = f'{result[i]["title"]}\n{result[i]["channel"]}\n{result[i]["views"]}'
            url = f'{URL}{result[i]["url_suffix"]}'
            embed.add_field(
                name=text,
                value=url,
                inline=False
            )
        embed.set_author(name=f'YouTube search results for {search}', url=URL)
        await message.delete()
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(Youtube(client))
