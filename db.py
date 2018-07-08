from mongoengine import *
connect('isla', host='localhost', port=27017)

import datetime


class NamDB(Document):
    name = StringField(required=True, max_length=200)

class ScoDB(Document):
    score = IntField(required=True, max_length=50)
