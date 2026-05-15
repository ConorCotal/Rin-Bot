import discord
from enum import Enum
from utils.UI import EmbedCreator, field

class EmbedType(Enum):
    INFO = "info"
    MESSAGE = "message"
    SERVICE = "service"
    CLAIM = "claim"
    CLOSE = "close"
    EVENT = "event"
    HELP = "help"
    CK = "ck"
    REPORT_PLAYER = "report_player"
    REPORT_ERROR = "report_error"
    CONTACT = "contact"

class Embeds:
    def __init__(self, user: discord.User, inputs: dict):
        self.user = user
        self.field_1 = inputs.get("field_1") if inputs.get("field_1") else None
        self.field_2 = inputs.get("field_2") if inputs.get("field_2") else None
        self.field_3 = inputs.get("field_3") if inputs.get("field_3") else None
        self.field_4 = inputs.get("field_4") if inputs.get("field_4") else None
        self.field_5 = inputs.get("field_5") if inputs.get("field_5") else None

        self.embeds = {
            EmbedType.INFO: EmbedCreator(
                title="Informacje o użytkowniku",
                description="> Poniżej znajdują się informacje o użytkowniku, który utworzył ticket.",
                color=discord.Color.blue(),
                fields=[
                    field(f"Nickname: `{self.user.name}`", f">>> Użytkownik: {self.user.mention}\nID: `{self.user.id}`", False),
                    field(f"Dołączono: `{self.user.joined_at.strftime('%d-%m-%Y %H:%M')}`", f"> Utworzono: `{self.user.created_at.strftime('%d-%m-%Y %H:%M')}`", False)
                ],
                footer="RiftTales"
            ),
            EmbedType.MESSAGE: EmbedCreator(
                title="Nowy Ticket",
                description="> Ticket został utworzony, oraz Admity zostali powiadomieni. Prosimy o cierpliwość, wkrótce ktoś się zajmie Twoją sprawą. Do tego czasu możesz dopisać więcej szczegółów do swojego zgłoszenia. Pamietaj, że to kanał z ustawionym __**Trybem Powolnym na 2 Minuty**__ aby uniknąć spamu, staraj się wysyłać po jednej wiadomości. Kiedy ktoś **Zajmie** twój ticket ten **Limit** zostanie zdjęty.",
                color=discord.Color.og_blurple(),
                footer="RiftTales"
            ),
            EmbedType.SERVICE: EmbedCreator(
                title="Panel Obsługi Ticketu",
                description="",
                color=discord.Color.dark_green(),
                footer="RiftTales"
            ),
            EmbedType.CLOSE: EmbedCreator(
                title="Ticket Zamknięty",
                description=f"> Ticket został zamknięty przez {self.user.mention}",
                color=discord.Color.red(),
                fields=[
                    field("Powód:", f"```\n{self.field_1}\n```", False)
                ],
                footer="RiftTales"
            ),
            EmbedType.EVENT: EmbedCreator(
                title="🎉  Podanie o Event  🎉",
                description="> Poniżej znajdują się szczegóły podania o event.",
                color=discord.Color.gold(),
                fields=[
                    field("Nickname Minecraft", f">>> `{self.field_1}`", False),
                    field("Data", f">>> `{self.field_2}`", False),
                    field("Rodzaj Eventu", f">>> `{self.field_3}`", False),
                    field("Potrzebny GM", f">>> `{self.field_4}`", False),
                    field("Pomysł na Event", f"```\n{self.field_5}\n```", False),
                ],
                footer="RiftTales"
            ),
            EmbedType.HELP: EmbedCreator(
                title="🙏  Potrzebuję Pomocy  🙏",
                description="> Poniżej znajdują się szczegóły zgłoszenia pomocy.",
                color=discord.Color.orange(),
                fields=[
                    field("Nickname Minecraft", f">>> `{self.field_1}`", False),
                    field("Szczegóły Zgłoszenia", f"```\n{self.field_2}\n```", False),
                    field("Próby Rozwiązania", f"```\n{self.field_3}\n```", False),
                ],
                footer="RiftTales"
            ),
            EmbedType.CK: EmbedCreator(
                title="💀  Character Kill  💀",
                description="> Poniżej znajdują się szczegóły zgłoszenia CK.",
                color=discord.Color.dark_red(),
                fields=[
                    field("Nickname Minecraft", f">>> `{self.field_1}`", False),
                    field("Nickname Oponenta", f">>> `{self.field_2}`", False),
                    field("Potrzebny GM", f">>> `{self.field_3}`", False),
                    field("Opis Śmierci", f"```\n{self.field_4}\n```", False),
                ],
                footer="RiftTales"
            ),
            EmbedType.REPORT_PLAYER: EmbedCreator(
                title="👤  Zgłoszenie Gracza  👤",
                description="> Poniżej znajdują się szczegóły zgłoszenia gracza.",
                color=discord.Color.dark_orange(),
                fields=[
                    field("Nickname Minecraft Zgłaszanego", f">>> `{self.field_1}`", False),
                    field("Szczegóły Zgłoszenia", f"```\n{self.field_2}\n```", False),
                ],
                footer="RiftTales"
            ),
            EmbedType.REPORT_ERROR: EmbedCreator(
                title="👾  Zgłoszenie Błędu  👾",
                description="> Poniżej znajdują się szczegóły zgłoszenia błędu.",
                color=discord.Color.dark_purple(),
                fields=[
                    field("Szczegóły Zgłoszenia", f"```\n{self.field_1}\n```", False),
                ],
                footer="RiftTales"
            ),
            EmbedType.CONTACT: EmbedCreator(
                title="✉️  Kontakt  ✉️",
                description="> Poniżej znajdują się szczegóły zgłoszenia kontaktowego.",
                color=discord.Color.blurple(),
                fields=[
                    field("Temat", f">>> `{self.field_1}`", False),
                    field("Treść", f"```\n{self.field_2}\n```", False),
                ],
                footer="RiftTales"
            ),
        }

    def get(self, embed_type: EmbedType):
        return self.embeds.get(embed_type)
