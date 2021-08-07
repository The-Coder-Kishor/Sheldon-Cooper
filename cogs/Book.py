
from discord.ext import commands, tasks
import discord
import datetime
import random
import requests as req
from bs4 import BeautifulSoup as bs
import re


class Book(commands.Cog):
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
        if (image !=""):
            embed.set_image(url=image)
        return embed

    @commands.command(name='book')
    async def book(self, ctx, *args):
        """Returns details about books."""
        x = advertisement = ' '.join(args)
        try:
            await ctx.send("Finding the book....")
            s = x
            print(s)
            doc = req.get("https://www.goodreads.com/search?q=" + s.replace(' ','+') + "&search%5Bsource%5D=goodreads&search_type=books&tab=books")
            soup = bs(doc.text, features="html.parser")
            dd = soup.find_all("div",{"class":"mainContent"})[0].find_all("table",{"cellspacing":"0"})[0].find_all("tr")[0].find_all("a",{"class":"bookTitle"})[0]
            link = ''.join(re.findall('href="(.+)" i',str(dd)))
            print("https://www.goodreads.com"+link)
            doc = req.get("https://www.goodreads.com"+link)
            soup = bs(doc.text, features="html.parser")
            dd = soup.find_all("div",{"class":"mainContent"})[0].find_all("div",{"id":"topcol"})[0]
        except:
            print('cannot find input')
            embed = discord.Embed(colour=0xff0000, description="Error: cannot find book")
            await ctx.send(embed = embed)
            return
        
        try:
            title = dd.find_all("div",{"class":"last col"})[0].find_all("h1",{"id":"bookTitle"})[0].text.replace('\n','')
        except:
            title = x

        try:
            cover = dd.find_all("a")[0].find_all("img",{"id":"coverImage"})[0]
            coverUrl = ''.join(re.findall('src="(.+)"',str(cover)))
        except:
            coverUrl = ''

        try:
            serie = dd.find_all("div",{"class":"last col"})[0].find_all("h2")[0].find_all("a")[0].text.replace('\n','')
        except:
            serie = 'N\A'

        try:
            desc = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"description"})[0].find_all("span")[0].text
        except:
            desc = 'N\A'

        try:
            author = dd.find_all("div",{"class":"last col"})[0].find_all("a",{"class":"authorName"})[0].find_all("span",{"itemprop":"name"})[0].text
        except:
            author = 'N\A'

        try:
            rating = dd.find_all("div",{"class":"last col"})[0].find_all("span",{"itemprop":"ratingValue"})[0].text.replace('\n','')
        except:
            rating = 'N\A'


        try:
            num = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("span",{"itemprop":"numberOfPages"})[0].text
        except:
            num = 'N\A'


        try:
            pub = dd.find_all("div",{"class":"last col"})[0].find_all("div",{"id":"details"})[0].find_all("div",{"class":"row"})[1].text.replace('\n','')
        except:
            pub = 'N\A'

        color = self.random_color()
        description ="**Title :** "+title+"\n"+"**Author :** "+author+"\n"+"**Book Series :** "+serie+"\n"+"**Rating :** "+rating+"\n"+"**Published :** "+pub+"\n"+"**Number Of Pages :** "+num+"\n"+"**Book Description :** "+desc+"\n"+"https://www.goodreads.com"+link
        embed = self.create_embed(title,description,color,coverUrl)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Book(bot))