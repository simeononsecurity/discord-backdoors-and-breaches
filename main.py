import discord
import random
import config
import datetime
from discord import Activity, ActivityType, Status, app_commands
from discord.ext import commands, tasks
import os
import copy

from typing import Literal, Union, NamedTuple, List
from enum import Enum

#import card dictionaries
import cards.procedures as proceduresData
import cards.initial_compromise as incident_masterData
import cards.c2_and_exfil as c2Data
import cards.persistence as persistenceData
import cards.injects as injectsData
import cards.pivot_and_escalate as pivot_and_escalateData

import time

import traceback

#tracemalloc
import tracemalloc
tracemalloc.start()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", "/"], intents=intents)

first_start = True

games = {}
players = {}
procedures = {}
incident_master = {}
played_cards = {}
incident_master_names = {}
pivot_played = {}
c2_played = {}
persistence_played = {}
inital_played = {}
turn = {}
hands = {}
cooldowns = {}
card_modifiers = {}
failed_rolls = {}
game_ended = {}

c2_and_exfil = {}
persistence = {}
injects = {}
pivot_and_escalate = {}

incident_master_card = {}
c2_and_exfil_card = {}
persistence_card = {}
pivot_and_escalate_card = {}

'''
def shuffle_deck():
	"""Shuffles the incident master deck and procedure deck."""
	random.shuffle(incident_master_deck)
	random.shuffle(procedure_deck)
'''


def roll_die():
	return random.randint(1, 20)

def find_game_id(user_id):
	global players
	
	user_id = int(user_id)
	game_id = None
	
	for game_id in players:
		for player in players[game_id]:
			if player.id == user_id:
				return game_id
			
	return game_id
		
		
@bot.hybrid_command(name="setup-game", description="Sets up a new game, the person who runs this will become incident master.")
async def setup_game(ctx):
	global turn, players, procedures, incident_master, incident_master_names, c2_and_exfil, persistence, injects, pivot_and_escalate, incident_master_card, game_ended, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card, inital_played
	await ctx.defer()
	
	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")
	
	game_id = find_game_id(ctx.author.id)
	if game_id:
		return await ctx.reply(f"You are already in game id {str(game_id)}.")
	
	game_id = str(int(time.time())) #Will enable some sorting
	games[game_id] = {}
	
	players[game_id] = []
	procedures[game_id] = []
	incident_master[game_id] = []
	played_cards[game_id] = []
	incident_master_names[game_id] = []
	pivot_played[game_id] = []
	c2_played[game_id] = []
	persistence_played[game_id] = []
	inital_played[game_id] = []
	turn[game_id] = 0
	hands[game_id] = {}
	cooldowns[game_id] = {}
	card_modifiers[game_id] = {}
	failed_rolls[game_id] = 0
	game_ended[game_id] = True
	
	procedures[game_id] = copy.deepcopy(proceduresData.Procedures)
	incident_master[game_id] = copy.deepcopy(incident_masterData.initial_compromise)
	c2_and_exfil[game_id] = copy.deepcopy(c2Data.C2)
	persistence[game_id] = copy.deepcopy(persistenceData.Persistence)
	injects[game_id] = copy.deepcopy(injectsData.Injects)
	pivot_and_escalate[game_id] = copy.deepcopy(pivot_and_escalateData.pivot_and_escalate)
	
	if ctx.author not in players[game_id]:
		players[game_id].append(ctx.author)
	
	await ctx.reply(
		embed=discord.Embed(title="Backdoors and Breaches",description=f"Game with id {str(game_id)} set up, use /join-game {str(game_id)} to join."
	))
	
