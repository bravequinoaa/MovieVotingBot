import sys
from mongoengine import *
from pymongo import * 

from db.models.Movie import Movie

class DataController:
    def __init__(self, Host: str, Port: int, client: MongoClient):
        self.client = client
        self.db = self.client['Movies']
        self.col = self.db['movie']
        connect(db='Movies', host=Host, port=Port)

    def submit(self, movieInfo: dict, voter=None):
        if self.__findMovieDB(imdbID = movieInfo['imdbID']) == None:
            self.__createMovie(movieInfo)

        self.__incVote(movieInfo['imdbID'])
        movie = self.__findMovieDB(imdbID = movieInfo['imdbID'])
        return movie
    
    def submitRemoveVote(self, title: str = None, imdbID: str = None):
        movie = self.__findMovieDB(title, imdbID)
        if movie == None:
            return movie 
        imdbID = movie['imdbID']
        self.__decVote(movie['imdbID'])
        return self.__findMovieDB(imdbID=movie['imdbID'])

    def submitRemoveMovie(self, title: str = None, imdbID: str = None):
        movie = self.__findMovieDB(imdbID=imdbID, title=title)
        if movie == None:
            return movie
        if movie['Votes'] != 0:
            return movie 

        self.__removeMovie(movie['imdbID'])
        return None


    def __createMovie(self, movieInfo: dict, voter: str = 'ADMIN') ->  Movie:
        movie = Movie()
        movie.Title = movieInfo['Title']
        movie.imdbID = movieInfo['imdbID']
        movie.Rating = movieInfo['imdbRating']
        movie.Genre = movieInfo['Genre']
        movie.Runtime = movieInfo['Runtime']
        movie.Rated = movieInfo['Rated']
        movie.voter = voter
        movie.save() 

        return movie

    def __removeMovie(self, imdbID: str):
        # remove movie by ID
        self.col.delete_one( {'imdbID': imdbID} )

    def __findMovieDB(self, title: str = None, imdbID: str = None):
        # return movie entry based on title
        movie = None
        if title != None:
            movie = self.col.find({ 'Title': title })
        if imdbID != None:
            movie = self.col.find( {'imdbID': imdbID})
        if movie.count() == 0: return None

        return movie.next()

    def __incVote(self, imdbID: str):
        # Incremement movie vote by 1 based on imdbID
        self.col.update_one({"imdbID": imdbID}, {"$inc": {"Votes": 1}})

    def __decVote(self, imdbID: str):
        # Incremement movie vote by 1 based on imdbID
        self.col.update_one({"imdbID": imdbID}, {"$inc": {"Votes": -1}})

    def getTopMovies(self):
        # need to limit to unique movies
        returnarr = []
        i = 0
        for doc in self.db.movie.find():
            while i < 3:
                i+=1
                returnarr.append(doc)
        return returnarr 
