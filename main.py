import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

class QOTDBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False

    async def setup_hook(self):
        await self.load_extension("qotd_bot")
        await self.load_extension("thread_creator")

    async def on_ready(self):
        if not self.synced:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            self.synced = True
        print(f"Bot ready as {self.user}")

bot = QOTDBot()
bot.run(TOKEN)