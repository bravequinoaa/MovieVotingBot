from discord.ext import commands
from discord.utils import get

from DiscordBot import BOT_PREFIX
from random import randint

class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='random', aliases=['r', 'roll'])
    async def random(self, ctx):
        args = self.__parseargs(ctx.message.content)
        if len(args) == 0:
            r = randint(0, 100)
            await ctx.message.channel.send(r)
            return

        try:
            args = [int(a) for a in args]
        except Exception as e:
            await ctx.message.channel.send('Invalid input, please give me ints')

        r = randint(args[0], args[1])
        await ctx.message.channel.send(r)

    @commands.command(name='flip', aliases=['coinflip'])
    async def flip(self, ctx):
        r = randint(0, 1)
        if r == 0:
            await ctx.message.channel.send('TAILS')
            return
        if r == 1:
            await ctx.message.channel.send('HEADS')
            return

    @commands.command(name='meow', aliases=['Meow'])
    async def meow(self, ctx):
        meows = [ 'MEOW', 'meow', 'mrwowwww', 'moo', 'RRRRROWWWW']
        r = randint(0, len(meows)-1)
        await ctx.message.channel.send(meows[r])

    @commands.command(name='bark', aliases=['Woof', 'Bark'])
    async def bark(self, ctx):
        await ctx.message.channel.send('meow')
        
    @commands.command(name='votekick')
    async def votekick(self, ctx):
        arg = self.__parseargs(ctx.message.content)
        arg = ''.join(arg)
        reactions = ['F1', 'F2']
        message = await ctx.message.channel.send(f'Vote Kick: {arg}')
        for r in reactions:
            emoji = get(ctx.guild.emojis, name=r)
            await message.add_reaction(emoji)

    def __parseargs(self, content):
        return content.split(' ')[1:]
        

def setup(bot):
    bot.add_cog(Fun(bot))
