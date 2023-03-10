import discord
import random
import config
import datetime
from discord import Activity, ActivityType, Status
from discord.ext import commands, tasks

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

    if not str(ctx.channel.id) == str(config.config["SETTINGS"]["channel_id"].strip()):
        return True

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
            await player.send(
                f"Your hand: {', '.join([card['Title'] for card in hand])}"
            )
            await ctx.send(
                f"{ctx.author.mention} hand: {', '.join([card['Title'] for card in hand])}"
            )

        # injects_card = injects.pop(0)
        # await player.send(f"Injects card: {injects_card['Title']}")

        if i == 0:
            incident_master_card = incident_master.pop(0)
            inital_played.append(incident_master_card)
            await player.send(f"Incident Master card: {incident_master_card['Title']}")
            c2_and_exfil_card = c2_and_exfil.pop(0)
            await player.send(f"C2 and Exfil card: {c2_and_exfil_card['Title']}")
            persistence_card = persistence.pop(0)
            await player.send(f"Persistence card: {persistence_card['Title']}")
            pivot_and_escalate_card = pivot_and_escalate.pop(0)
            await player.send(
                f"Pivot and Escalate card: {pivot_and_escalate_card['Title']}"
            )

    # Start the first player's turn
    await ctx.send(
        f"Starting Backdoors and Breaches game with {len(players)} players... {players[0].mention}'s turn"
    )

    await ctx.send(
        f"Remaining procedures cards: {', '.join([card['Title'] for card in procedures])}"
    )


@bot.hybrid_command(name="join-game", description="Lets players join by assigning roles, channel access.")
async def join_game(ctx):
    global players

    if not str(ctx.channel.id) == str(config.config["SETTINGS"]["channel_id"].strip()):
        return True

    if ctx.author not in players:
        players.append(ctx.author)
        await ctx.send(
            f"{ctx.author.mention} has joined the game! {len(players)} players are now playing."
        )
    else:
        await ctx.send(f"{ctx.author.mention} is already in the game!")


@bot.hybrid_command(name="play-procedure", description="Starts Procedure phase, complete challenges.")
async def play_procedure(ctx, card_name):
    global incident_master_card, turn, players, game_ended, hands, pivot_played, c2_played, persistence_played, procedures, cooldowns, inital_played, failed_rolls

    if game_ended:
        await ctx.send("No game running")

    player = ctx.author
    if player != players[turn]:
        await ctx.send("It's not your turn!")
        return

    if not str(ctx.channel.id) == str(config.config["SETTINGS"]["channel_id"].strip()):
        return True

    # Find the current player's hand and incident master card
    player_index = players.index(player)

    # Find the card to play and remove it from the player's hand or procedures
    modifier = 0
    playerCard = False
    for cardToTurn in cooldowns.copy():
        if (cooldowns[cardToTurn] + 3) < turn:
            del cooldowns[cardToTurn]
    if card_name in cooldowns:
        return await ctx.send("Card is on cooldown!")

    try:
        card_index = [card["Title"] for card in hands[ctx.message.author.id]].index(
            card_name
        )
        # card = hands[ctx.message.author.id].pop(card_index)
        modifier = 3
        await player.send(
            f"Your hand: {', '.join([card['Title'] for card in hands[ctx.message.author.id]])}"
        )
    except:
        try:
            card_index = [card["Title"] for card in procedures].index(card_name)
            # card = procedures.pop(card_index)
            modifier = 0
            await ctx.send(
                f"Remaining procedures: {', '.join([card['Title'] for card in procedures])}"
            )
        except:
            await player.send("Invalid card!")
            return

    await ctx.send(player.mention + " Plays card: " + card["Title"])
    dice_roll = roll_die() + modifier
    if (dice_roll) > 10:
        fail = True
        for pivot_card in pivot_played:
            if card["Title"] in pivot_card["Detection"]:
                pivot_played.remove(pivot_card)
                await ctx.send("Pivot: " + pivot_card["Title"])
                fail = False

        for c2_card in c2_played:
            if card["Title"] in c2_card["Detection"]:
                c2_played.remove(c2_card)
                await ctx.send("C2: " + c2_card["Title"])
                fail = False

        for persistence_card in persistence_played:
            if card["Title"] in persistence_card["Detection"]:
                persistence_played.remove(persistence_card)
                await ctx.send("Persistence: " + persistence_card["Title"])
                fail = False

        for incident_master_card in inital_played:
            if card["Title"] in incident_master_card["Detection"]:
                inital_played.remove(incident_master_card)
                await ctx.send("Initial Incident was: " + incident_master_card["Title"])
                fail = False

        if card["Title"] in incident_master_card["Detection"]:
            await ctx.send("Initial Incident was: " + incident_master_card["Title"])
            fail = False

        if fail:
            cooldowns[card["Title"]] = turn

    else:
        failed_rolls = failed_rolls + 1
        cooldowns[card["Title"]] = turn
        print("Procedure failed")

    if dice_roll == 1:
        injects_card = injects.pop(0)
        await ctx.send(f"Injects card: {injects_card['Title']}")
    elif failed_rolls > 2:
        failed_rolls = 0
        injects_card = injects.pop(0)
        await ctx.send(f"Injects card: {injects_card['Title']}")

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


