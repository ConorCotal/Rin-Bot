import discord
from discord import app_commands
from discord.ext import commands


class RemoveDebug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="removedebug", description="Usuń wszystkie wątki, które mają prefix [DEBUG].")
    @app_commands.default_permissions(manage_threads=True, manage_channels=True)
    async def remove_debug(self, interaction: discord.Interaction):
        prefix = "[debug]"
        count = 0

        if interaction.guild is None:
            await interaction.response.send_message("Ta komenda musi być użyta na serwerze.", ephemeral=True)
            return

        for thread in interaction.guild.threads:
            if thread.name.lower().startswith(prefix):
                try:
                    await thread.delete()
                    count += 1
                except Exception:
                    pass

        await interaction.response.send_message(f"Usunięto {count} wątków z prefixem [DEBUG].")


async def setup(bot):
    await bot.add_cog(RemoveDebug(bot))
