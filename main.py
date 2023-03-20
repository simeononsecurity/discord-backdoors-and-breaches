import discord
import random
import config
import datetime
from discord import Activity, ActivityType, Status, app_commands
from discord.ext import commands, tasks

from typing import Literal, Union, NamedTuple, List
from enum import Enum

#import card dictionaries
import cards.procedures as proceduresData
import cards.initial_compromise as incident_masterData
import cards.c2_and_exfil as c2Data
import cards.persistence as persistenceData
import cards.injects as injectsData
import cards.pivot_and_escalate as pivot_and_escalateData

#tracemalloc
import tracemalloc
tracemalloc.start()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", "/"], intents=intents)

players = []
procedures = []
incident_master = []
played_cards = []
incident_master_names = []
pivot_played = []
c2_played = []
persistence_played = []
inital_played = []
turn = 0
hands = {}
cooldowns = {}
card_modifiers = {}
failed_rolls = 0

procedures = proceduresData.Procedures
incident_master = incident_masterData.initial_compromise
c2_and_exfil = c2Data.C2
persistence = persistenceData.Persistence
injects = injectsData.Injects
pivot_and_escalate = pivot_and_escalateData.pivot_and_escalate

'''
def shuffle_deck():
	"""Shuffles the incident master deck and procedure deck."""
	random.shuffle(incident_master_deck)
	random.shuffle(procedure_deck)
'''

game_ended = True


def roll_die():
	return random.randint(1, 20)


@bot.hybrid_command(name="start-game", description="Begins a game, sets up channel, roles, permissions.")
async def start_game(ctx):
	global players, procedures, incident_master, incident_master_names, c2_and_exfil, persistence, injects, pivot_and_escalate, incident_master_card, game_ended, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card, inital_played
	
	await ctx.defer()
	
	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")
		
	if ctx.author not in players:
		players.append(ctx.author)

	game_ended = False

	# Shuffle procedures and incident master decks
	random.shuffle(procedures)
	random.shuffle(incident_master)

	random.shuffle(c2_and_exfil)
	random.shuffle(persistence)
	random.shuffle(injects)
	random.shuffle(pivot_and_escalate)

	incident_master_names = [card["Title"] for card in incident_master]

	# Deal cards to players
	for i, player in enumerate(players):
		hand = []
		if i != 0:
			for i in range(0, 4):
				hand.append(procedures.pop(0))
			hands[player.id] = hand
			await player.send(embed=discord.Embed(title="Backdoors and Breaches",description="Your hand:\n {}".format('\n\n'.join([format_card_info(card) for card in hand]))))
			await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description="{} hand:\n {}".format(ctx.author.mention,'\n\n'.join([format_card_info(card) for card in hand]))))

		# injects_card = injects.pop(0)
		# await player.send(f"Injects card: {injects_card['Title']}")

		if i == 0:
			cards_to_send = "\n\n"
			incident_master_card = incident_master.pop(0)
			inital_played.append(incident_master_card)
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"Incident Master card: {incident_master_card['Title']}"))
			cards_to_send = cards_to_send + "Incident Master card:\n"+format_card_info(incident_master_card)+"\n"
			c2_and_exfil_card = c2_and_exfil.pop(0)
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"C2 and Exfil card: {c2_and_exfil_card['Title']}"))
			cards_to_send = cards_to_send + "C2 and Exfil card:\n"+format_card_info(c2_and_exfil_card)+"\n"
			persistence_card = persistence.pop(0)
			cards_to_send = cards_to_send + "Persistence card:\n"+format_card_info(persistence_card)+"\n"
			#await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=f"Persistence card: {persistence_card['Title']}"))
			pivot_and_escalate_card = pivot_and_escalate.pop(0)
			cards_to_send = cards_to_send + "Pivot and Escalate card:\n"+format_card_info(pivot_and_escalate_card)+"\n"
			await player.send(
				embed=discord.Embed(title="Backdoors and Breaches",description=f"Your hand: {cards_to_send}"
			))

	# Start the first player's turn
	await ctx.reply(
		embed=discord.Embed(title="Backdoors and Breaches",description=f"Starting Backdoors and Breaches game with {len(players)} players... {players[0].mention}'s turn"
	))

	await ctx.send(
		embed=discord.Embed(title="Backdoors and Breaches",description="Remaining procedures cards:\n\n {}".format('\n\n'.join([format_card_info(card) for card in procedures]))
	))


@bot.hybrid_command(name="join-game", description="Lets players join by assigning roles, channel access.")
async def join_game(ctx):
	global players

	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")

	if ctx.author not in players:
		players.append(ctx.author)
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description=
			f"{ctx.author.mention} has joined the game! {len(players)} players are now playing."
		))
	else:
		await ctx.reply(f"{ctx.author.mention} is already in the game!")


