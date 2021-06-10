from discord.ext import commands
from DiscordBot import BOT_PREFIX

class Test(commands.Cog, name="Test"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        print(ctx)


def setup(bot):
    bot.add_cog(Test(bot))
