import discord
from discord.ext import commands, tasks
from itertools import cycle
from datetime import datetime

class Cool(commands.Cog):
    def __init__(self, client):
        self.client = client
        stat= f"Agreement with {len(self.client.guilds)} servers and {len([x for x in self.client.get_all_members() if not x.bot])} signatories"
        self.statuslist = cycle([
            'Pythoning',
            stat,
            'Doing stuff...',
            'Watching Big Bang Theory',
            stat,
            'Remember that I have an eidetic memory.',
            'I am Sheldon Cooper.',
            stat,
            'Trying out String Functions...',
            'The world is chaos',
            stat,
            'I have to win the Nobel',
            ])
        self.change_status.start() # start playing/changing status if bot is onlin
        """ Change the status of the bot every 10 seconds """
        
        
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.statuslist)))

def setup(client):
    client.add_cog(Cool(client))



