import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from database.python.db_manager import DBManager


class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="help", description="Info on all the / commands")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message("help yourself :/")

    @app_commands.command(name="availability", description="Check out SWAMP Lab availability")
    @app_commands.describe(date="dd-mm-yyyy")
    async def availability(self, interaction: discord.Interaction, date: str = None):

        date = datetime.now().strftime("%Y-%m-%d")
        date_object = datetime.datetime.strptime(date, "%Y-%m-%d")

        await interaction.response.send_message(date_object)


async def setup(bot):
    await bot.add_cog(CommandHandler(bot))