async def valid_cards_procedures(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global procedures
	global hands
	
	hand = []
	validCards = []
	if interaction.user.id in hands:
		hand = hands[interaction.user.id]
	validCards = procedures + hand
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_c2(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global c2_and_exfil_card
	
	validCards = [c2_and_exfil_card]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_persistence(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global persistence_card
	
	validCards = [persistence_card]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

async def valid_cards_pivot(interaction: discord.Interaction, card_name: str) -> List[app_commands.Choice[str]]:
	global pivot_and_escalate_card
	
	validCards = [pivot_and_escalate_card]
	
	return [app_commands.Choice(name=card["Title"].lower().capitalize(), value=card["Title"]) for card in validCards]

def format_card_info(card):
	
	cardInfo = "**"+card["Title"]+"**\n\n```"+card["Description"]+"```"
	
	return cardInfo

def handle_extra_modifiers(card):
	global card_modifiers
	if card["Title"] in card_modifiers:
		modifier = modifier + card_modifiers[card["Title"]]
	
	modifier = 0
	return modifier

async def handle_injects(ctx,card):
	global pivot_and_escalate_card
	global card_modifiers
	global procedures
	
	if card["Title"] == "HONEYPOTS DEPLOYED":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(pivot_and_escalate_card)))
		
	elif card["Title"] == "IT WAS A PENTEST":
		await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=format_card_info(card)))
		await end_game(ctx)
		
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
		card_removed = procedures.pop()
	
@bot.hybrid_command(name="play-procedure", description="Starts Procedure phase, complete challenges.")
@app_commands.autocomplete(card_name=valid_cards_procedures)
async def play_procedure(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, hands, pivot_played, c2_played, persistence_played, procedures, cooldowns, inital_played, failed_rolls

	if game_ended:
		return await ctx.reply("No game running")

	player = ctx.author
	if player != players[turn]:
		await ctx.reply("It's not your turn!")
		return

	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")

	# Find the current player's hand and incident master card
	player_index = players.index(player)

	# Find the card to play and remove it from the player's hand or procedures
	modifier = 0
	playerCard = False
	for cardToTurn in cooldowns.copy():
		if (cooldowns[cardToTurn] + 3) < turn:
			del cooldowns[cardToTurn]
	if card_name in cooldowns:
		return await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card is on cooldown!"))

	try:
		card_index = [card["Title"] for card in hands[ctx.message.author.id]].index(
			card_name
		)
		card = hands[ctx.message.author.id].pop(card_index)
		modifier = 3
		await player.send(embed=discord.Embed(title="Backdoors and Breaches",description=
			"Your hand:\n {}".format(',\n'.join([card['Title'] for card in hands[ctx.message.author.id]]))
		))
	except:
		try:
			card_index = [card["Title"] for card in procedures].index(card_name)
			card = procedures.pop(card_index)
			modifier = 0
			await ctx.send(
				embed=discord.Embed(title="Backdoors and Breaches",description="Remaining procedures:\n {}".format(',\n'.join([card['Title'] for card in procedures]))
			))
		except:
			await player.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
			return

	await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description=player.mention + " Plays card:\n\n" + format_card_info(card)))
	dice_roll_orginal = roll_die()
	dice_roll = dice_roll_orginal + (modifier+handle_extra_modifiers(card))
	print("Dice rolled: "+str(dice_roll_orginal)+" Modifier: "+str(modifier))
	await ctx.send(embed=discord.Embed(title="Backdoors and Breaches",description="Dice rolled: "+str(dice_roll_orginal)+" Modifier: "+str(modifier)))
	if (dice_roll) > 10:
		fail = True
		for pivot_card in pivot_played:
			if card["Title"] in pivot_card["Detection"]:
				pivot_played.remove(pivot_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Pivot: " + pivot_card["Title"]))
				fail = False

		for c2_card in c2_played:
			if card["Title"] in c2_card["Detection"]:
				c2_played.remove(c2_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="C2: " + c2_card["Title"]))
				fail = False

		for persistence_card in persistence_played:
			if card["Title"] in persistence_card["Detection"]:
				persistence_played.remove(persistence_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Persistence: " + persistence_card["Title"]))
				fail = False

		for incident_master_card in inital_played:
			if card["Title"] in incident_master_card["Detection"]:
				inital_played.remove(incident_master_card)
				await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Initial Incident was: " + incident_master_card["Title"]))
				fail = False

		if card["Title"] in incident_master_card["Detection"]:
			await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Initial Incident was: " + incident_master_card["Title"]))
			fail = False

		if fail:
			cooldowns[card["Title"]] = turn
			await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Procedure had no effect"))

	else:
		failed_rolls = failed_rolls + 1
		cooldowns[card["Title"]] = turn
		print("Procedure failed")
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Procedure failed"))

	if dice_roll == 1:
		injects_card = injects.pop(0)
		await handle_injects(ctx,injects_card)
	elif failed_rolls > 2:
		failed_rolls = 0
		injects_card = injects.pop(0)
		await handle_injects(ctx,injects_card)

	if len(persistence_played) == 0:
		if len(c2_played) == 0:
			if len(pivot_played) == 0:
				if len(inital_played) == 0:
					game_ended = True

	# Check if the game has ended
	turn = (turn + 1) % len(players)
	if turn > 10:
		game_ended = True

	if game_ended:
		await end_game(ctx)
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

	if not (card_name == c2_and_exfil_card["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = c2_and_exfil_card
	c2_played.append(card)
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))


@bot.hybrid_command(name="play-persistence", description="Starts Persistence phase, eliminate hidden backdoor.")
@app_commands.autocomplete(card_name=valid_cards_persistence)
async def play_persistence(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, persistence_card, persistence_played

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

	if not (card_name == persistence_card["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = persistence_card
	persistence_played.append(card)
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))


@bot.hybrid_command(name="play-pivot", description="Starts Pivot phase, pivot to different part of system")
@app_commands.autocomplete(card_name=valid_cards_pivot)
async def play_pivot_and_escalate(ctx, card_name: str):
	global incident_master_card, turn, players, game_ended, incident_master, hands, pivot_and_escalate_card, pivot_played

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

	if not (card_name == pivot_and_escalate_card["Title"]):
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Invalid card!"))
		return

	card = pivot_and_escalate_card
	pivot_played.append(card)
	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Card played"))


@bot.hybrid_command(name="end-game", description="Ends game, deletes channel and associated roles.")
async def end_game(ctx):
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

	if str(ctx.channel.id) != str(config.config["SETTINGS"]["channel_id"].strip()):
		if str(ctx.channel.id) != str(os.environ.get("CHANNEL_ID")):
			return await ctx.reply("This command can only be used in the designated game channel.")

	game_ended = True

	# Reset game variables
	players = []
	procedures = []
	incident_master = []
	played_cards = []
	incident_master_names = []
	turn = 0
	hands = {}
	pivot_played = []
	c2_played = []
	persistence_played = []
	inital_played = []
	cooldowns = {}
	card_modifiers = {}
	failed_rolls = 0

	await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description="Game ended"))

