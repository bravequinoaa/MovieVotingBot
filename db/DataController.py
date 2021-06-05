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
        if self.__findMovieByID(movieInfo['imdbID']) == None:
            print("Creating")
            self.__createMovie(movieInfo)

        self.__incVote(movieInfo['imdbID'])
        movie = self.__findMovieByID(movieInfo['imdbID'])
        return movie
    
    def submitRemoveVote(self, title: str = None, imdbID: str = None):
        movie = self.__getMovieID(imdbID, title)
        if movie == None:
            return movie 
        imdbID = movie['imdbID']
        print('imdbID: ', imdbID)
        self.__decVote(movie['imdbID'])
        return self.__findMovieByID(movie['imdbID'])


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

    def __getMovieID(self, imdbID: str = None, title: str = None):
        movie = None
        if imdbID != None:
            movie = self.col.find( {'imdbID': imdbID}, {imdbID: 1} )
        if title != None:
            movie = self.col.find( {'Title': title}, {imdbID: 1} )
        if movie.count() == 0:
            return None
        print("ID GOT")
        return movie.next()       

    def __removeMovie(self, imdbID: str):
        # remove movie by ID
        self.col.delete( {'imdbID': imdbID} )

    def __findMovieByTitle(self, title: str):
        # return movie entry based on title
        movie = self.col.find({ 'Title': title })
        
        if movie.count() == 0: return None
        else: return movie.next()

    def __findMovieByID(self, imdbID: str):
        # return movie entry based on imdbID
        movie = self.col.find({ 'imdbID': imdbID })
        
        if movie.count() == 0: return None
        else: return movie.next()

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
