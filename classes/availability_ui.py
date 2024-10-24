import discord
from datetime import datetime


class AvailabilityUI(discord.ui.View):
    def __init__(self, date: datetime):
        super().__init__()
        self.date = date
        self.embed = discord.Embed(color=discord.Color.yellow())

    @discord.ui.button(label="<<")
    async def backward(self, button: discord.ui.Button, interaction:discord.Interaction):
        pass

    @discord.ui.button(label=">>")
    async def forward(self, button: discord.ui.Button, interaction:discord.Interaction):
        pass

    def get_embed(self):
        return self.get_embed
