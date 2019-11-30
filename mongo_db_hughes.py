import auth
import pymongo  # pip install pymongo
import traceback
from textblob import TextBlob
import json
import re

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
    user_created = tweet.user.created_at
    followers = tweet.user.followers_count
    id_str = tweet.id_str
    created = tweet.created_at
    retweets = tweet.retweet_count
    bg_color = tweet.user.profile_background_color
    blob = TextBlob(text)
    sent = blob.sentiment
    url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", tweet.text)
    print(text)

    if url is not None:
        url = " ".join(str(x) for x in url)

    if geo is not None:
        geo = json.dumps(geo)

    if coords is not None:
        coords = json.dumps(coords)

    # Perform a bulk insert and  return the IDs
    try:
        return coll.insert(
            {"tweet_id": tweet.id_str, "user_id": tweet.user.id_str, "user_name": tweet.user.name,
             "text": tweet.text, "url": url, "retweet_count": retweets, "favorite_count": tweet.favorite_count,
             "polarity": sent.polarity, "subjectivity": sent.subjectivity, "description": description,
             "location": loc, "coords": coords, "geo": geo, "name": name, "user_created": user_created,
             "followers": followers, "created": created, "bg_color": bg_color})
    except Exception:
        traceback.print_exc()
        print('error inserting a tweet')
        # return coll.insert_one(data)


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
