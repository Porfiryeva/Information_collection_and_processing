from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['insta_follow']


name = 'techskills_2022'

# подписчики только указанного пользователя
for follower in db[name].find({'in_follower': True}):
    pprint(follower)

# подписки только указанного пользователя
for following in db[name].find({'in_following': True}):
    pprint(following)