@bot.hybrid_command(name="start-game", description="Begins a game, sets up channel, roles, permissions.")
async def start_game(ctx):
	global players, procedures, incident_master, incident_master_names, c2_and_exfil, persistence, injects, pivot_and_escalate, incident_master_card, game_ended, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card, inital_played
	
	await ctx.defer()
	
	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if not players[game_id][0] == ctx.author:
		return await ctx.reply("Only incident master can use this command.")
	
	if not game_ended[game_id]:
		return await ctx.reply("Game already started.")
		
	game_ended[game_id] = False

	# Shuffle procedures and incident master decks
	random.shuffle(procedures[game_id])
	random.shuffle(incident_master[game_id])

	random.shuffle(c2_and_exfil[game_id])
	random.shuffle(persistence[game_id])
	random.shuffle(injects[game_id])
	random.shuffle(pivot_and_escalate[game_id])

	incident_master_names[game_id] = [card["Title"] for card in incident_master[game_id]]
	master_cards_to_send = ""
	
	# Deal cards to players
	for i, player in enumerate(players[game_id]):
		hand = []
		if i != 0:
			for i in range(0, 4):
				hand.append(procedures[game_id].pop(0))
			hands[game_id][player.id] = hand
			
			
			try: #Try and dm hand but skip if cant dm
				await player.send(embed=discord.Embed(title="Backdoors and Breaches",description="Your hand:\n {}".format('\n\n'.join([format_card_info(card) for card in hand]))))
			except:
				pass
			
			await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description="{} hand:\n {}".format(player.mention,'\n\n'.join([format_card_info(card) for card in hand]))))

		# injects_card = injects.pop(0)
		# await player.send(f"Injects card: {injects_card['Title']}")

		if i == 0:
			cards_to_send = "\n\n"
			incident_master_card[game_id] = incident_master[game_id].pop(0)
			inital_played[game_id].append(incident_master_card[game_id])
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"Incident Master card: {incident_master_card['Title']}"))
			cards_to_send = cards_to_send + "Incident Master card:\n"+format_card_info(incident_master_card[game_id])+"\n"
			c2_and_exfil_card[game_id] = c2_and_exfil[game_id].pop(0)
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"C2 and Exfil card: {c2_and_exfil_card['Title']}"))
			cards_to_send = cards_to_send + "C2 and Exfil card:\n"+format_card_info(c2_and_exfil_card[game_id])+"\n"
			persistence_card[game_id] = persistence[game_id].pop(0)
			cards_to_send = cards_to_send + "Persistence card:\n"+format_card_info(persistence_card[game_id])+"\n"
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"Persistence card: {persistence_card['Title']}"))
			pivot_and_escalate_card[game_id] = pivot_and_escalate[game_id].pop(0)
			cards_to_send = cards_to_send + "Pivot and Escalate card:\n"+format_card_info(pivot_and_escalate_card[game_id])+"\n"
			try:
				await player.send(
					embed=discord.Embed(title="Backdoors and Breaches",description=f"Your hand: {cards_to_send}"
				))
			except:
				pass
			master_cards_to_send = cards_to_send

	# Start the first player's turn
	await ctx.send(
		embed=discord.Embed(title="Backdoors and Breaches",description=f"Starting Backdoors and Breaches game with {len(players[game_id])} players... {players[game_id][0].mention}'s turn"
	))

	await ctx.send(
		embed=discord.Embed(title="Backdoors and Breaches",description="Remaining procedures cards:\n\n {}".format('\n\n'.join([format_card_info(card) for card in procedures[game_id]]))
	))
	
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description=f"Your hand: {master_cards_to_send}"),ephemeral=True)

async def get_joinable_games(interaction: discord.Interaction, games: str) -> List[app_commands.Choice[str]]:
	global players
	
	return [app_commands.Choice(name=str(game), value=str(game)) for game in players]


@bot.hybrid_command(name="join-game", description="Lets players join by assigning roles, channel access.")
@app_commands.autocomplete(game_id=get_joinable_games)
async def join_game(ctx,game_id):
	global players
	
	if not game_id in players:
		return await ctx.reply("Invalid game id.")
	
	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")

	if ctx.author not in players[game_id]:
		players[game_id].append(ctx.author)
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description=
			f"{ctx.author.mention} has joined the game! {len(players[game_id])} players are now playing."
		))
	else:
		await ctx.reply(f"{ctx.author.mention} is already in the game!")

