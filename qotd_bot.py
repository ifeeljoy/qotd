import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import time
import asyncio
from dotenv import load_dotenv

load_dotenv()

GUILD_ID = int(os.getenv("GUILD_ID"))
REVIEW_CHANNEL_ID = int(os.getenv("REVIEW_CHANNEL_ID"))
QOTD_CHANNEL_ID = int(os.getenv("QOTD_CHANNEL_ID"))
PING_ROLE_ID = int(os.getenv("PING_ROLE_ID"))

DATA_FILE = "data.json"
COOLDOWN_SECONDS = 24 * 60 * 60
APPROVE_EMOJI = "✅"
DENY_EMOJI = "❌"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "last_post_time": 0,
        "submissions": {},
        "queue": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()
        self.auto_post.start()

    @app_commands.command(name="submit", description="Submit a Question of the Day")
    async def submit(self, interaction: discord.Interaction, question: str):
        review_channel = interaction.guild.get_channel(REVIEW_CHANNEL_ID)
        if not review_channel:
            await interaction.response.send_message("Review channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Question awaiting review",
            description=question,
            color=discord.Color.orange()
        )
        embed.add_field(name="Submitted by", value=interaction.user.mention)

        msg = await review_channel.send(embed=embed)
        await msg.add_reaction(APPROVE_EMOJI)
        await msg.add_reaction(DENY_EMOJI)

        self.data["submissions"][str(msg.id)] = {
            "question": question,
            "submitter_id": interaction.user.id,
            "handled": False
        }
        save_data(self.data)

        await interaction.response.send_message("Your question has been submitted for review.", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.emoji) not in [APPROVE_EMOJI, DENY_EMOJI]:
            return
        if payload.channel_id != REVIEW_CHANNEL_ID:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None:
            try:
                member = await guild.fetch_member(payload.user_id)
            except discord.NotFound:
                return

        if not member.guild_permissions.manage_guild:
            return

        message_id = str(payload.message_id)
        submission = self.data["submissions"].get(message_id)
        if not submission or submission.get("handled"):
            return

        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        submitter = guild.get_member(submission["submitter_id"])
        question = submission["question"]

        if str(payload.emoji) == APPROVE_EMOJI:
            self.data["queue"].append({
                "question": question,
                "submitter_id": submission["submitter_id"]
            })

            embed = discord.Embed(
                title="Question approved and added to queue",
                description=question,
                color=discord.Color.green()
            )
            embed.add_field(name="Submitted by", value=submitter.mention if submitter else "Unknown")
            embed.add_field(name="Approved by", value=member.mention)
            await message.reply(embed=embed)

        elif str(payload.emoji) == DENY_EMOJI:
            embed = discord.Embed(
                title="Question denied",
                description=question,
                color=discord.Color.red()
            )
            embed.add_field(name="Submitted by", value=submitter.mention if submitter else "Unknown")
            embed.add_field(name="Denied by", value=member.mention)
            await message.reply(embed=embed)

        submission["handled"] = True
        save_data(self.data)

    @tasks.loop(count=1)
    async def auto_post(self):
        while True:
            now = time.time()
            last_post = self.data.get("last_post_time", 0)
            elapsed = now - last_post
            wait_time = COOLDOWN_SECONDS - elapsed

            if len(self.data.get("queue", [])) == 0:
                print("Queue empty. Waiting 10 minutes before checking again.")
                await asyncio.sleep(600)
                continue

            if wait_time > 0:
                print(f"Waiting {int(wait_time)}s until next post...")
                await asyncio.sleep(wait_time)

            guild = self.bot.get_guild(GUILD_ID)
            channel = guild.get_channel(QOTD_CHANNEL_ID)
            role_mention = f"<@&{PING_ROLE_ID}>"

            next_q = self.data["queue"].pop(0)
            question = next_q["question"]

            msg = await channel.send(f"{role_mention}\n**Question of the Day:** {question}")
            self.bot.dispatch("qotd_posted", msg)

            self.data["last_post_time"] = time.time()
            save_data(self.data)

            print("QOTD posted. Waiting 24 hours until next post.")
            await asyncio.sleep(COOLDOWN_SECONDS)

    @auto_post.before_loop
    async def before_auto_post(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(QOTD(bot))
