from discord.ext import commands
import discord
import datetime


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='echo')
    async def echo(self, ctx, *, message):
        """Echose your message"""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Returns bot latency."""
        await ctx.send(f'🏓 {round(self.bot.latency * 1000)} ms.')

    @commands.command(name='dmhelp')
    async def dmhelp(self, ctx):
        """Gives dm help."""
        await ctx.author.send('You know, you can use the same sc.help command here')

    @commands.command()
    async def suggest(self,ctx, *args):
        """You can now send suggestions directly to the creators"""
        k = ' '.join(args)
        await ctx.send("Your recommendation will be duly sent to the bot creators")
        await ctx.send("In the meantime you can maybe join the support server: ")
        await ctx.send("https://discord.gg/DEAevXRduJ")
        channel = self.bot.get_channel(857202646268379164)
        await channel.send("Message from " + str(ctx.message.author) +": "+k)

    @commands.command(name='bot_info')
    async def get_info(self, ctx):
        """Returns bot_info."""
        embed = discord.Embed(
            title = 'Info',
            description = 'About Sheldon Cooper',
            colour = discord.Colour.blurple(),
            timestamp = datetime.datetime.utcnow()
        )
        embed.set_footer(text=f'This bot is running on {len(self.bot.guilds)} guilds')
        embed.add_field(name='Version', value='0.4', inline=True)
        embed.add_field(name='Language', value='Python 3.8.8', inline=True)
        embed.add_field(name='Discord.py', value='Version:1.7.2', inline=True)
        embed.set_thumbnail(url="https://data.whicdn.com/images/346034271/original.jpg")
        await ctx.send(embed = embed)

		
def setup(bot):
    bot.add_cog(Tools(bot))