async def valid_cards_procedures(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global procedures
	global hands
	global players
	
	game_id = find_game_id(interaction.user.id)
	if not game_id:
		print("Not in a game")
		return []
	
	#player_index = players[game_id].index(interaction.user)
	#if player_index == 0:
		#return []
	
	hand = []
	validCards = []
	if interaction.user.id in hands[game_id]:
		hand = hands[game_id][interaction.user.id]
	validCards = procedures[game_id] + hand
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_c2(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global c2_and_exfil_card
	global players
	
	game_id = find_game_id(interaction.user.id)
	if not game_id:
		print("Not in a game")
		return []
	
	player_index = players[game_id].index(interaction.user)
	if player_index != 0:
		return []
	
	validCards = [c2_and_exfil_card[game_id]]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_persistence(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global persistence_card
	global players
	
	game_id = find_game_id(interaction.user.id)
	if not game_id:
		print("Not in a game")
		return []
	
	player_index = players[game_id].index(interaction.user)
	if player_index != 0:
		return []
	
	validCards = [persistence_card[game_id]]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_pivot(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global pivot_and_escalate_card
	global players
	
	game_id = find_game_id(interaction.user.id)
	if not game_id:
		print("Not in a game")
		return []
	
	player_index = players[game_id].index(interaction.user)
	if player_index != 0:
		return []
	
	validCards = [pivot_and_escalate_card[game_id]]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

def format_card_info(card):
	
	cardInfo = "**"+card["Title"]+"**\n\n```"+card["Description"]+"```"
	
	return cardInfo

def handle_extra_modifiers(card,game_id):
	global card_modifiers
	if card["Title"] in card_modifiers[game_id]:
		modifier = modifier + card_modifiers[game_id][card["Title"]]
	
	modifier = 0
	return modifier

async def handle_injects(ctx,card,game_id):
	global pivot_and_escalate_card
	global card_modifiers
	global procedures
	
	if card["Title"] == "HONEYPOTS DEPLOYED":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(pivot_and_escalate_card[game_id])))
		
	elif card["Title"] == "IT WAS A PENTEST":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		#await end_game(ctx)
		
	elif card["Title"] == "MANAGEMENT HAS JUST APPROVED THE RELEASE OF A NEW PROCEDURE":
		card_modifiers["WHAT_CARDS_SHOULD_THIS_AFFECT?"] = 3 #Add the valid cards
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		
	elif card["Title"] == "DATA UPLOADED TO PASTEBIN":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
	
	elif card["Title"] == "SIEM ANALYST RETURNS FROM SPLUNK TRAINING":
		card_modifiers["WHAT_CARDS_SHOULD_THIS_AFFECT?"] = 2 #Add the valid cards
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))	
		
	elif card["Title"] == "GIVE THE DEFENDERS A RANDOM PROCEDURE CARD":
		#Should this play a card directly? Or add cards for them to pick later? Add from where, played cards? Duplicate an existing procedure?
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
	
	elif card["Title"] == "LEAD HANDLER HAS A BABY, TAKES FMLA LEAVE":
		#Should it randomly kick one player from the game? Or should each player have a role?
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
	
	elif card["Title"] == "BOBBY THE INTERN KILLS THE SYSTEM YOU ARE REVIEWING":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
	
	elif card["Title"] == "LEGAL TAKES YOUR ONLY SKILLED HANDLER INTO A MEETING TO EXPLAIN THE INCIDENT":
		#Should it randomly kick one player from the game? Or should each player have a role?
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
	
	elif card["Title"] == "TAKE ONE PROCEDURE CARD AWAY":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		card_removed = procedures[game_id].pop()
	
