import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from database.python.db_manager import DBManager as dbm
from classes.booking_manager import BookingManager as bkm
from classes.datetime_manager import DTManager as dtm
from classes.parameterizer import Parameterizer

from classes.availability_ui import AvailabilityUI


class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="help", description="Info on all the / commands")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message("help yourself :/")

    @app_commands.command(name="book", description="Book a time slot in the SWAMP Lab")
    @app_commands.describe(
        date="dd-mm-yyyy",
        start="hh:mm",
        end="hh:mm",
        name="name"
    )
    async def book(self, interaction: discord.Interaction, date: str, start: str, end: str, name: str):
        if Parameterizer.check_date(date):
            await interaction.response.send_message("**ERROR:** Date Format = [MM-DD-YYYY]", ephemeral=True)
            return

        if Parameterizer.check_time(start) or Parameterizer.check_time(end):
            await interaction.response.send_message("**ERROR:** Start/End Format = [HH-MM]", ephemeral=True)
            return

        date_formatted: str = Parameterizer.reformat_date(date)
        start = f"{date_formatted} {start}"
        end = f"{date_formatted} {end}"

        start_dt: datetime = dtm.string_to_datetime(start)
        end_dt: datetime = dtm.string_to_datetime(end)

        start_dt = dtm.convert_to_utc(start_dt, -5)
        end_dt = dtm.convert_to_utc(end_dt, -5)

        reserved_slots: list = await dbm.find_bookings(date_formatted, -5, False)
        booking_status: int = bkm.check_booking(start_dt, end_dt, reserved_slots)

        if booking_status == 0:
            start = dtm.datetime_to_string(start_dt)
            end = dtm.datetime_to_string(end_dt)
            await dbm.add_booking(start, end, interaction.user.id, name, 0)
            await interaction.response.send_message("Booking successful")
        elif booking_status == -1:
            await interaction.response.send_message(
                "**ERROR:** The time frame inputted is not possible",
                ephemeral=True
            )
        elif booking_status == -2:
            await interaction.response.send_message(
                "**ERROR:** Your booking duration exceeds 4 hours",
                ephemeral=True
            )
        elif booking_status == -3:
            await interaction.response.send_message(
                "**ERROR:** Your booking conflicts with another reservation",
                ephemeral=True
            )

    @app_commands.command(name="availability", description="Check out SWAMP Lab availability")
    @app_commands.describe(date="dd-mm-yyyy")
    async def availability(self, interaction: discord.Interaction, date: str):
        if Parameterizer.check_date(date):
            await interaction.response.send_message("**ERROR:** Date Format = [MM-DD-YYYY]", ephemeral=True)
            return

        date = Parameterizer.reformat_date(date)
        view = AvailabilityUI(date)
        await interaction.response.send_message(embed=view.get_embed(), view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(CommandHandler(bot))
