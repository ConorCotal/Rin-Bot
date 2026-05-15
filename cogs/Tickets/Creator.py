import discord
from .UI.Embeds import EmbedType, Embeds
from utils.Config import config

name = "{type} | {user}"

class Creator:
    def __init__(self, bot, debug=False):
        self.bot = bot
        self.debug = debug
        self.ticket_role = None
        
        self.interaction = None
        self.inputs = None
        self.embeds = None
        self.buttons = None

    async def setup(self, interaction: discord.Interaction, inputs: dict):
        self.interaction = interaction
        self.inputs = inputs
        self.embeds = Embeds(interaction.user, inputs)
        self.ticket_role = self.get_role()

    def get_name(self, ticket_type: str):
        return name.format(type=ticket_type, user=self.interaction.user.global_name)
    
    def get_role(self):
        return self.interaction.guild.get_role(config['Tickets.ticket_role_id'])

    async def thread_create(self, embed_type: EmbedType, ticket_type: str):
        from .UI.Buttons import Buttons
        ticket_name = f"{'[DEBUG]' if self.debug else ''} {self.get_name(ticket_type)}"

        try:
            if not isinstance(self.interaction.channel, discord.TextChannel):
                await self.interaction.followup.send("Ten kanał nie pozwala na tworzenie wątków.", ephemeral=True)
                return

            buttons = Buttons(self.bot)
            buttons.create()
            await buttons.modals.create()

            thread = await self.interaction.channel.create_thread(name=ticket_name, type=discord.ChannelType.private_thread, auto_archive_duration=10080, slowmode_delay=120, invitable=False)
            mention_message = await thread.send(f"{self.interaction.user.mention} {self.ticket_role.mention}")
            await mention_message.delete()

            await thread.send(embed=self.embeds.get(EmbedType.INFO))
            await thread.send(embed=self.embeds.get(embed_type))
            await thread.send(embed=self.embeds.get(EmbedType.MESSAGE))
            await thread.send(embed=self.embeds.get(EmbedType.SERVICE), view=buttons.service_view)

            # set_ticket(self.bot.user.id, ticket_type, thread.id)  # Zakładam, że masz funkcję do przechowywania ticketów
            
            await self.interaction.followup.send(f"# Ticket został utworzony\n\n> {thread.mention} ◀ `[Kliknij Tutaj Aby Wejść]`", ephemeral=True)
        except Exception as e:
            print(f"Błąd: {e}")
            await self.interaction.followup.send(f"# Koniecznie skontaktuj się z administratorem.\n\n> Wystąpił błąd: {e}\n-# Creator.py", ephemeral=True)
