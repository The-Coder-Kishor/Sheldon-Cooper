from discord.ext import commands, tasks
import discord
import requests as req
import random
import baseconvert
import requests as req
from urllib.parse import urlencode, quote_plus
from sympy import *
import json
from latex2p import l2py

class Math(commands.Cog):
    def _init_(self):
        super()._init_()

    def random_color(self):
        hexa = "0123456789abcd"
        random_hex = "0x"
        for i in range(6):
            random_hex += random.choice(hexa)
        return discord.Colour(int(random_hex,16))

    def create_embed(self,title,desc,colour,image=""):
        embed = discord.Embed()
        embed.title = title
        embed.description = desc
        embed.colour = colour
        if(image !=""):
            embed.set_image(url=image)
        return embed

    @commands.command(name='base')
    async def base(self, ctx, number:str,base1:int, base2:int):
        """<number> <original base> <new base> returns the number in the new base
            e.g. 10 10 2 will return 1010"""
        try:
            await ctx.send(baseconvert.base(number, base1, base2, string=True))
        except:
            await ctx.send('Please use sc.help <command name> to know more about the command')

    @commands.command(name='factorial')
    async def factorial(self, ctx, n:int):
        """Returns factorial of the number passed"""
        try:
            await ctx.send(factorial(n))
        except:
            await ctx.send('Please use sc.help <command name> to know more about the command')

    @commands.command(name='smath')
    async def math(self, ctx, *args):
        """For evaluating sinlge one line math expressions. If you want more precision add pres=<value> at the end"""
        inp = ' '.join(args)
        payload = {}
        exp = ""
        pres = ""
        if(inp.find("pres")!= -1):
            ind = inp.find("pres")
            exp = inp[:ind]
            pres = inp[ind:]
            pres = pres.replace(" ","")
            pres = pres[5:]
            payload = {'expr':exp, 'precision':pres}
            result = urlencode(payload, quote_via=quote_plus)
        else:
            exp = inp
            payload = {'expr':exp}
            result = urlencode(payload)
        url = "https://api.mathjs.org/v4/?"+result
        response = req.get(url)
        if(response.status_code == 200):
            output = (response.text)
        else:
            output = 'Error:' + response.text
        title = "Calc"
        math = "https://api.mathjs.org/"
        desc ="**Expression :** "+exp+"\n"+"**Requested by :** "+str(ctx.author)+"\n"+"**Precision :** "+pres+"\n"+"**Result :** "+output+"\n"+"**Know more:** "+math
        color = color = self.random_color()
        image = ""
        embed = self.create_embed(title,desc,color,image)
        await ctx.send(embed = embed)
        
    @commands.command(name='cmath')
    async def cmath(self,ctx,*args):
        """Use the help command to know more - For evaluating multiple line math expressions. 
        Syntax: <expr1>,<expr2>,....,<pres=n>
        Now with variavle support. Note variables are only remembered for one command so pass
        all required functions with the variable in one command """
        inp = ' '.join(args)
        data = inp.split(",")
        leng = len(data)
        last = data[leng-1]
        url='http://api.mathjs.org/v4/'
        headers={"content-type": "application/json"}
        output = {}
        flag = 0
        pres = ""
        if(last.find("pres")!= -1):
            last = last.replace(" ","")
            pres = last[5:]
            flag = 1
            exp = data.pop(leng-1)
            variables = {
                "expr": data,
                "precision": pres
                }
            r = req.post(url, json=variables, headers=headers)
        else:
            flag = 0
            variables = {
                "expr": data
                }
            r = req.post(url, json=variables, headers=headers)
        output = json.loads(r.text)
        desc = ""
        if((output["error"] == "null")or(output["error"] == None)):
            if(flag == 1):
                for i in range(0,leng-1):
                    desc = desc + data[i]+": " + output["result"][i] + "\n"
            else:
                for i in range(0,leng):
                    desc = desc + data[i]+": " + output["result"][i] + "\n"
        else:
            desc = output["error"]
        math = "https://api.mathjs.org/"
        desc = desc + "Precision: " + pres + "\n" + "Requested by: " + str(ctx.author) + "\n" + "Know More: " + math
        color = color = self.random_color()
        title = "Calc"
        embed = self.create_embed(title,desc,color,image="")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Math(bot))