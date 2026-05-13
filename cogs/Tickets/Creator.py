import discord
from .UI.Embeds import EmbedType, Embeds

class Creator:
    def __init__(self, bot):
        self.bot = bot
        self.embeds = None
        self.interaction = None
        self.inputs = None

    async def setup(self, interaction: discord.Interaction, inputs: dict):
        self.interaction = interaction
        self.inputs = inputs
        self.embeds = Embeds(interaction.user, inputs)

    async def thread_create(self, ticket_type: EmbedType):
        try:
            if not isinstance(self.interaction.channel, discord.TextChannel):
                await self.interaction.followup.send("Ten kanał nie pozwala na tworzenie wątków.", ephemeral=True)
                return

            thread = await self.interaction.channel.create_thread(name="[Debug] test", type=discord.ChannelType.private_thread)
            mention_message = await thread.send(f"{self.interaction.user.mention} and ticket admit")
            await mention_message.delete()

            await thread.send(embed=self.embeds.get(EmbedType.INFO))
            await thread.send(embed=self.embeds.get(ticket_type))

            # set_ticket(self.bot.user.id, ticket_type, thread.id)  # Zakładam, że masz funkcję do przechowywania ticketów
            
            await self.interaction.followup.send(f"# Ticket został utworzony\n\n> {thread.mention} ◀ `[Kliknij Tutaj Aby Wejść]`", ephemeral=True)
        except Exception as e:
            print(f"Błąd: {e}")
            await self.interaction.followup.send(f"# Koniecznie skontaktuj się z administratorem.\n\n> Wystąpił błąd: {e}\n-# Creator.py", ephemeral=True)
