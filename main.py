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


@bot.tree.command(name="roll", description="Roll a champion category")
async def roll(interaction: discord.Interaction):
    outcome = funkyDBrollingLogic.rolling_dice()
    await interaction.response.send_message(outcome)


bot.run(token)
