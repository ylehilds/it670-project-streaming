import settings
import tweepy
import csv
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import mongo_db_hughes

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.retweeted:
            return
        try:
            mongo_db_hughes.save_to_mongo(status, 'thanksgiving', 'stream', host='mongodb://localhost:27017')
        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS)
# stream.filter(locations=settings.LOCATION_TERMS)
