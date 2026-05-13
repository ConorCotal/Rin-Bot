import discord
from utils.UI import ButtonCreator, button
from .Modals import Modals

class Buttons:
    def __init__(self, bot):
        self.bot = bot
        self.modals = Modals(bot)

        self.mc_view = None
        self.other_view = None

    @property
    def handlers(self):
        return {
            "event_ticket": self.modals.event,
            "help_ticket": self.modals.help,
        }

    def create(self):
        self.mc_view = ButtonCreator(
            button("Podanie o Event", discord.ButtonStyle.green, emoji="🎉", custom_id="event_ticket", row=0),
            button("Potrzebuję Pomocy", discord.ButtonStyle.blurple, emoji="🙏", custom_id="help_ticket", row=0),
            button("CK", discord.ButtonStyle.red, emoji="💀", custom_id="ck_ticket", row=1),
            callback=self.callback,
            persistent=True,
            bot=self.bot
        )

        self.other_view = ButtonCreator(
            button("Zgłoś Gracza", discord.ButtonStyle.red, emoji="👤", custom_id="report_player_ticket", row=0),
            button("Zgłoś Błąd", discord.ButtonStyle.red, emoji="👾", custom_id="report_error_ticket", row=0),
            button("Kontakt", discord.ButtonStyle.blurple, emoji="✉️", custom_id="contact_ticket", row=1),
            callback=self.callback,
            persistent=True,
            bot=self.bot
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            custom_id = interaction.data.get("custom_id")
            handler = self.handlers.get(custom_id)
            if handler:
                await interaction.response.send_modal(handler)
            else:
                await interaction.response.send_message("Nieznany przycisk.", ephemeral=True)
                print(f"Nieznany custom_id: {custom_id}")
                print(f"{handler}")

        except Exception as e:
            print(f"Error in callback: {e}")
            # Nie próbuj odpowiadać, jeśli interakcja wygasła
    