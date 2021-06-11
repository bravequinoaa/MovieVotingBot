import sys
from mongoengine import *
from pymongo import * 

from db.models.Movie import Movie

class DataController:
    def __init__(self, Host: str, Port: int, client: MongoClient):
        self.client = client
        self.db = self.client['Movies']
        self.movieCol = self.db['movie']
        connect(db='Movies', host=Host, port=Port)

    def submit(self, ctx, movieInfo: dict, voter=None):
        movie = self.__findMovieDB(imdbID = movieInfo['imdbID'])
        if movie == None:
            movie = self.__createMovie(movieInfo, voter=ctx.message.author)

        if self.__checkVoter(ctx.message.author, movie):
            self.__incVote(ctx.message.author, movieInfo['imdbID'])
            return self.__findMovieDB(imdbID = movieInfo['imdbID'])
        else:
            return 1
    
    def submitRemoveVote(self, ctx, title: str = None, imdbID: str = None):
        movie = self.__findMovieDB(title, imdbID)
        if movie == None:
            return movie 
        if not self.__checkVoter(ctx.message.author, movie):
            imdbID = movie['imdbID']
            self.__decVote(ctx.message.author, movie['imdbID'])
            return self.__findMovieDB(imdbID=movie['imdbID'])
        return 1

    def submitRemoveMovie(self, ctx, title: str = None, imdbID: str = None):
        movie = self.__findMovieDB(imdbID=imdbID, title=title)
        if movie == None:
            return 1
        if movie['Votes'] != 0:
            return 2 
        if movie['Creator'] != str(ctx.message.author):
            return 3

        self.__removeMovie(movie['imdbID'])
        return 0 

    def __createMovie(self, movieInfo: dict, voter: str = 'ADMIN') ->  Movie:
        movie = Movie()
        movie.Title = movieInfo['Title']
        movie.imdbID = movieInfo['imdbID']
        movie.Rating = movieInfo['imdbRating']
        movie.Genre = movieInfo['Genre']
        movie.Runtime = movieInfo['Runtime']
        movie.Rated = movieInfo['Rated']
        movie.Creator = str(voter)
        movie.save() 

        return movie

    def __removeMovie(self, imdbID: str):
        # remove movie by ID
        self.movieCol.delete_one( {'imdbID': imdbID} )

    def __findMovieDB(self, title: str = None, imdbID: str = None):
        # return movie entry based on title or imdbID
        movie = None
        if title != None:
            movie = self.movieCol.find({ 'Title': title })
        if imdbID != None:
            movie = self.movieCol.find( {'imdbID': imdbID})
        if movie.count() == 0: return None

        return movie.next()

    def __incVote(self, author, imdbID: str):
        # Incremement movie vote by 1 based on imdbID
        self.movieCol.update_one({"imdbID": imdbID}, {"$inc": {"Votes": 1}})
        self.movieCol.update_one({"imdbID": imdbID}, {"$push": {"Voters": str(author)}})

    def __decVote(self, author, imdbID: str):
        # Deincrement movie vote by 1 based on imdbID
        self.movieCol.update_one({"imdbID": imdbID}, {"$inc": {"Votes": -1}})
        self.movieCol.update_one({"imdbID": imdbID}, {"$pull": {"Voters": str(author)}})

    def __checkVoter(self, author, movie):
        if author in movie['Voters']:
            return True
        else: return False
        

    def getTopMovies(self):
        # need to limit to unique movies
        returnarr = []
        i = 0
        for doc in self.db.movie.find():
            while i < 3:
                i+=1
                returnarr.append(doc)
        return returnarr 
