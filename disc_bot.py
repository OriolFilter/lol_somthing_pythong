#!/usr/bin/env python
# -*- coding: utf-8 -*-
import discord
import random
import cassiopeia as cass
from credentials import *
from cassiopeia import Summoner
from discord.ext import commands
from discord.utils import get


description = '''Big boi is here boys'''

bot = commands.Bot(command_prefix=",", description=description)

##Variables
where_i_im="/var/git/lol_somthing/" #where is the file/folder of this python document...
user_folder=where_i_im+"users/"
blacklist_folder=user_folder+"blacklist/"
summonerlist_folder=user_folder+"summonerlist/"

#Config_start
cass.set_riot_api_key(key)  # This overrides the value set in your configuration/settings.
cass.set_default_region("EUW") #Regio per defecte
#Config_end

##Definitions

client = discord.Client()

##Commands

@bot.event
async def on_ready():
	print('Logged as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
#	await statuslisten()

##Test_commands

@bot.command() #0
async def hello(ctx):
	global playerdir
	await ctx.send('Hello world') #T


@bot.command(pass_context=True)
async def test(ctx, user: discord.User):
	await ctx.send("JAJAJAJAJAJA")
	await ctx.send("@"+str(ctx.author.id))
	await ctx.send(str(user.name))
	await ctx.send(user.mention)
	await ctx.send("ABC: "+str(client.get_user(ctx.author.id)))
	await ctx.send("ABC: "+str(client.get_user(ctx.author.id)))
#	await ctx.send("ABC: "+client.user.name(ctx.author.id))
#    print(message.author.id)

@bot.command(pass_context=True)
async def tests(ctx, user: discord.user):
	await ctx.send(str(discord.User.id))
	await ctx.send(str(discord.User.name))
	await ctx.send(str(discord.User.nicks))
	if not user:
		await ctx.send("Try using an argument. For example: !test yes")
	elif user[0] == "yes":
		await ctx.send("This is a valid argument!")
	else:
		await ctx.send("Not a valid argument!")


def on_message(message):
	print(message.author.id)

###########################################################################

###########################################################################

##list_commands

@bot.command(pass_context=True)
async def list(ctx, user: discord.User = None):
	"""use 'list' to check your list, or use 'list @somone' to see his list"""
	if user is None:	#if not user:
		id=(str(ctx.author.id))
	else:
		id=(str(user.id))
	try:
		summoner_list_file_r = open(summonerlist_folder+id, "r")
		print(summonerlist_folder+id)
		file_readed = str(summoner_list_file_r.read().splitlines())
		if not file_readed :
			await ctx.send("The user does not have a list, start by adding a summoner name!")
		else:
			await ctx.send(user.mention+"'s summoner list: "+file_readed)
	except AttributeError:
		await ctx.send ("The user does not have a list, start by adding a summoner name!")
	except FileNotFoundError:
		await ctx.send ("The user does not have a list, start by adding a summoner name!")

	summoner_list_file_r.close()

def add_list(discord_user_id):
	summoner_list_file_a = open(summonerlist_folder+discord_user_id, "a")
	summoner_list_file_r = open(summonerlist_folder+discord_user_id, "r")
	file_readed = summoner_list_file_r.read().splitlines()
	summ_name = input("Introduce the name of the summoner that you want to add to your summoner list\n").lower()
	##CHECK IF EXISTS
	print("Checking if the summoner is alredy in")

	exist=False
	#		while line in file_readed or not exist: #pendent
	for line in file_readed:
		print(line)
		if line == summ_name:
			exist=True
	if not exist:
		summoner_list_file_a.write(summ_name+"\n")
		print ("Added "+summ_name+" to the summoner list")
	else:
		print ("This summoner name is alredy in")

	summoner_list_file_r.close()
	summoner_list_file_a.close()

def get_summoner(summoner_input):
	#summoner = Summoner(name=summoner_input)
	summoner = cass.get_summoner(name=summoner_input)
	return(summoner)



@bot.command()
async def rankeu(ctx, arg1):
	"""use 'rankeu *account*' to check the elo from this account (in the EWU server)"""
	summoner = get_summoner(arg1)

	entries = summoner.league_entries
	user_rank = ""
	for entry in entries:
		if user_rank == "":
			user_rank = get_queue_rank(ctx,entry)
		else:
			user_rank = user_rank+"\n"+get_queue_rank(ctx,entry)
	if user_rank != "" : #CHECK_if_empty
		await ctx.send ("\nQueue Name\tTier\t\tDivision\tlp\tLeague Name\n-----------------------------------------------------------------------------------\n"+user_rank) #FORMATAT COLUMNES
	else:
		await ctx.send ("Player it's not currentlly ranked")##debugg

@bot.command()
async def blacklist(ctx):
	await ctx.send("Coming soon")

@bot.command(pass_context=True)
async def mastery(ctx,arg1,arg2,arg3):
	#"""syntax: ',mastery summoner_name comparative_argument number' where summoner_name it's a summoner name, comparative_argument it's one of this options {== (equal),< (smaller than), > (bigger than), >= bigger (than or equal), <= (smaller than or equal)}"""
	"""usage: ',mastery summoner_name '>/</>=/<=/==/!=' number' where summoner_name it's a summoner name, comparative_argument it's one of this options {== (equal),< (smaller than), > (bigger than), >= bigger (than or equal), <= (smaller than or equal)}"""
	mastery_level = arg3
	print(arg1,arg2,arg3)
	if arg3 is None:
		await ctx.send("Please revise your input and try again")
	#elif arg2 == "==":
	#elif arg2 is not '>' or '>=' or '==' or '<' or '<=' or '!=':
	#	await ctx.send("Please revise your comparative argument, type ,help to check the options")
	else:
		summoner = get_summoner(arg1)
		comparative_argument = arg2
		good_with =eval ("summoner.champion_masteries.filter(lambda cm: cm.level {arg} {mastery_level})".format(arg=arg2,
																												mastery_level=arg3))  #get the info
		#good_with = eval ("summoner.champion_masteries.filter(lambda cm: cm.level {arg} arg3)".format(arg=arg1))
		#																										mastery_level=mastery_level))  #get the info
		text = arg1 +" "+arg2+" "+arg3+"\n"
		text = text +"```"+str([cm.champion.name for cm in good_with])+"``` "+arg2+arg3
		print(text)
		await ctx.send(text)

#GET_QUEUE_NAME
def get_queue_rank(ctx,entry):
	if ("SOLO" in str([entry.queue])):	##podria fer una variable que emmagatzemes el format
		queue_name = "Solo/Duo 5v5"
	elif ("flex" in str([entry.queue])):
		queue_name = "Flex 5v5"
	else:
		queue_name = "NotDetectedQueue"

	#Formating/check_tier
	if (str(entry.tier) == "Diamond"):
		f_tier=str(entry.tier)+"\t"
	elif (str(entry.tier) == "Platinum") or (str(entry.tier) == "Challenger") or (str(entry.tier) == "Grandmaster"):
		f_tier=str(entry.tier)
	else:
		f_tier=str(entry.tier)+"\t"

	queue_values = queue_name+"\t"+f_tier+"\t"+str(entry.division)+"\t\t"+str(entry.league_points)+"\t"+str(entry.league.name)
	return(queue_values)

#Mastery


#def summoner_info(summoner):
#	summ_info = "Summoner:\t{name}\nLevel:\t\t{level}\nRegion:\t\t{region}".format(name=summoner.name,
#																				   level=summoner.level,
#																				   region=summoner.region)
#	await ctx.send(summ_info)

### EXTRA ###
@bot.command()
async def ching(ctx, text:str):
	"""call me .ching chong"""
	if text=="chong":
		await ctx.send("Your champion is wrong!")


bot.run(TOKEN)