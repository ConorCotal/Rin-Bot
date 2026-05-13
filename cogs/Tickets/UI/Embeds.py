import discord
from enum import Enum
from utils.UI import EmbedCreator, field

class EmbedType(Enum):
    INFO = "info"
    EVENT = "event"
    HELP = "help"

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
                    field(f"Użytkownik: {self.user.mention}", f">>> Nickname: `{self.user.name}`\nID: `{self.user.id}`", False),
                    field(f"Dołączono: `{self.user.joined_at.strftime('%d-%m-%Y %H:%M')}`", f"> Utworzono: `{self.user.created_at.strftime('%d-%m-%Y %H:%M')}`", False)
                ],
                footer="RiftTales"
            ),
            EmbedType.EVENT: EmbedCreator(
                title="Podanie o Event 🎉",
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
                title="Potrzebuję Pomocy 🙏",
                description="> Poniżej znajdują się szczegóły zgłoszenia pomocy.",
                color=discord.Color.orange(),
                fields=[
                    field("Nickname Minecraft", f">>> `{self.field_1}`", False),
                    field("Szczegóły Zgłoszenia", f"```\n{self.field_2}\n```", False),
                    field("Próby Rozwiązania", f"```\n{self.field_3}\n```", False),
                ],
                footer="RiftTales"
            )
        }

    def get(self, embed_type: EmbedType):
        return self.embeds.get(embed_type)
