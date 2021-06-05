import requests
from requests.exceptions import HTTPError
import os
import json

class omdbAPIController:
    def __init__(self):
        self.key = os.getenv('OMDB_API_KEY')

    def getMovie(self, title: str = None, imdbID: str = None):
        request = self.__createRequests(title, imdbID)
        response = self.__sendRequests(request)
        cleanedJSON = self.__cleanJSON(response.json())
        #print(cleanedJSON)
        return cleanedJSON 

    def __createRequests(self, title: str = None, imdbID: str = None):
        request = f'http://www.omdbapi.com/?apikey={self.key}'
        params = {}

        # might be a better way to build params
        if title != None:
            params['t'] = title
        if imdbID != None:
            params['i'] = imdbID

        for key, val in params.items():
            request += f'&{key}={val}'
        return request

    def __sendRequests(self, request):
        try:
           response = requests.get(request)
        except HTTPError as http_err:
            pass
        except Exception as err:
            pass
        else:
            return response

    def __cleanJSON(self, json):
        returndict = {}
        fields = ['Title', 'imdbID', 'imdbRating', 'Genre', 'Runtime', 'Rated']

        for field in fields:
            if field == 'Genre':
                genreList = self.__cleanGenre(json[field])
                returndict[field] = genreList
            else:
                returndict[field] = json[field]


        return returndict

    def __cleanGenre(self, genres: str):
        genrearr = genres.replace(' ', '').split(',')
        return genrearr


if __name__=="__main__":
    controller = omdbAPIController()
    res = controller.getMovie(title='Shrek')
    print(res)

    


