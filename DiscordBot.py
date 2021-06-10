import os
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from MovieVotingSystem import MovieVotingSystem

# DISCORD CONFIG
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = "$"

intents = discord.Intents.default()
bot = Bot(command_prefix=BOT_PREFIX, intents=intents)

mvs = MovieVotingSystem()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello {message.author}')
    if message.content.startswith('$'):
        await bot.process_commands(message)

if __name__ == "__main__":
    # Load Cogs
    cogs = ['test', 'MovieVoting']
    for cog in cogs:
        try:
            bot.load_extension(f"cogs.{cog}")
            print(f"loaded cog '{cog}'")
        except Exception as e:
            print(f"Failed to load extension {cog}\n{e}")

    bot.run(DISCORD_TOKEN)
