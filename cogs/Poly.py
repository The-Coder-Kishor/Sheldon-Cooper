from mimetypes import init
from discord.ext import commands
import discord
import datetime
from sympy import *
from latex2p import l2py


class Poly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='findroot')
    async def findroot(self, ctx, *args):
        """Returns the roots of the equation in x"""
        try:
            k = ' '.join(args)
            x, y = symbols('x y')
            gfg_exp = l2py(k)
            intr = solve(gfg_exp,x)
            await ctx.send(intr)
        except:
            await ctx.send('Enter valid equation in x')

    @commands.command(name='factor')
    async def factor(self, ctx, *args):
        """Factors the equation. (if it is factorable!!!)"""
        try:
            k = ' '.join(args)
            x, y = symbols('x y')
            gfg_exp = l2py(k)
            intr = factor(gfg_exp,x)
            init_printing()
            await ctx.send(intr)
        except:
            await ctx.send('Enter valid equation in x')


def setup(bot):
    bot.add_cog(Poly(bot))