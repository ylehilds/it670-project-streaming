import auth
import pymongo  # pip install pymongo
import traceback
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import json
import re

# import nltk
# nltk.download('movie_reviews')
# nltk.download('punkt')

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def save_to_mongo(tweet, mongo_db, mongo_db_coll, **mongo_conn_kw):
    # Connects to the MongoDB server running on
    # localhost:27017 by default

    client = pymongo.MongoClient(**mongo_conn_kw)

    # Get a reference to a particular database

    db = client[mongo_db]

    # Reference a particular collection in the database

    coll = db[mongo_db_coll]

    description = tweet.user.description
    loc = tweet.user.location
    text = tweet.text
    coords = tweet.coordinates
    geo = tweet.geo
    name = tweet.user.screen_name
    user_id = tweet.user.id_str
    user_name = tweet.user.name
    user_created = tweet.user.created_at
    followers = tweet.user.followers_count
    id_str = tweet.id_str
    created = tweet.created_at
    retweets = tweet.retweet_count
    favorites = tweet.favorite_count
    bg_color = tweet.user.profile_background_color
    blob = TextBlob(text)
    # blob2 = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    sent = blob.sentiment
    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", tweet.text)
    print(text)

    media_files = set()
    medias = tweet.entities.get('media', [])
    if (len(medias) > 0):
        for media in medias:
            media_files.add(media['media_url'])
    if media_files is not None:
        images = " ".join(str(x) for x in media_files)

    # candidate_sentiment = sentiment_classification(sent.polarity)
    # candidate_sentiment = sentiment_classification_naive_bayes_analyzer(blob2.sentiment)
    candidate_sentiment = vader_sentiment_analyzer_scores(text)
    # import wget
    # for media_file in media_files:
    #     wget.download(media_file)

    candidate = candidate_selection(text)
    if url is not None:
        url = " ".join(str(x) for x in url)

    if geo is not None:
        geo = json.dumps(geo)

    if coords is not None:
        coords = json.dumps(coords)

    # Perform a bulk insert and  return the IDs
    try:
        return coll.insert(
            {"tweet_id": id_str, "user_id": user_id, "user_name": user_name,
             "text": tweet.text, "candidate": candidate, "url": url, "retweet_count": retweets, "favorite_count": favorites,
             "polarity": sent.polarity, "subjectivity": sent.subjectivity, "sentiment": candidate_sentiment, "description": description,
             "location": loc, "coords": coords, "geo": geo, "name": name, "user_created": user_created,
             "followers": followers, "created": created, "bg_color": bg_color, "images": images})
    except Exception:
        traceback.print_exc()
        print('error inserting a tweet')
        # return coll.insert_one(data)

def sentiment_classification(polarity):
    sentiment = float(polarity)
    if sentiment < 0:
        return 'negative'
    if sentiment == 0:
        return 'neutral'
    if sentiment > 0:
        return 'positive'

def sentiment_classification_naive_bayes_analyzer(sentiment):
    if sentiment.classification == 'neg':
        return 'negative'
    if sentiment.classification == 'neu':
        return 'neutral'
    if sentiment.classification == 'pos':
        return 'positive'

def vader_sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))
    if score['compound'] <= -0.05:
        return 'negative'
    if -0.05 < score['compound'] < 0.05:
        return 'neutral'
    if score['compound'] >= 0.05:
        return 'positive'

def candidate_selection(text):
    if text.lower().count('donald') or text.lower().count('trump'):
        return 'Donald Trump'
    if text.lower().count('bill') or text.lower().count('weld'):
        return 'Bill Weld'
    if text.lower().count('joe') or text.lower().count('walsh'):
        return 'Joe Walsh'
    if text.lower().count('roque') or text.lower().count('fuente'):
        return 'Roque De La Fuente'
    if text.lower().count('joe') or text.lower().count('biden'):
        return 'Joe Biden'
    if text.lower().count('michael') or text.lower().count('bennet'):
        return 'Michael Bennet'
    if text.lower().count('michael') or text.lower().count('bloomberg'):
        return 'Michael Bloomberg'
    if text.lower().count('cory') or text.lower().count('booker'):
        return 'Cory Booker'
    if text.lower().count('pete') or text.lower().count('buttigieg'):
        return 'Pete Buttigieg'
    if text.lower().count('bernie') or text.lower().count('sanders'):
        return 'Bernie Sanders'
    else:
        return 'Inconclusive'

def load_from_mongo(mongo_db, mongo_db_coll, return_cursor=False,
                    criteria=None, projection=None, **mongo_conn_kw):
    # Optionally, use criteria and projection to limit the data that is
    # returned as documented in
    # http://docs.mongodb.org/manual/reference/method/db.collection.find/

    # Consider leveraging MongoDB's aggregations framework for more
    # sophisticated queries.

    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]

    if criteria is None:
        criteria = {}

    if projection is None:
        cursor = coll.find(criteria)
    else:
        cursor = coll.find(criteria, projection)

    # Returning a cursor is recommended for large amounts of data

    if return_cursor:
        return cursor
    else:
        return [item for item in cursor]

# Sample usage

# q = 'CrossFit'
#
# twitter_api = auth.oauth_login()
# results = search.twitter_search(twitter_api, q, max_results=10)
#
# ids = save_to_mongo(results, 'search_results', q, host='mongodb://localhost:27017')
#
# load_from_mongo('search_results', q, host='mongodb://localhost:27017')
