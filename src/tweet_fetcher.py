import tweepy
import os
from datetime import date

# consumer keys and access tokens used by OAuth
consumer_token = 'dXlF7WS3knOkX9BGNOKmXfwIP'
consumer_secret = 'qXoIqrfVbwPvrVgKt8GRSMQuiMatTGGpa8xaf3TQUo2Ljls2qk'
access_token = '120142660-bWJojyo1vmTzU3xo2LMEJXe38sLAicOGx9MzpE0F'
access_token_secret = 'DhHn5HhJ0vYDTlg7iHLhiECcGzzpV05MOr733HiEWzeed'

# create auth object
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get API
api = tweepy.API(auth)

# search for tweets
query = 'bilkent'
max_tweets = 2

searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # the operation may be retried if the search operation failed.
        break

# Save the tweets found to a subfolder named as the lowercase version of the query string in data directory 
# if no such folder found, create one.
if searched_tweets:

    current_dir = os.getcwd()
    dir_suffix = 'data/' + ''.join(c.lower() for c in query if not c.isspace())
    query_dir = os.path.join(current_dir, dir_suffix)

    if not os.path.exists(query_dir):
        os.mkdir(query_dir)

    # save the query results to a textfile named as today's date 
    today = date.today()
    filename = today.strftime("%B_%d_%Y.txt")
    filepath = os.path.join(query_dir, filename)

    try:
        f = open(filepath, "a")
        for tweet in searched_tweets:
            line = tweet.text
            # all tweets in the text file are separated by three newlines.
            f.write(line + "\n\n\n")
    finally:
        f.close()





