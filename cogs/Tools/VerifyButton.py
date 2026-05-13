import discord
from discord.ext import commands
from discord import app_commands

from utils.UI import ButtonCreator, button

class VerifyButton(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_view = None

    async def cog_load(self):
        self.persistent_view = ButtonCreator(
            button("Akcjeptuje Regulamin", discord.ButtonStyle.green, custom_id="rules_accept"),
            callback=self.callback,
            persistent=True,
            bot=self.bot
        )

    @app_commands.command(
        name="send-verify-button",
        description="Wysyła przycisk do weryfikacji."
    )
    async def send_verify_button(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test", view=self.persistent_view)

    async def callback(self, interaction: discord.Interaction):
        if interaction.data["custom_id"] == "rules_accept":
            # role = discord.utils.get(interaction.guild.roles, name="Zweryfikowany")
            # await interaction.user.add_roles(role)
            await interaction.response.send_message("Pomyślnie zweryfikowano!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerifyButton(bot))