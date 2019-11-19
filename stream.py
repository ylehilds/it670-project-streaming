# Find topics of interest by using the filtering capabilities the API offers

import sys
import twitter
from auth import oauth_login
import mongo_db

# Query terms

q = 'thanksgiving' # Comma-separated list of terms

print('Filtering the public timeline for track={0}'.format(q), file=sys.stderr)
sys.stderr.flush()

# Returns an instance of twitter.Twitter
twitter_api = oauth_login()

# Reference the self.auth parameter
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# See https://developer.twitter.com/en/docs/tutorials/consuming-streaming-data
stream = twitter_stream.statuses.filter(track=q)

# For illustrative purposes, when all else fails, search for Justin Bieber
# and something is sure to turn up (at least, on Twitter)

for tweet in stream:
    print(tweet['text'])
    mongo_db.save_to_mongo(tweet, 'mytest', 'stream', host='mongodb://localhost:27017')
    sys.stdout.flush()

    # Save to a database in a particular collection