@bot.hybrid_command(name="bnbhelp", description="Describes the available commands.")
async def bnbhelp(ctx):
	try:
		response = """## Available Commands

- `start-game`: Starts a new game by creating a new channel and setting up the necessary roles and permissions.
- `join-game`: Allows players to join the game by assigning them the "Player" role and granting them access to the game channel.
- `play-procedure`: Starts the Procedure phase of the game, where players must complete a series of challenges to progress.
- `play-c2`: Starts the Command and Control phase of the game, where players take turns being the C2 team and must coordinate with the other players to complete a series of tasks.
- `play-persistence`: Starts the Persistence phase of the game, where players must find and eliminate a hidden backdoor in the system.
- `play-pivot`: Starts the Pivot phase of the game, where players must pivot to a different part of the system and continue their investigation.
- `end-game`: Ends the current game and deletes the game channel and associated roles.

To run a command, type `!` or `/` followed by the command name in the game channel. For example, to start a new game, type `!start-game`. Note that some commands may only be available during certain phases of the game."""
		await ctx.reply(embed=discord.Embed(title="Backdoors and Breaches",description=response))
	except Exception as e:
		await ctx.reply(f"Error: {e}. An unexpected error occurred.")

@bot.event
async def on_ready():
	print("\nLogged in as:")
	print(" Username", bot.user.name)
	print(" User ID", bot.user.id)
	print(
		"To invite the bot in your server use this link:\n https://discord.com/api/oauth2/authorize?client_id="
		+ str(bot.user.id)
		+ "&permissions=8&scope=bot%20applications.commands"
	)
	print("Time now", str(datetime.datetime.now()))
	
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")
	except Exception as e:
		print(e)

	await bot.change_presence(
		activity=Activity(
			type=ActivityType.playing, name="Backdoors and Breaches"
		),
		status=Status.online,
	)
 + "&permissions=8&scope=bot%20applications.commands"
    )
    print("Time now", str(datetime.datetime.now()))
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name="Backdoors and Breaches"
        ),
        status=Status.online,
    )

bot.run(config.discordtoken)
