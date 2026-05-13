import discord
from discord.ext import commands
from discord import app_commands

from utils.UI import EmbedCreator

class PanelSend(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="setup-ticket-panel",
        description="Tworzy panel do tworzenia ticketów."
    )
    async def setup_ticket_panel(self, interaction: discord.Interaction):
        setup_ui = self.bot.get_cog('SetupUI')
        if setup_ui is None:
            await interaction.response.send_message("Błąd: SetupUI nie jest załadowany.", ephemeral=True)
            return
        mc_picture = discord.File("images/MC_icon.png", filename="MC_icon.png")
        sep_line = discord.File("images/sep_line.png", filename="sep_line.png")
        other_picture = discord.File("images/DC_icon.png", filename="DC_icon.png")
        mc_ticket = EmbedCreator(
            title="Serwis Minecraft",
            description="> Sprawy związane z serwisem Minecraft.",
            color=discord.Color.dark_green(),
            thumbnail="attachment://MC_icon.png",
        )
        other_ticket = EmbedCreator(
            title="Ogólne",
            description="> Sprawy Ogólne.",
            color=discord.Color.dark_green(),
            thumbnail="attachment://DC_icon.png",
        )

        await interaction.response.send_message("Wysyłanie panelu ticketów...", ephemeral=True)
        await interaction.channel.send(embed=mc_ticket, file=mc_picture, view=setup_ui.mc_view)
        await interaction.channel.send(file=sep_line)
        await interaction.channel.send(embed=other_ticket, file=other_picture, view=setup_ui.other_view)

async def setup(bot):
    await bot.add_cog(PanelSend(bot))