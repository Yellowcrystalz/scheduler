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
    
    def set_embed(self, schedule: str):
        self.embed.clear_fields()
        self.embed.add_field(name="", value=schedule, inline=False)


    def availability_to_embed(self, availability_slots: list):
        schedule: str = ""

        for i in range(len(availability_slots)):
            if i % 12 == 0:
                schedule += ("—" * 21)
                schedule += "\n"

                if i == 0:
                    schedule += ":one::two: :one: :two: :three: :four: :five:\n"
                elif i == 12:
                    schedule += ":six: :seven: :eight: :nine: :number_10: :one::one:\n"
                elif i == 24:
                    schedule += ":one::two: :one: :two: :three: :four: :five:\n"
                elif i == 36:
                    schedule += ":six: :seven: :eight: :nine: :number_10: :one::one:\n"

            if(availability_slots[i] == 0):
                schedule += ":green_square:"
            else:
                schedule += ":red_square:"

            if (i % 12) % 2 == 1:
                schedule += " "

            if i % 12 == 11:
                schedule += "\n"
        
        self.set_embed(schedule)