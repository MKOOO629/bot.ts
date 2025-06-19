import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not set")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Needed to ban members

bot = commands.Bot(command_prefix="!", intents=intents)

# Common English curse words (expand as needed)
cuss_words = {
    "fuck", "shit", "bitch", "asshole", "bastard", "damn", "crap", "piss", "dick", "pussy",
    "cunt", "fag", "slut", "whore", "twat", "cock", "motherfucker", "nigger", "nigga",
    "retard", "spaz", "douche", "bollocks", "bugger", "wanker", "prick", "arse", "tosser",
    "shithead", "douchebag", "jackass", "jerkoff", "son of a bitch"
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg_lc = message.content.lower()
    if any(cuss in msg_lc for cuss in cuss_words):
        try:
            await message.author.ban(reason="Used prohibited language")
            await message.channel.send(f"{message.author.mention} has been banned for using prohibited language!")
        except discord.Forbidden:
            await message.channel.send("I do not have permission to ban this user.")
        except Exception as e:
            await message.channel.send(f"Error banning user: {e}")
        return

    if msg_lc.strip() == "!nuke":
        try:
            await message.author.ban(reason="Used the forbidden !nuke command")
            await message.channel.send(f"{message.author.mention} has been banned for using !nuke!")
        except discord.Forbidden:
            await message.channel.send("I do not have permission to ban this user.")
        except Exception as e:
            await message.channel.send(f"Error banning user: {e}")
        return

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

if __name__ == "__main__":
    bot.run(TOKEN)
