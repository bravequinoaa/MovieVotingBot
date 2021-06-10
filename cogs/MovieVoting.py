from discord.ext import commands

from MovieVotingSystem import MovieVotingSystem
from DiscordBot import BOT_PREFIX

class MovieVoting(commands.Cog, name="MovieVoting"):
    def __init__(self, bot):
        self.bot = bot
        self.mvs = MovieVotingSystem()

    @commands.command(name="vote", aliases=['votemovie', 'movievote', 'v'])
    async def voteMovie(self, ctx):
        arg = self.__parseArgs(ctx.message.content)
        movie = self.mvs.submitAddMovie(ctx, title=arg)

        if movie == 1: 
            await ctx.message.channel.send(f"Unable to create movie: {arg}")
        elif movie == 2:
            await ctx.message.channel.send(f"You are already a voter on movie: {arg}")
        elif movie == None:
            print("An Error occurred: voteMovie()")
        else:
            await ctx.message.channel.send(f"{movie['Title']}: {movie['Votes']} vote(s)\nCreator: {movie['Creator'].split('#')[0]}")

    @commands.command(name="removevote", aliases=['voteremove', 'rv'])
    async def removeVote(self, ctx):
        arg = self.__parseArgs(ctx.message.content)
        movie = self.mvs.submitRemoveVote(ctx, title=arg)

        if movie == 1:
            await ctx.message.channel.send(f"Movie: {arg} not found")
        elif movie == 2: 
            await ctx.message.channel.send(f"You are not a voter on this movie: unable to remove vote")
        elif movie == None:
            print("An Error occured: removeVote()")
        else:
            await ctx.message.channel.send(f"{movie['Title']}: {movie['Votes']} vote(s)\nCreator: {movie['Creator'].split('#')[0]}")

    @commands.command(name="removemovie", aliases=['movieremove', 'rm'])
    async def removeMovie(self, ctx):
        arg = self.__parseArgs(ctx.message.content)
        movie = self.mvs.submitRemoveMovie(ctx, title=arg)



    @commands.command(name="top", aliases=['topmovies', 't'])
    async def top(self, ctx):
        pass

    @commands.command(name="uservotes", aliases=['uservoted', 'uv'])
    async def userVotes(self, ctx):
        pass

    @commands.command(name="usermovies", aliases=['um'])
    async def userMovies(self, ctx):
        pass

    @commands.command(name="printinfo")
    async def printinfo(self, ctx):
        print(ctx.message.content)
        print(ctx.author)
        print(ctx.guild)
        print(ctx.channel)
        pass

    def __parseArgs(self, content):
        c = content.split(" ")[1:]
        print(c)
        return ' '.join(c)

def setup(bot):
    bot.add_cog(MovieVoting(bot))