@bot.hybrid_command(name="play-incident-master", description="Starts Incident Master phase, respond to simulated incidents.")
async def play_incident_master(ctx, card_name: str):
    global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card

    if game_ended:
        await ctx.send("No game running")

    # Find the current player's index
    player_index = players.index(ctx.author)

    if player_index != 0:
        await ctx.send("You are not incident master")

    # Check that the player sent a valid command to play an incident master card
    if ctx.author != players[turn]:
        await ctx.send("It's not your turn!")
        return

    if not (card_name in incident_master_names):
        await ctx.send("Invalid card!")
        return

    card = incident_master_card
    # await ctx.send(f"{ctx.author.mention} played {card['Title']} as the Incident Master card.")

    # c2_played.append(card)
    await ctx.send("Cmd should not be used?")


@bot.hybrid_command(name="play-c2", description="Starts Command and Control phase, complete tasks.")
async def play_c2(ctx, card_name: str):
    global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, c2_played

    if game_ended:
        await ctx.send("No game running")

    # Find the current player's index
    player_index = players.index(ctx.author)

    if player_index != 0:
        await ctx.send("You are not incident master")

    # Check that the player sent a valid command to play an incident master card
    if ctx.author != players[turn]:
        await ctx.send("It's not your turn!")
        return

    if not (card_name == c2_and_exfil_card):
        await ctx.send("Invalid card!")
        return

    card = c2_and_exfil_card
    c2_played.append(card)
    await ctx.send("Card played")


@bot.hybrid_command(name="play-persistence", description="Starts Persistence phase, eliminate hidden backdoor.")
async def play_persistence(ctx, card_name: str):
    global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, persistence_card, persistence_played

    if game_ended:
        await ctx.send("No game running")

    # Find the current player's index
    player_index = players.index(ctx.author)

    if player_index != 0:
        await ctx.send("You are not incident master")

    # Check that the player sent a valid command to play an incident master card
    if ctx.author != players[turn]:
        await ctx.send("It's not your turn!")
        return

    if not (card_name == persistence_card):
        await ctx.send("Invalid card!")
        return

    card = persistence_card
    persistence_played.append(card)
    await ctx.send("Card played")


@bot.hybrid_command(name="play-pivot", description="Starts Pivot phase, pivot to different part of system")
async def play_pivot_and_escalate(ctx, card_name: str):
    global incident_master_card, turn, players, game_ended, incident_master, hands, c2_and_exfil_card, persistence_card, pivot_and_escalate_card, pivot_played

    if game_ended:
        await ctx.send("No game running")

    # Find the current player's index
    player_index = players.index(ctx.author)

    if player_index != 0:
        await ctx.send("You are not incident master")

    # Check that the player sent a valid command to play an incident master card
    if ctx.author != players[turn]:
        await ctx.send("It's not your turn!")
        return

    if not (card_name == pivot_and_escalate_card):
        await ctx.send("Invalid card!")
        return

    card = pivot_and_escalate_card
    pivot_played.append(card)
    await ctx.send("Card played")


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

    if not str(ctx.channel.id) == str(config.config["SETTINGS"]["channel_id"].strip()):
        return True

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
    failed_rolls = 0

    await ctx.send("Game ended")

@bot.hybrid_command(name="bnbhelp", description="Describes the available commands.")
async def bnbhelp(ctx):
    try:
        response = """## Available Commands

- `start-game`: Starts a new game by creating a new channel and setting up the necessary roles and permissions.
- `join-game`: Allows players to join the game by assigning them the "Player" role and granting them access to the game channel.
- `play-procedure`: Starts the Procedure phase of the game, where players must complete a series of challenges to progress.
- `play-incident-master`: Starts the Incident Master phase of the game, where players take turns being the Incident Master and directing the other players on how to respond to a simulated incident.
- `play-c2`: Starts the Command and Control phase of the game, where players take turns being the C2 team and must coordinate with the other players to complete a series of tasks.
- `play-persistence`: Starts the Persistence phase of the game, where players must find and eliminate a hidden backdoor in the system.
- `play-pivot`: Starts the Pivot phase of the game, where players must pivot to a different part of the system and continue their investigation.
- `end-game`: Ends the current game and deletes the game channel and associated roles.

To run a command, type `!` or `/` followed by the command name in the game channel. For example, to start a new game, type `!start-game`. Note that some commands may only be available during certain phases of the game."""
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

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

bot.run(config.discordtoken)
