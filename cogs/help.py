from discord.ext import commands
from DiscordBot import BOT_PREFIX

class Help(commands.Cog, name='Help'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        link = 'https://docs.google.com/spreadsheets/d/11aLjflonVWJsDXZwvDkJLNXK7DROmStpTNDQc-Q4DV0/edit?usp=sharing'
        await ctx.message.channel.send(link)

def setup(bot):
    bot.add_cog(Help(bot))
