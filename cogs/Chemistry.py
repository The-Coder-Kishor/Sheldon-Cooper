from discord.ext import commands, tasks
import discord
import datetime
import random
import requests as req
from bs4 import BeautifulSoup as bs
import re
from chemlib import *
import pubchempy as pcp
from balanceEquation import solve

class Chemistry(commands.Cog):
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

    @commands.command(name='compound')
    async def compound(self,ctx,n):
        """Returns the details of the compound(Please enter the formula only)"""
        try:
            await ctx.send("Calculating....")
            t = Compound(n)
            x=t.occurences
            per = ""
            for i in x:
                per = per + (str(i)+": "+str(t.percentage_by_mass(i))+"%")
                per = per + "\n"
            color = self.random_color()
            description ="**Molar mass :** "+str(t.molar_mass())+"\n"+"**Element Occurences :** "+str(t.occurences)+"\n"+"**Percentage Composition :** "+per
            image = ""
            embed = self.create_embed(n,description,color,image)
            await ctx.send(embed = embed)
        except:
            await ctx.send('Compound not found in Chemlib')

    @commands.command(name='element')
    async def element(self,ctx,*args):
        """Returns all details of the element(Please enter the symbol only)."""
        await ctx.send("Calculating....")
        x = ''.join(args)
        m = Element(x)
        name = str(m.Element)
        atn = str(m.AtomicNumber)
        symbol = str(m.Symbol)
        mass = str(m.AtomicMass)
        neutron = str(m.Neutrons)
        proton = str(m.Protons)
        electron = str(m.Electrons)
        period = str(m.Period)
        group = str(m.Group)
        state = str(m.Phase)
        radio = str(m.Radioactive)
        natural = str(m.Natural)
        metal = str(m.Metal)
        nmetal = str(m.Nonmetal)
        metalloid = str(m.Metalloid)
        type = str(m.Type)
        radius = str(m.AtomicRadius)
        en = str(m.Electronegativity)
        ion = str(m.FirstIonization)
        density = str(m.Density)
        mp = str(m.MeltingPoint)
        bp = str(m.BoilingPoint)
        iso = str(m.Isotopes)
        discov = str(m.Discoverer)
        year = str(m.Year)
        sh = str(m.SpecificHeat)
        shells = str(m.Shells)
        valence = str(m.Valence)
        config = str(m.Config)
        mn = str(m.MassNumber)
        color = self.random_color()
        coverUrl = "https://st.depositphotos.com/1000943/2157/i/450/depositphotos_21578567-stock-photo-atom.jpg"
        description ="**Element Name :** "+name+"\n"+"**Symbol :** "+symbol+"\n"+"**Atomic Number :** "+atn+"\n"+"**Mass Number :** "+mn+"\n"+"**# of neutrons :** "+neutron+"\n"+"**# of protons :** "+proton+"\n"+"**# of electrons :** "+electron+"\n"+"**Valence :** "+valence+"\n"+"**# of shells :** "+shells+"\n"+"**Electronic Config :** "+config+"\n"+"**Period :** "+period+"\n"+"**Group :** "+group+"\n"+"**# of isotopes :** "+iso+"\n"+"**Atomic Mass :** "+mass+"\n"+"**State :** "+state+"\n"+"**Radioactive :** "+radio+"\n"+"**Natural :** "+natural+"\n"+"**Metal :**"+metal+"\n"+"**Non-metal :** "+nmetal+"\n"+"**Metalloid :** "+metalloid+"\n"+"**Type :** "+type+"\n"+"**Atomic Radius :** "+radius+"\n"+"**Electronegativity :** "+en+"\n"+"**First Ionization :** "+ion+"\n"+"**Density :** "+density+"\n"+"**Melting Point :** "+mp+"\n"+"**Boiling Point :** "+bp+"\n"+"**Specific Heat :** "+sh+"\n"+"**Discoverer :** "+discov+"\n"+"**Year of Discovery :** "+year
        embed = self.create_embed(name,description,color,coverUrl)
        await ctx.send(embed = embed)

    @commands.command(name='pubchem')
    async def pubchem(self,ctx,*args):
        """Retrieves compound information from PubChem Servers"""
        try:
            await ctx.send("Calculating....")
            x = ''.join(args)
            k = pcp.get_compounds(x, 'name')
            t = str(k[0])
            l = len(t)
            m = t[9:l-1]
            c = pcp.Compound.from_cid(m)
            color = self.random_color()
            description ="**Molecular Formula :** "+str(c.molecular_formula)+"\n"+"**Molecular Weight :** "+str(c.molecular_weight)+"\n"+"**IUPAC Name :** "+str(c.iupac_name)
            image = ""
            embed = self.create_embed(x,description,color,image)
            await ctx.send(embed = embed)
        except:
            await ctx.send('Compound not found in PubChem servers')

    @commands.command(name='em')
    async def em(self,ctx,*args):
        """Gives the properties of electromagnetic wave
            Please write in the form 2e+17 for 2x10^{17} or 2e-10 for 2x10^{-10}
            The units are energy:joule, frequency:Hz and wavelength:metres
            Do not enter the units while inputting!!!
            if you enter energy=value or frequency=value or wavelenth=value for getting the properties"""
        try:
            await ctx.send("Calculating....")
            x = ''.join(args)
            if(x.startswith('energy=')):
                t= float(x[7:].strip())
                w = Wave(energy=t)
                await ctx.send(w.properties)
            elif(x.startswith('energy =')):
                t= float(x[8:].strip())
                w = Wave(energy=t)
                await ctx.send(w.properties)
            elif(x.startswith('frequency=')):
                t= float(x[10:].strip())
                w = Wave(frequency=t)
                await ctx.send(w.properties)
            elif(x.startswith('frequency =')):
                t= float(x[11:].strip())
                w = Wave(frequency=t)
                await ctx.send(w.properties)
            elif(x.startswith('wavelength=')):
                t= float(x[11:].strip())
                w = Wave(wavelength=t)
                await ctx.send(w.properties)
            elif(x.startswith('wavelength=')):
                t= float(x[12:].strip())
                w = Wave(wavelength=t)
                await ctx.send(w.properties)
            else:
                await ctx.send('Enter proper value')
        except:
            pass

    @commands.command(name='borbital')
    async def borbital(self,ctx,n):
        """Returns the energy of nth orbital in Bohr's isoelectronic species"""
        try:
            await ctx.send("Calculating....")
            x = float(n)
            await ctx.send(str(energy_of_hydrogen_orbital(x))+" Joules")
        except:
            await ctx.send('Enter a proper value')

    @commands.command(name='gal-cell')
    async def galvani(self, ctx, el1:str,el2:str):
        """Returns properties of a galvanic cell"""
        await ctx.send("Calculating....")
        g = Galvanic_Cell(el1, el2)
        await ctx.send(g.properties)

    @commands.command(name='combustion')
    async def combustion(self, ctx, com:str):
        """Returns the combustion reaction for a hydrocarbon"""
        try:
            await ctx.send("Calculating....")
            compound = Compound(com)
            c = Combustion(compound)
            await ctx.send(c.formula)
        except:
            await ctx.send('Please use sc.help <command name> to know more about the command')

    @commands.command(name='mole')
    async def mole(self, ctx, compound:str,qty:str,number:float):
        """<compound> <grams/moles/molecules> <number> returns the properties
            number if power has to be written as 6e-2 for 6x10^{2}
            e.g. H2O grams 2 will return {'Compound': 'H₂O₁', 'Grams': 2, 'Moles': 0.111, 'Molecules': 6.685e+22} """
        try:
            await ctx.send("Calculating....")
            c = Compound(compound)
            if(qty == "grams"):
                await ctx.send(c.get_amounts(grams = number))
            elif(qty == "moles"):
                await ctx.send(c.get_amounts(moles = number))
            elif(qty == "molecules"):
                await ctx.send(c.get_amounts(molecules = number))
            else:
                await ctx.send('Please give a proper command')
        except:
            await ctx.send('Please use sc.help <command name> to know more about the command')

    @commands.command(name='balance')
    async def bal(self, ctx, *args):
        """Enter the equation in the form A<space>+<space>B<space>=><space>C<space>+<space>D
        	not redox!!"""
        try:
            await ctx.send("Calculating....")
            k = ' '.join(args)
            await ctx.send(solve(k))
        except:
            await ctx.send('Please use sc.help <command name> to know more about the command')

def setup(bot):
    bot.add_cog(Chemistry(bot))