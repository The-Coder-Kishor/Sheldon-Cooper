import discord
from discord.ext import commands
import random

def setup(bot):
    bot.add_cog(Sheldon(bot))

class Sheldon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sheldon(self, ctx):
        """Who... who are you?"""
        groots = [
            "I am Sheldon",
            "**I AM Sheldon**",
            "I... am... *Sheldon*",
            "I am Sheldooooooon",
        ]
        punct = [
            "!",
            ".",
            "?"
        ]
        # Build our groots
        groot_max = 5
        groot = " ".join([random.choice(groots) + (random.choice(punct)*random.randint(0, 5)) for x in range(random.randint(1, groot_max))])
        await ctx.send(groot)