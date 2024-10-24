import discord
from datetime import datetime

from classes.datetime_manager import DTManager as dtm


class AvailabilityUI(discord.ui.View):
    def __init__(self, date: str):
        super().__init__()
        self.date: str = date
        self.date_dt: datetime = dtm.string_to_datetime(date, False)
        self.embed = discord.Embed(
            title=f"Availability Chart: {self.date_dt.strftime('%B %d, %Y')}",
            color=discord.Color.yellow()
        )

    @discord.ui.button(label="<<")
    async def backward(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label=">>")
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    def get_embed(self):
        return self.embed

    def schedule_to_string(self, schedule: list):
        pass
