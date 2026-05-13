import discord
from functools import partial
from datetime import datetime, timezone, timedelta
from utils.UI import ModalCreator, modal_field
from ..Creator import Creator
from .Embeds import EmbedType

debug = True  # Ustaw na False w produkcji

class Modals:
    def __init__(self, bot):
        self.bot = bot
        self.creator = Creator(bot)

        self.event = None
        self.help = None

    async def create(self):
        self.event = ModalCreator(
            "Ticket > Podanie o Event 🎉",
            modal_field("Nickname Minecraft", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz swój nickname Minecraft..", max_length=16, min_length=2, required=True, default="RinPlay" if debug else None),
            modal_field("Data", discord.TextStyle.short, custom_id="field_2", placeholder="Tu wpisz datę eventu..", max_length=21, min_length=10, required=True, default=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=2))).strftime("%d-%m | %H:%M")),
            modal_field("Lokalny czy Globalny", discord.TextStyle.short, custom_id="field_3", placeholder="Tu wpisz rodzaj eventu..", max_length=8, min_length=7, required=True, default="Lokalny"),
            modal_field("Potrzebny GM", discord.TextStyle.short, custom_id="field_4", placeholder="Tak/Nie", max_length=3, min_length=3, required=True, default="Nie"),
            modal_field("Pomysł na Event", discord.TextStyle.long, custom_id="field_5", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Opis eventu..." if debug else None),
            callback=partial(self.callback, ticket_type=EmbedType.EVENT)
        )

        self.help = ModalCreator(
            "Ticket > Potrzebuję Pomocy 🙏",
            modal_field("Nickname Minecraft", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz swój nickname Minecraft..", max_length=16, min_length=2, required=True, default="RinPlay" if debug else None),
            modal_field("Szczegóły Zgłoszenia", discord.TextStyle.long, custom_id="field_2", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Szczegóły zgłoszenia..." if debug else None),
            modal_field("Próby Rozwiązania", discord.TextStyle.long, custom_id="field_3", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Próby rozwiązania..." if debug else None),
            callback=partial(self.callback, ticket_type=EmbedType.HELP)
        )

    async def callback(self, interaction: discord.Interaction, inputs: dict, ticket_type: EmbedType):
        await interaction.response.defer(ephemeral=True)
        await self.creator.setup(interaction, inputs)
        await self.creator.thread_create(ticket_type)
