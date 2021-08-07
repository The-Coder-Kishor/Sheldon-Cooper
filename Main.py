import asyncio, discord, sys, os, random, traceback, json
from   discord.ext import commands,tasks
from datetime import datetime
from   discord import errors
from   cogs import DisplayName
from itertools import *
import os
from dotenv import load_dotenv
load_dotenv()


stat = ""

if os.path.exists("settings_dict.json"):
	try: settings_dict = json.load(open("settings_dict.json"))
	except Exception as e:
		print("Could not load settings_dict.json!")
		print(" - {}".format(e))
		# Kill the process to avoid constant reloads
		os._exit(3)
else:
	settings_dict = {"token":""}
	print("Migrating .txt files to settings_dict.json...")
	for x in ["prefix.txt","corpSiteAuth.txt","token.txt","igdbKey.txt","weather.txt","discogs.txt","currency.txt"]:
		if not os.path.exists(x): continue # Didn't find it
		try:
			with open(x,"rb") as f:
				setting = f.read().strip().decode("utf-8")
		except Exception as e:
			print("Failed to migrate setting from {}! Ignoring.".format(x))
			print(" - {}".format(e))
			continue
		settings_dict[x[:-4].lower()] = setting
	json.dump(settings_dict,open("settings_dict.json","w"),indent=4)

async def get_prefix(bot, message):
	# Check commands against some things and do stuff or whatever...
	try:
		# Set the settings var up
		settings = bot.get_cog("Settings")
		serverPrefix = settings.getServerStat(message.guild, "Prefix")
	except Exception:
		serverPrefix = None

	if not serverPrefix:
		# No custom prefix - use the default
		serverPrefix = settings_dict.get("prefix","$") # prefix
	return (serverPrefix, "<@!{}> ".format(bot.user.id), "<@{}> ".format(bot.user.id))


try:
	# Setup intents
	intents = discord.Intents().all()
	bot = commands.AutoShardedBot(command_prefix=get_prefix, pm_help=None, description='A bot that does stuff.... probably', case_insensitive=True, shard_count=4, intents=intents)
except:
	# Possibly using the old gateway?
	print("Using the old gateway - this may not be around forever...\n")
	bot = commands.AutoShardedBot(command_prefix=get_prefix, pm_help=None, description='A bot that does stuff.... probably', shard_count=4)
bot.settings_dict    = settings_dict
bot.ready_dispatched = False

async def return_message():
	# Set the settings var up
	settings = bot.get_cog("Settings")
	if not settings:
		return
	return_channel = settings.getGlobalStat("ReturnChannel",None)
	if not return_channel == None:
		message_to = bot.get_channel(return_channel)
		if message_to == None:
			# No channel
			return
		settings.delGlobalStat("ReturnChannel")
		return_options = [
			"I'm back!",
			"I have returned!",
			"Guess who's back?",
			"Fear not!  I have returned!",
			"I'm alive!"
		]
		await message_to.send(random.choice(return_options))

# Main bot events
@bot.event
async def on_ready():
	if not bot.ready_dispatched:
		print(" - {} of {} ready...".format(len(bot.shards), bot.shard_count))
		if len(bot.shards) >= bot.shard_count:
			print("\nAll shards ready!\n")
			bot.ready_dispatched = True
			bot.dispatch("all_shards_ready")

@bot.command()
async def greet(ctx):
    """Greets you"""
    await ctx.send(f'Hello {ctx.message.author.mention}!')

@bot.event
# async def on_ready():
async def on_all_shards_ready():
	if not bot.get_cog("CogManager"):
		# We need to load shiz!
		print('Logged in as:\n{0} (ID: {0.id})\n'.format(bot.user))
		print("Invite Link:\nhttps://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8\n".format(bot.user.id))
		# Let's try to use the CogManager class to load things
		print("Loading CogManager...")
		bot.load_extension("cogs.CogManager")
		cg_man = bot.get_cog("CogManager")
		# Load up the rest of the extensions
		cog_loaded, cog_count = cg_man._load_extension()
		# Output the load counts
		if cog_count == 1:
			print("Loaded {} of {} cog.".format(cog_loaded, cog_count))
		else:
			print("Loaded {} of {} cogs.".format(cog_loaded, cog_count))
	await return_message()

	
@bot.event
async def on_voice_state_update(user, beforeState, afterState):
	return

@bot.event
async def on_typing(channel, user, when):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.ontyping(channel, user, when)
		except AttributeError:
			continue

@bot.event
async def on_member_remove(member):
	server = member.guild
	# Set the settings var up
	settings = bot.get_cog("Settings")
	settings.removeUser(member, server)
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.onleave(member, server)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_member_ban(guild, member):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.onban(guild, member)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_member_unban(member, server):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.onunban(member, server)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_guild_join(server):
	didLeave = False
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			if await cog.onserverjoin(server):
				didLeave = True
		except AttributeError:
			# Onto the next
			continue
	if didLeave:
		return
	# Set the settings var up
	settings = bot.get_cog("Settings")
	owner = server.owner
	# Let's message hello in the main chat - then pm the owner
	prefixes = await get_prefix(bot,None)
	prefix = prefixes[0] if len(prefixes) else "$"
	msg = 'Hello there! Sheldon the great is here! ({})\n\nFeel free to put me to work.\n\nYou can get a list of my commands by typing `{}help` either in chat or in PM.\n\n'.format(server.name, prefix)
	msg += 'I look forward to having a wonderful Server Agreement with you Thanks!'.format(settings_dict.get("prefix","$"))
	try:
		await owner.send(msg)
	except Exception:
		pass

