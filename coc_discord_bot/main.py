import discord
import os
import random
from discord.ext import commands
import logging
import json
from dotenv import load_dotenv
import requests

load_dotenv()
intents = discord.Intents(messages=True, guilds=True)

# client = discord.Client(intents=intents)


token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv('API_KEY')

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix='!')

@client.event
async def on_ready():
    try:
        await client.tree.sync()
        print("Synced the commands with Discord.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return

    if channel == "bot_commands":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            jokes = [" Can someone please shed more\
            light on how my lamp got stolen?",
                     "Why is she called llene? She\
                     stands on equal legs.",
                     "What do you call a gazelle in a \
                     lions territory? Denzel."]
            await message.channel.send(random.choice(jokes))
            
@client.tree.command(name="hello", description="Says hello to the user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

@client.tree.command(name="say")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f"{interaction.user.mention} says: {things_to_say}")

@client.tree.command(name="war_log", description="Fetches the war log of a clan")
async def war_log(interaction: discord.Interaction):

    url = "https://api.clashofclans.com/v1/clans/%232rrjgccvv/warlog"
    headers = {
        "Authorization": f"Bearer {api_key}" 
    }

    response = requests.get(url, headers=headers)

    # Print the response
    print(response.status_code)
    data = response.json()
    print(json.dumps(data, indent=4))  # Beautified output
    clan_name = data["items"][0]["clan"]["name"]
    
    print(f"Clan Name: {clan_name}")
    response = ""
    
    # for i in data["items"]:
    for i in data.get("items", []):
        clan_name = i.get("clan", {}).get("name", "Unknown Clan")
        opponent_name = i.get("opponent", {}).get("name", "Unknown Opponent")
        result = i.get("result", "Unknown Result")
        
        line = f"{clan_name} vs {opponent_name} - {result}\n"
        print(line)
        response += line

    await interaction.response.send_message(f"War log for : {clan_name}\n{response}")




handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')



# Assume client refers to a discord.Client subclass...
client.run(token, log_handler=handler, log_level=logging.DEBUG)