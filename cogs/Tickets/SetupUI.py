import discord
from discord.ext import commands
from .UI.Buttons import Buttons

class SetupUI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.buttons = Buttons(bot)

        self.service_view = None
        self.mc_view = None
        self.other_view = None

    async def cog_load(self):
        self.buttons.create()
        await self.buttons.modals.create()
        self.service_view = self.buttons.service_view
        self.mc_view = self.buttons.mc_view
        self.other_view = self.buttons.other_view


async def setup(bot):
    await bot.add_cog(SetupUI(bot))