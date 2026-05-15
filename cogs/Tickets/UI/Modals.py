import discord
from functools import partial
from datetime import datetime, timezone, timedelta
from utils.UI import ModalCreator, modal_field
from ..Creator import Creator
from .Embeds import EmbedType, Embeds

debug = True  # Ustaw na False w produkcji

class Modals:
    def __init__(self, bot):
        self.bot = bot
        self.creator = Creator(bot, debug=debug)

        self.close = None
        self.event = None
        self.help = None
        self.ck = None
        self.report_player = None
        self.report_error = None
        self.contact = None

    async def create(self):
        self.close = ModalCreator(
            "Ticket > Zamknięcie ❌",
            modal_field("Powód Zamknięcia", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz powód zamknięcia..", required=True, default="[DEBUG] Powód zamknięcia..." if debug else None),
            callback=self.close_callback
        )

        self.event = ModalCreator(
            "Ticket > Podanie o Event 🎉",
            modal_field("Nickname Minecraft", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz swój nickname Minecraft..", max_length=16, min_length=2, required=True, default="RinPlay" if debug else None),
            modal_field("Data", discord.TextStyle.short, custom_id="field_2", placeholder="Tu wpisz datę eventu..", max_length=21, min_length=10, required=True, default=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=2))).strftime("%d-%m | %H:%M")),
            modal_field("Lokalny czy Globalny", discord.TextStyle.short, custom_id="field_3", placeholder="Tu wpisz rodzaj eventu..", max_length=8, min_length=7, required=True, default="Lokalny"),
            modal_field("Potrzebny GM", discord.TextStyle.short, custom_id="field_4", placeholder="Tak/Nie", max_length=3, min_length=3, required=True, default="Nie"),
            modal_field("Pomysł na Event", discord.TextStyle.long, custom_id="field_5", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Opis eventu..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.EVENT, ticket_type="🎉")
        )

        self.help = ModalCreator(
            "Ticket > Potrzebuję Pomocy 🙏",
            modal_field("Nickname Minecraft", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz swój nickname Minecraft..", max_length=16, min_length=2, required=True, default="RinPlay" if debug else None),
            modal_field("Szczegóły Zgłoszenia", discord.TextStyle.long, custom_id="field_2", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Szczegóły zgłoszenia..." if debug else None),
            modal_field("Próby Rozwiązania", discord.TextStyle.long, custom_id="field_3", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Próby rozwiązania..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.HELP, ticket_type="🙏")
        )
        
        self.ck = ModalCreator(
            "Ticket > Character Kill 💀",
            modal_field("Nickname Minecraft", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz swój nickname Minecraft..", max_length=16, min_length=2, required=True, default="RinPlay" if debug else None),
            modal_field("Nickname Minecraft Oponenta", discord.TextStyle.short, custom_id="field_2", placeholder="Tu wpisz nickname oponenta jeśli Ticket dotyczy śmierci innej postaci..", max_length=16, min_length=2, required=False, default="Gracz123" if debug else None),
            modal_field("Potrzebny GM", discord.TextStyle.short, custom_id="field_3", placeholder="Tak/Nie", max_length=3, min_length=3, required=True, default="Nie"),
            modal_field("Jak postać ma umrzeć?", discord.TextStyle.long, custom_id="field_4", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Opis śmierci..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.CK, ticket_type="💀"))
        
        self.report_player = ModalCreator(
            "Ticket > Zgłoszenie Gracza 👤",
            modal_field("Nickname Minecraft Zgłaszanego", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz nickname zgłaszanego gracza..", max_length=16, min_length=2, required=True, default="Gracz123" if debug else None),
            modal_field("Szczegóły Zgłoszenia", discord.TextStyle.long, custom_id="field_2", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Szczegóły zgłoszenia..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.REPORT_PLAYER, ticket_type="👤"))
        
        self.report_error = ModalCreator(
            "Ticket > Zgłoszenie Błędu 👾",
            modal_field("Szczegóły Zgłoszenia", discord.TextStyle.long, custom_id="field_1", placeholder="Tu wpisz treść..", min_length=14, required=True, default="[DEBUG] Szczegóły zgłoszenia..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.REPORT_ERROR, ticket_type="👾"))
        
        self.contact = ModalCreator(
            "Ticket > Kontakt ✉️",
            modal_field("Temat", discord.TextStyle.short, custom_id="field_1", placeholder="Tu wpisz temat wiadomości..", max_length=50, min_length=2, required=True, default="Kontakt w sprawie..." if debug else None),
            modal_field("Treść", discord.TextStyle.long, custom_id="field_2", placeholder="Tu wpisz treść wiadomości..", min_length=14, required=True, default="[DEBUG] Treść wiadomości..." if debug else None),
            callback=partial(self.callback, embed_type=EmbedType.CONTACT, ticket_type="✉️"))

    async def callback(self, interaction: discord.Interaction, inputs: dict, embed_type: EmbedType, ticket_type: str):
        await interaction.response.defer(ephemeral=True)
        await self.creator.setup(interaction, inputs)
        await self.creator.thread_create(embed_type, ticket_type)

    async def close_callback(self, interaction: discord.Interaction, inputs: dict):
        thread = interaction.channel if isinstance(interaction.channel, discord.Thread) else None
        if thread is None: return

        embeds = Embeds(interaction.user, inputs)
        await interaction.response.defer()
        await interaction.channel.send(embed=embeds.get(EmbedType.CLOSE))

        await thread.edit(archived=True, locked=True)
