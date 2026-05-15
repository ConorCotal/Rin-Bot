import discord
import asyncio
from utils.UI import ButtonCreator, button, EmbedCreator
from utils.Config import config
from .Modals import Modals

class Buttons:
    def __init__(self, bot):
        self.bot = bot
        self.modals = Modals(bot)

        self.service_view = None
        self.mc_view = None
        self.other_view = None

    @property
    def handlers(self):
        return {
            "close_ticket": self.modals.close,
            "event_ticket": self.modals.event,
            "help_ticket": self.modals.help,
            "ck_ticket": self.modals.ck,
            "report_player_ticket": self.modals.report_player,
            "report_error_ticket": self.modals.report_error,
            "contact_ticket": self.modals.contact
        }

    def create(self):
        self.service_view = ButtonCreator(
            button("Zajmij", discord.ButtonStyle.green, emoji="🏷️", custom_id="claim_ticket", row=0),
            button("Zamknij", discord.ButtonStyle.red, emoji="✖️", custom_id="close_ticket", row=0),
            callback=self.callback,
            persistent=True,
            bot=self.bot
        )

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

            elif custom_id == "claim_ticket":
                await interaction.response.defer()
                thread = interaction.channel if isinstance(interaction.channel, discord.Thread) else None
                if thread is None: return
                await thread.edit(locked=True)
                
                # Pobierz rangę Ticket
                ticket_role = interaction.guild.get_role(config['Tickets.ticket_role_id'])
                if not ticket_role: return
                
                # Usuń członków z rangą Ticket (oprócz tej osoby)
                for member in thread.members:
                    if member.id != interaction.user.id:
                        # Pobierz pełny obiekt Member (thread.members zwraca ThreadMember bez roles)
                        full_member = interaction.guild.get_member(member.id)
                        if full_member and ticket_role in full_member.roles:
                            try:
                                await thread.remove_user(member)
                                await asyncio.sleep(1)  # 1 sekunda między usuwaniem
                            except Exception as e:
                                print(f"Nie mogę usunąć {member}: {e}")
                                
                # Wyłącz przycisk "Zajmij" w wiadomości interakcji
                try:
                    # Wyłącz przycisk
                    for item in self.service_view.children:
                        if hasattr(item, 'custom_id') and item.custom_id == 'claim_ticket':
                            item.disabled = True
                    
                    # Edytuj wiadomość z wyłączonym przyciskiem
                    await interaction.message.edit(view=self.service_view)

                except Exception as e:
                    print(f"Błąd edycji wiadomości: {e}")

                await thread.edit(slowmode_delay=0, locked=False)
                await thread.send(embed=EmbedCreator(title=f"✅ **{interaction.user.display_name}** zajął ticket!", color=discord.Color.green()))

            else:
                await interaction.response.send_message("Nieznany przycisk.", ephemeral=True)

        except Exception as e:
            print(f"Error in callback: {e}")
    