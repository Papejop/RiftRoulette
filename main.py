import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import funkyDBrollingLogic

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')


@bot.tree.command(name="roll_categories", description="Roll a champion category")
async def roll_categories(interaction: discord.Interaction):
    outcome = funkyDBrollingLogic.rolling_dice()
    await interaction.response.send_message(outcome)

@bot.tree.command(name="roll_skins", description="Roll a skinline for 5 players")
async def roll_skins(
    interaction: discord.Interaction,
    username1: str,
    username2: str,
    username3: str,
    username4: str,
    username5: str                 
):
    usernames = [username1, username2, username3, username4, username5]
    outcome = funkyDBrollingLogic.rolling_dice_skinline(usernames)
    await interaction.response.send_message(outcome)

bot.run(token)
