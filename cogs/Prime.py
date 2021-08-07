from discord.ext import commands
import discord
import datetime
from sympy import *


class Prime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ispr')
    async def ispr(self, ctx,n):
        """Checks whether the number given is prime."""
        try:
            x = int(n)
            await ctx.send((isprime(x)))
        except:
            pass

    @commands.command(name='nextpr')
    async def nextpr(self, ctx,n):
        """Gives the next nearest prime number."""
        try:
            result = nextprime(n)
            await ctx.send(result)
        except:
            pass    

    @commands.command(name='prevpr')
    async def prevpr(self, ctx,n):
        """Gives the previous nearest prime number."""
        try:
            result = prevprime(n)
            await ctx.send(result)
        except:
            pass 

    @commands.command(name='listpr')
    async def listpr(self, ctx,n,k):
        """Lists all the prime numbers from the frist number to the second number."""
        try:
            await ctx.send(list(sieve.primerange(n,k)))
        except:
            pass 

    @commands.command(name='npr')
    async def npr(self,ctx,n):
        """Gives the nth prime number."""
        try:
            await ctx.send(prime((int(n))))
        except:
            pass

def setup(bot):
    bot.add_cog(Prime(bot))