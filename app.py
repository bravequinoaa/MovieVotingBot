from pymongo import MongoClient
import pprint

from db.DataController import DataController 
from omdbAPIController import omdbAPIController


class App:
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

    def submitAddMovie(self, title: str = None, imdbID: str = None):
        # Adds a movie to the db or if already present, adds a vote
        movieInfo = self.__searchMovie(title, imdbID)
        print(movieInfo)
        movie = self.dc.submit(movieInfo)
        return movie
        # Then pass to discord bot

    def submitRemoveVote(self, title: str = None, imdbID: str = None):
        # Checks if user voted for a certain movie
        # removes vote from movie
        # removes movie from user.votedMovies
        movie = self.dc.submitRemoveVote(title, imdbID)
        if movie == None:
            print("Movie not found")
            return
        print("Vote removed")

    def removeMovie(self, title: str = None, imdbID: str = None):
        # Remove movie from db if done by owner or to be called when Movie.Votes = 0
        pass

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

    def __str__(self):
        return "HELLO WORLD"


if __name__=="__main__":
    app = App()
    print(app)
    app.test()

    