@bot.hybrid_command(name="play-procedure", description="Starts Procedure phase, complete challenges.")
@app_commands.autocomplete(card_name=valid_cards_procedures)
async def play_procedure(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, hands, pivot_played, c2_played, persistence_played, procedures, cooldowns, inital_played, failed_rolls
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if game_ended[game_id]:
		return await ctx.reply("No game running")

	player = ctx.author
	if player != players[game_id][turn[game_id]]:
		await ctx.reply("It's not your turn!")
		return

	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")

	# Find the current player's hand and incident master card
	player_index = players[game_id].index(player)

	# Find the card to play and remove it from the player's hand or procedures
	modifier = 0
	playerCard = False
	for cardToTurn in cooldowns[game_id].copy():
		if (cooldowns[game_id][cardToTurn] + 3) < turn[game_id]:
			del cooldowns[game_id][cardToTurn]
	if card_name in cooldowns[game_id]:
		return await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card is on cooldown!"))

	try:
		card_index = [card["Title"] for card in hands[game_id][ctx.message.author.id]].index(
			card_name
		)
		card = hands[game_id][ctx.message.author.id].pop(card_index)
		modifier = 3
		await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=
			"Your hand:\n {}".format(',\n'.join([card['Title'] for card in hands[game_id][ctx.message.author.id]]))
		))
	except:
		#print(traceback.format_exc())
		try:
			card_index = [card["Title"] for card in procedures[game_id]].index(card_name)
			card = procedures[game_id].pop(card_index)
			modifier = 0
			await ctx.send(
				embed=discord.Embed(title="Backdoors and Breaches",description="Remaining procedures:\n {}".format(',\n'.join([card['Title'] for card in procedures[game_id]]))
			))
		except:
			#print(traceback.format_exc())
			await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
			return

	await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=player.mention + " Plays card:\n\n" + format_card_info(card)))
	dice_roll_orginal = roll_die()
	dice_roll = dice_roll_orginal + (modifier+handle_extra_modifiers(card,game_id))
	print("Dice rolled: "+str(dice_roll_orginal)+" Modifier: "+str(modifier))
	await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description="Dice rolled: "+str(dice_roll_orginal)+" Modifier: "+str(modifier)))
	if (dice_roll) > 10:
		fail = True
		for pivot_card in pivot_played[game_id]:
			if card["Title"] in pivot_card["Detection"]:
				pivot_played[game_id].remove(pivot_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Pivot: " + pivot_card["Title"]))
				fail = False

		for c2_card in c2_played[game_id]:
			if card["Title"] in c2_card["Detection"]:
				c2_played[game_id].remove(c2_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="C2: " + c2_card["Title"]))
				fail = False

		for persistence_card in persistence_played[game_id]:
			if card["Title"] in persistence_card["Detection"]:
				persistence_played[game_id].remove(persistence_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Persistence: " + persistence_card["Title"]))
				fail = False

		for master_card in inital_played[game_id]:
			if card["Title"] in master_card["Detection"]:
				inital_played[game_id].remove(master_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Initial Incident was: " + master_card["Title"]))
				fail = False

		if card["Title"] in incident_master_card[game_id]["Detection"]:
			await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Initial Incident was: " + incident_master_card[game_id]["Title"]))
			fail = False

		if fail:
			cooldowns[game_id][card["Title"]] = turn[game_id]
			await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Procedure had no effect"))

	else:
		failed_rolls[game_id] = failed_rolls[game_id] + 1
		cooldowns[game_id][card["Title"]] = turn[game_id]
		print("Procedure failed")
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Procedure failed"))

	if dice_roll == 1:
		injects_card = injects[game_id].pop(0)
		await handle_injects(ctx,injects_card)
	elif failed_rolls[game_id] > 2:
		failed_rolls[game_id] = 0
		injects_card = injects[game_id].pop(0)
		await handle_injects(ctx,injects_card)

	if len(persistence_played[game_id]) == 0:
		if len(c2_played[game_id]) == 0:
			if len(pivot_played[game_id]) == 0:
				if len(inital_played[game_id]) == 0:
					game_ended[game_id] = True

	# Check if the game has ended
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	if turn[game_id] > 10:
		game_ended[game_id] = True

	if game_ended[game_id]:
		await end_game(ctx,game_id)
		return

'''
@bot.hybrid_command(name="play-incident-master", description="Starts Incident Master phase, respond to simulated incidents.")
async def play_incident_master(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card

	if game_ended:
		return await ctx.reply("No game running")

	# Find the current player's index
	player_index = players.index(ctx.author)

	if player_index != 0:
		return await ctx.reply("You are not incident master")

	# Check that the player sent a valid command to play an incident master card
	if ctx.author != players[turn]:
		await ctx.reply("It's not your turn!")
		return

	if not (card_name in incident_master_names):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = incident_master_card
	# await ctx.send(f"{ctx.author.mention} played {card['Title']} as the Incident Master card.")

	# c2_played.append(card)
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Cmd should not be used?"))
'''

@bot.hybrid_command(name="play-c2", description="Starts Command and Control phase, complete tasks.")
@app_commands.autocomplete(card_name=valid_cards_c2)
async def play_c2(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, c2_played
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if game_ended[game_id]:
		return await ctx.reply("No game running")

	# Find the current player's index
	player_index = players[game_id].index(ctx.author)

	if player_index != 0:
		return await ctx.reply("You are not incident master")

	# Check that the player sent a valid command to play an incident master card
	if ctx.author != players[game_id][turn[game_id]]:
		await ctx.reply("It's not your turn!")
		return

	if not (card_name == c2_and_exfil_card[game_id]["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = c2_and_exfil_card[game_id]
	c2_played[game_id].append(card)
	
	# Check if the game has ended
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	if turn[game_id] > 10:
		game_ended[game_id] = True

	if game_ended[game_id]:
		await end_game(ctx,game_id)
		return
	
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))

@bot.hybrid_command(name="pass", description="Passes a turn, do nothing")
async def pass_turn(ctx):
	global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, c2_played
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if game_ended[game_id]:
		return await ctx.reply("No game running")

	# Find the current player's index
	player_index = players[game_id].index(ctx.author)

	##if player_index != 0:
		#return await ctx.reply("You are not incident master")

	# Check that the player sent a valid command to pass a turn
	if ctx.author != players[game_id][turn[game_id]]:
		await ctx.reply("It's not your turn!")
		return
	
	# Check if the game has ended
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	if turn[game_id] > 10:
		game_ended[game_id] = True

	if game_ended[game_id]:
		await end_game(ctx,game_id)
		return
	
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Turn passed"))

@bot.hybrid_command(name="play-persistence", description="Starts Persistence phase, eliminate hidden backdoor.")
@app_commands.autocomplete(card_name=valid_cards_persistence)
async def play_persistence(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, persistence_card, persistence_played
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if game_ended[game_id]:
		return await ctx.reply("No game running")

	# Find the current player's index
	player_index = players[game_id].index(ctx.author)

	if player_index != 0:
		return await ctx.reply("You are not incident master")

	# Check that the player sent a valid command to play an incident master card
	if ctx.author != players[game_id][turn[game_id]]:
		await ctx.reply("It's not your turn!")
		return

	if not (card_name == persistence_card[game_id]["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = persistence_card[game_id]
	persistence_played[game_id].append(card)
	
	# Check if the game has ended
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	if turn[game_id] > 10:
		game_ended[game_id] = True

	if game_ended[game_id]:
		await end_game(ctx,game_id)
		return
	
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))


@bot.hybrid_command(name="play-pivot", description="Starts Pivot phase, pivot to different part of system")
@app_commands.autocomplete(card_name=valid_cards_pivot)
async def play_pivot_and_escalate(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, pivot_and_escalate_card, pivot_played
	
	game_id = find_game_id(ctx.author.id)
	if not game_id:
		return await ctx.reply("You are not in a game.")
	
	if game_ended[game_id]:
		return await ctx.reply("No game running")

	# Find the current player's index
	player_index = players[game_id].index(ctx.author)

	if player_index != 0:
		return await ctx.reply("You are not incident master")

	# Check that the player sent a valid command to play an incident master card
	if ctx.author != players[game_id][turn[game_id]]:
		await ctx.reply("It's not your turn!")
		return

	if not (card_name == pivot_and_escalate_card[game_id]["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = pivot_and_escalate_card[game_id]
	pivot_played[game_id].append(card)
	
	# Check if the game has ended
	turn[game_id] = (turn[game_id] + 1) % len(players[game_id])
	if turn[game_id] > 10:
		game_ended[game_id] = True

	if game_ended[game_id]:
		await end_game(ctx,game_id)
		return
	
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))


@bot.hybrid_command(name="end-game", description="Ends game, deletes channel and associated roles.")
async def end_game(ctx,game_id=None):
	global players
	global procedures
	global incident_master
	global scores
	global played_cards
	global incident_master_names
	global game_ended
	global hands
	global pivot_played
	global c2_played
	global persistence_played
	global inital_played
	global failed_rolls
	global card_modifiers
	global games
	
	global incident_master_card
	global c2_and_exfil_card
	global persistence_card
	global pivot_and_escalate_card
	
	if ctx:
		if game_id is None:
			game_id = find_game_id(ctx.author.id)
			if not game_id:
				return await ctx.reply("You are not in a game.")
	
	if not game_id in players:
		if ctx:
			return await ctx.reply("Invalid game id.")
	
	if ctx:
		if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
			if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
				return await ctx.reply("This command can only be used in the designated game channel.")
	
	if ctx:
		if not players[game_id][0] == ctx.author:
			return await ctx.reply("Only incident master can use this command.")
	
	print(f"Ending game {str(game_id)} manually")
	
	try:
		del game_ended[game_id]
	except:
		pass
	
	# Reset game variables
	try:
		del players[game_id]
	except:
		pass
	
	try:
		del procedures[game_id]
	except:
		pass
	
	try:
		del incident_master[game_id]
	except:
		pass
	
	try:
		del played_cards[game_id]
	except:
		pass
	
	try:
		del incident_master_names[game_id]
	except:
		pass
	
	try:
		del turn[game_id]
	except:
		pass
	
	try:
		del hands[game_id]
	except:
		pass
	
	try:
		del pivot_played[game_id]
	except:
		pass
	
	try:
		del c2_played[game_id]
	except:
		pass
	
	try:
		del persistence_played[game_id]
	except:
		pass
	
	try:
		del inital_played[game_id]
	except:
		pass
	
	try:
		del cooldowns[game_id]
	except:
		pass
	
	try:
		del card_modifiers[game_id]
	except:
		pass
	
	try:
		del failed_rolls[game_id]
	except:
		pass
	
	try:
		del c2_and_exfil[game_id]
	except:
		pass
	try:	
		del persistence[game_id]
	except:
		pass
	try:
		del injects[game_id]
	except:
		pass
	try:
		del pivot_and_escalate[game_id]
	except:
		pass
	try:
		del incident_master_card[game_id]
	except:
		pass
	try:
		del c2_and_exfil_card[game_id]
	except:
		pass
	try:
		del persistence_card[game_id]
	except:
		pass
	try:
		del pivot_and_escalate_card[game_id]
	except:
		pass
	
	if ctx:
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Game ended"))

@bot.hybrid_command(name="bnbhelp", description="Describes the available commands.")
async def bnbhelp(ctx):
	try:
		response = """## Available Commands

- `setup-game`: Creates a game id and sets all the needed variables.
- `start-game`: Starts a new game should be run my incident master only after `setup-game`
- `join-game`: Allows players to join the game by assigning them the "Player" role and granting them access to the game channel.
- `play-procedure`: Starts the Procedure phase of the game, where players must complete a series of challenges to progress.
- `play-incident-master`: Starts the Incident Master phase of the game, where players take turns being the Incident Master and directing the other players on how to respond to a simulated incident.
- `play-c2`: Starts the Command and Control phase of the game, where players take turns being the C2 team and must coordinate with the other players to complete a series of tasks.
- `play-persistence`: Starts the Persistence phase of the game, where players must find and eliminate a hidden backdoor in the system.
- `play-pivot`: Starts the Pivot phase of the game, where players must pivot to a different part of the system and continue their investigation.
- `end-game`: Ends the current game and deletes the game channel and associated roles.

To run a command, type `!` or `/` followed by the command name in the game channel. For example, to start a new game, type `!start-game`. Note that some commands may only be available during certain phases of the game."""
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description=response))
	except Exception as e:
		await ctx.reply(f"Error: {e}. An unexpected error occurred.")

@tasks.loop(seconds=3600.0)
async def check_games():
	global players
	print("Starting check games task")
	
	now = int(time.time())
	for game_id in players:
		if (int(now)) > (int(game_id)+86400):
			print(f"Ending game {str(game_id)} automatically")
			await end_game(None,game_id)
	
@bot.event
async def on_ready():
	global first_start
	
	print("\nLogged in as:")
	print(" Username", bot.user.name)
	print(" User ID", bot.user.id)
	print(
		"To invite the bot in your server use this link:\n https://discord.com/api/oauth2/authorize?client_id="
		+ str(bot.user.id)
		+ "&permissions=8&scope=bot%20applications.commands"
	)
	print("Time now", str(datetime.datetime.now()))
	
	# on_ready event can fire more than once
	if first_start:
		try:
			synced = await bot.tree.sync()
			print(f"Synced {len(synced)} command(s)")
		except Exception as e:
			print(e)
		
		await check_games.start()
		first_start = False

bot.run(config.discordtoken)
