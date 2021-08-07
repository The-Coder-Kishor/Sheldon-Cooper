
from discord.ext import commands, tasks
import discord
import datetime
import random
import requests
from bs4 import BeautifulSoup as bs
import re
from mimetypes import init
from sympy import *
import asyncio
import extract


class Aops(commands.Cog):
        def _init_(self,bot):
                super()._init_()
                self.bot = bot

        @commands.command(name='aops')
        async def aops(self, ctx, *args):
                """Gives random math questions"""
                mes = extract.extractRandom()
                year = mes[0]
                contest = mes[1]
                form = mes[2]
                problem = mes[3]
                problemText = mes[4]
                url = 'http://artofproblemsolving.com/wiki/index.php?title=%s_%s_%s_Problems/Problem_%s' % (year, contest, form, problem)
                print(url)
                await ctx.send("Problem %s from the %s %s %s contest:" % (problem,year,contest,form))
                await ctx.send(url)

def setup(bot):
        bot.add_cog(Aops(bot))