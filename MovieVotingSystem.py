from pymongo import MongoClient
import pprint

from db.DataController import DataController 
from omdbAPIController import omdbAPIController


class MovieVotingSystem:
    def __init__(self):
        host = 'localhost'
        port = 27017

        # Mongo DB Set up
        self.client = MongoClient(host, port)
        self.db = self.client['Movies']
        self.col = self.db['movie']

        # Core Objects 
        self.dc = DataController(host, port, self.client)
        self.omdb = omdbAPIController()

        # Supplementary
        self.pp = pprint.PrettyPrinter(indent=4)

    def submitAddMovie(self, ctx, title: str = None, imdbID: str = None):
        # Adds a movie to the db or if already present, adds a vote
        movieInfo = self.__searchMovie(title, imdbID)
        movie = self.dc.submit(ctx, movieInfo)

        if movie == None: 
            print(f"Failed to create movie: {title}")
            return 1 
        if movie == 1:
            print(f"Movie already created/you have already voted for this movie: {title}")
            return 2

        print(f"Movie Created: {movie['Title']}")
        return movie

    def submitRemoveVote(self, ctx, title: str = None, imdbID: str = None):
        # Checks if user voted for a certain movie
        # removes vote from movie
        # removes movie from user.votedMovies
        movie = self.dc.submitRemoveVote(ctx, title, imdbID)
        if movie == 1:
            print(f"Movie not found: {title}")
            return 1
        if movie == 2:
            print(f"{ctx.message.author} is not a voter on this movie")
            return 2
        return movie

    def removeMovie(self, ctx, title: str = None, imdbID: str = None):
        # Remove movie from db if done by owner or to be called when Movie.Votes = 0
        movie = self.dc.submitRemoveMovie(ctx, title=title, imdbID=imdbID)
        if movie == 0:
            print(f"Movie Removed: {title}")
            return 0
        if movie == 1:
            print(f'Movie not found: {title}')
            return 1
        if movie == 2:
            print(f'Movie still has votes: {title}')
            return 2
        if movie == 3:
            print(f'Not movie creator: {title}, author: {ctx.message.author}')
            return 3

        print(f"Unable to remove movie, votes still exists: {title}")


    def __printMovies(self):
        self.pp.pprint(self.dc.getMovies())

    def __createMovie(self, movieInfo: dict):
        self.dc.createMovie(title)

    def __searchMovie(self, title: str = None, imdbID: str = None):
        movieDict = self.omdb.getMovie(title, imdbID)
        return movieDict

    def test(self):
        movie1 = self.submitAddMovie("Spy Kids")
        movie2 = self.submitAddMovie("Hereditary")
        movie3 = self.submitAddMovie("Hereditary")
        movie4 = self.submitAddMovie("House")
        self.submitRemoveVote(title="POOP")
        self.submitRemoveVote(title="Hereditary")
        self.submitRemoveVote(title="Spy Kids")
        self.removeMovie(title="Spy Kids")


if __name__=="__main__":
    mvs = MovieVotingSystem()
    mvs.test()

    
