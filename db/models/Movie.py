from mongoengine import *
import datetime

class Movie(Document):
    # Movie Data taken from OMDB API 
    Title = StringField(max_length=200, required=True)
    imdbID = StringField(max_length=50, required=True)
    Rating = StringField(max_length=4)
    Genre = ListField(field=StringField())
    Runtime = StringField(max_length=10)
    Rated = StringField(max_length = 5)
    Creator = StringField(max_length=200, required=True, default='ADMIN')
    Voters = ListField(field=StringField(), default=[])
    Votes = IntField(default=0)
    date_added = DateTimeField(default=datetime.datetime.now(), required=True)

