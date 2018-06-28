from mongoengine import *
connect('top_scores', host='localhost', port=27017)


import datetime

class Post(Document):
    name = StringField(required=True, max_length=200)
    score = IntField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)



    #print(post_1.title)
    #post_1.title = 'A Better Post Title'
    #post_1.save()       # This will perform an atomic edit on "title"
    #print(post_1.title)
