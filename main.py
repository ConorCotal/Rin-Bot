import discord
from dotenv import load_dotenv
from discord.ext import commands
import os
from pathlib import Path

load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = '!',
            intents = discord.Intents.all()
            )

    async def setup_hook(self):
        for file_path in Path('cogs').rglob('*.py'):
            if any(part.startswith('.') for part in file_path.parts):
                continue

            module_name = '.'.join(file_path.with_suffix('').parts)

            try:
                await self.load_extension(module_name)
            except commands.NoEntryPointError:
                pass
            except Exception as e:
                print(f"Bląd w pliku {module_name}: {e}")

        if os.getenv('GUILD_ID'):
            test_guild = discord.Object(id=int(os.getenv('GUILD_ID')))

            self.tree.copy_global_to(guild=test_guild)

            await self.tree.sync(guild=test_guild)
        else:
            await self.tree.sync()

    async def on_ready(self):
        print('done')

bot = Bot()
bot.run(os.getenv('TOKEN'))
