import asyncio, discord, os, re
from   datetime import datetime
from   discord.ext import commands
from   cogs import Utils, Message, PCPP

def setup(bot):
	# Add the bot and deps
	settings = bot.get_cog("Settings")
	bot.add_cog(Server(bot, settings))

# This module sets/gets some server info

class Server(commands.Cog):

	# Init with the bot reference, and a reference to the settings var and xp var
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings
		# Regex for extracting urls from strings
		self.regex = re.compile(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")
		global Utils, DisplayName
		Utils = self.bot.get_cog("Utils")
		DisplayName = self.bot.get_cog("DisplayName")

	async def message(self, message):
		if not type(message.channel) is discord.TextChannel:
			return { "Ignore" : False, "Delete" : False }
		# Make sure we're not already in a parts transaction
		if self.settings.getGlobalUserStat(message.author, 'HWActive'):
			return { "Ignore" : False, "Delete" : False }
		# Check if we're attempting to run the pcpp command
		the_prefix = await self.bot.command_prefix(self.bot, message)
		if message.content.startswith(the_prefix):
			# Running a command - return
			return { "Ignore" : False, "Delete" : False }
		# Check if we have a pcpartpicker link
		matches = re.finditer(self.regex, message.content)
		pcpplink = None
		for match in matches:
			if 'pcpartpicker.com' in match.group(0).lower():
				pcpplink = match.group(0)
		if not pcpplink:
			# Didn't find any
			return { "Ignore" : False, "Delete" : False }
		autopcpp = self.settings.getServerStat(message.guild, "AutoPCPP")
		if autopcpp == None:
			return { "Ignore" : False, "Delete" : False }
		ret = await PCPP.getMarkdown(pcpplink, autopcpp)
		return { "Ignore" : False, "Delete" : False, "Respond" : ret }

	@commands.command(pass_context=True)
	async def setprefix(self, ctx, *, prefix : str = None):
		"""Sets the bot's prefix (bot-admin only)."""
		if not await Utils.is_bot_admin_reply(ctx): return
		# We're admin
		if not prefix:
			self.settings.setServerStat(ctx.guild, "Prefix", None)
			msg = 'Custom server prefix *removed*.'
		elif prefix in ['@everyone','@here']:
			return await ctx.send("Yeah, that'd get annoying *reaaaal* fast.  Try another prefix.")
		else:
			self.settings.setServerStat(ctx.guild, "Prefix", prefix)
			msg = 'Custom server prefix is now: {}'.format(prefix)
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def getprefix(self, ctx):
		"""Output's the server's prefix - custom or otherwise."""
		# Get the current prefix
		prefix = await self.bot.command_prefix(self.bot, ctx.message)
		prefixlist = ", ".join([x for x in prefix if not x == "<@!{}> ".format(self.bot.user.id)])
		msg = 'Prefix{}: {}'.format("es are" if len(prefix) > 1 else " is",prefixlist)
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def setinfo(self, ctx, *, word : str = None):
		"""Sets the server info (bot-admin only)."""
		if not await Utils.is_bot_admin_reply(ctx): return
		# We're admin
		word = None if not word else word
		self.settings.setServerStat(ctx.guild,"Info",word)
		msg = "Server info *{}*.".format("updated" if word else "removed")
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def info(self, ctx):
		"""Displays the server info if any."""
		serverInfo = self.settings.getServerStat(ctx.guild, "Info")
		msg = 'I have no info on *{}* yet.'.format(ctx.guild.name)
		if serverInfo:
			msg = '*{}*:\n\n{}'.format(ctx.guild.name, serverInfo)
		await ctx.send(Utils.suppressed(ctx,msg))

	@commands.command(pass_context=True,hidden=True)
	@commands.is_owner()
	async def dumpservers(self, ctx):
		"""Dumps a timpestamped list of servers into the same directory as the bot (owner only)."""
		if not await Utils.is_owner_reply(ctx): return
		timeStamp = datetime.today().strftime("%Y-%m-%d %H.%M")
		serverFile = 'ServerList-{}.txt'.format(timeStamp)
		message = await ctx.author.send('Saving server list to *{}*...'.format(serverFile))
		msg = ''
		for server in self.bot.guilds:
			msg += server.name + "\n"
			msg += str(server.id) + "\n"
			msg += server.owner.name + "#" + str(server.owner.discriminator) + "\n\n"
			msg += str(len(server.members)) + "\n\n"
		# Trim the last 2 newlines
		msg = msg[:-2].encode("utf-8")
		with open(serverFile, "wb") as myfile:
			myfile.write(msg)
		await message.edit(content='Uploading *{}*...'.format(serverFile))
		await ctx.author.send(file=discord.File(serverFile))
		await message.edit(content='Uploaded *{}!*'.format(serverFile))
		os.remove(serverFile)