@bot.event
async def on_guild_remove(server):
	# Set the settings var up
	settings = bot.get_cog("Settings")
	settings.removeServer(server)

@bot.event
async def on_member_join(member):
	server = member.guild
	# Set the settings var up
	settings = bot.get_cog("Settings")

	rules = settings.getServerStat(server, "Rules")
	
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.onjoin(member, server)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_member_update(before, after):	
	# Check for cogs that accept updates
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.member_update(before, after)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_message(message):
	# Post the context too
	context = await bot.get_context(message)
	bot.dispatch("message_context", context, message)

	if not message.guild:
		# This wasn't said in a server, process commands, then return
		await bot.process_commands(message)
		return

	if message.author.bot:
		# We don't need other bots controlling things we do.
		return

	try:
		message.author.roles
	except AttributeError:
		# Not a User
		await bot.process_commands(message)
		return
	
	# Check if we need to ignore or delete the message
	# or respond or replace
	ignore, delete, react = False, False, False
	respond = None
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			check = await cog.message(message)
		except AttributeError:
			# Onto the next
			continue
		# Make sure we have things formatted right
		if not type(check) is dict:
			check = {}
		if check.get("Delete",False):
			delete = True
		if check.get("Ignore",False):
			ignore = True
		try: respond = check['Respond']
		except KeyError: pass
		try: react = check['Reaction']
		except KeyError: pass

	if delete:
		# We need to delete the message - top priority
		await message.delete()

	if not ignore:
		# We're processing commands here
		if respond:
			# We have something to say
			await message.channel.send(respond)
		if react:
			# We have something to react with
			for r in react:
				await message.add_reaction(r)
		await bot.process_commands(message)

@bot.event
async def on_command(command):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.oncommand(command)
		except AttributeError:
			# Onto the next
			continue

@bot.event
async def on_command_completion(command):
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.oncommandcompletion(command)
		except AttributeError:
			# Onto the next
			continue


async def on_command_error(
    self,
    ctx: commands.Context,
    error: commands.CommandError
):
    # Skips errors that were already handled locally.
    if getattr(ctx, 'handled', False):
        return

    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send('This command cannot be used in direct messages.')
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send('Too many arguments.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing required argument `{error.param.name}`.')
    elif (
        isinstance(error, commands.NotOwner)
        or isinstance(error, commands.MissingPermissions)
    ):
        await ctx.send(
            'You do not have the required permissions to invoke this '
            'command.'
        )
    elif (
        isinstance(error, commands.CommandOnCooldown)
        or isinstance(error, commands.CheckFailure)
    ):
        await ctx.send(error)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send(
            'This command is currently disabled and cannot be used.'
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'Bad argument: {error}')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(
            'Oops! The bot does not have the required permissions to '
            'execute this command.'
        )
        log.error(
            f'{ctx.command.qualified_name} cannot be executed because the '
            f'bot is missing the following permissions: '
            f'{", ".join(error.list)}'
        )
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send('Something went wrong internally!')
        log.error(
            f'{ctx.command.qualified_name} failed to execute. '
            f'{error.original.__class__.__name__}: {error.original}\n'
            f'{"".join(traceback.format_tb(error.original.__traceback__))}'
        )
            
@bot.event
async def on_message_delete(message):
	# Run through the on_message commands, but on deletes.
	if not message.guild:
		# This wasn't in a server, return
		return
	try:
		message.author.roles
	except AttributeError:
		# Not a User
		return
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			await cog.message_delete(message)
		except AttributeError:
			# Onto the next
			continue

		
@bot.event
async def on_message_edit(before, message):
	# Run through the on_message commands, but on edits.
	if not message.guild:
		# This wasn't said in a server, return
		return

	try:
		message.author.roles
	except AttributeError:
		# Not a User
		return
	
	# Check if we need to ignore or delete the message
	# or respond or replace
	ignore = delete = False
	respond = None
	for cog in bot.cogs:
		cog = bot.get_cog(cog)
		try:
			check = await cog.message_edit(before, message)
		except AttributeError:
			# Onto the next
			continue
		if check.get("Delete",False):
			delete = True
		if check.get("Ignore",False):
			ignore = True
		try: respond = check['Respond']
		except KeyError: pass

	if respond:
		# We have something to say
		await message.channel.send(respond)
	if delete:
		# We need to delete the message - top priority
		await message.delete()

# Run the bot
print("Starting up {} shard{}...".format(bot.shard_count,"" if bot.shard_count == 1 else "s"))
bot.run(os.getenv('TOKEN'))