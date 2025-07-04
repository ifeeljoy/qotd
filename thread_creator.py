import discord
from discord.ext import commands
from datetime import datetime

class ThreadCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_qotd_posted(self, message: discord.Message):
        # Make sure this was sent in the QOTD channel
        if message.channel.id != int(os.getenv("QOTD_CHANNEL_ID")):
            return

        date_str = datetime.now().strftime("%B %d, %Y")
        thread_name = f"QOTD • {date_str}"

        try:
            await message.create_thread(name=thread_name, auto_archive_duration=1440)
        except discord.HTTPException as e:
            print(f"Failed to create thread: {e}")

async def setup(bot):
    await bot.add_cog(ThreadCreator(bot))