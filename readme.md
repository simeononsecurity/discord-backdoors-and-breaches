# Discord Backdoors and Breaches Bot

[![Docker Image CI](https://github.com/simeononsecurity/discord-backdoors-and-breaches/actions/workflows/docker-image.yml/badge.svg)](https://github.com/simeononsecurity/discord-backdoors-and-breaches/actions/workflows/docker-image.yml)

![Backdoors and Breaches](https://github.com/simeononsecurity/discord-backdoors-and-breaches/blob/main/.github/images/bnb-dark.png?raw=true)


A Discord bot for Backdoors and Breaches, a turn-based strategy game by The Meld Group.

## Commands

- `!startgame`: starts a new game of Backdoors and Breaches. Only one game can be active at a time.
- `!endgame`: ends the current game of Backdoors and Breaches.
- `!turn <team>`: allows the specified team to take their turn. Can only be used by the team that is currently up.
- `!place <team> <node>`: allows the specified team to place one of their nodes on the specified node on the game board. Can only be used during the placement phase of the game.
- `!move <team> <from_node> <to_node>`: allows the specified team to move one of their nodes from the specified node to the specified destination node. Can only be used during the movement phase of the game.

## Setting up the Bot

### Using Python

1. Clone this repository using `git clone https://github.com/simeononsecurity/discord-backdoors-and-breaches.git`.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create a `config.ini` file in the root directory of the project with the following content:
```ini
[SETTINGS]
discordtoken = put_discord_bot_token_here
channel_id = put_game_channel_id_here

markdown
```
4. Replace `put_discord_bot_token_here` with your Discord bot token and `put_game_channel_id_here` with the ID of the channel where you want the game to be played.
5. Run the bot using `python main.py`.

### Using Docker

1. Clone the repository and navigate to the directory:
```
git clone https://github.com/simeononsecurity/discord-backdoors-and-breaches.git
cd discord-backdoors-and-breaches
```
2. Create an `.env` file in the root directory of the project and add the following environment variables with their corresponding values:
```env
BOT_TOKEN=<discord_bot_token_here>
CHANNEL_ID=<game_channel_id_here>
```
3. Build the Docker image using the provided Dockerfile:
```bash
docker build -t discord-backdoors-and-breaches .
```
4. Run the Docker container, passing in the environment variables from the `.env` file:
```bash
docker run --env-file .env discord-backdoors-and-breaches
```

Alternatively, you can set the environment variables directly during the `docker run` command:
```bash
docker run -e BOT_TOKEN=<discord_bot_token_here> -e CHANNEL_ID=<game_channel_id_here> discord-backdoors-and-breaches
```



