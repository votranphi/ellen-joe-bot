import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class EllenJoeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=intents, help_command=None)

    async def setup_hook(self):
        await self.load_extension('src.cogs.admin')
        await self.load_extension('src.cogs.bridge')
        await self.load_extension('src.cogs.chat')
        print("✅ Extensions Loaded")

    async def on_ready(self):
        print(f'Logged in as {self.user}')

bot = EllenJoeBot()

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))