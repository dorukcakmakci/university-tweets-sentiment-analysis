import tweepy
import json
import os
from datetime import date

# consumer keys and access tokens used for Twitter api
consumer_token = 'INSERT'
consumer_secret = 'INSERT'
access_token = 'INSERT'
access_token_secret = 'INSERT'

# create auth object
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get API
api = tweepy.API(auth)

# for automated tweet fetching change INSERT.json 
with open("INSERT.json", 'r') as json_file:
    universities = json.load(json_file)

# search for tweets
for university in universities:
    if university['country'] == "Turkey":
        query = university['name']
        max_tweets = 50

        searched_tweets = []
        last_id = -1
        while len(searched_tweets) < max_tweets:
            count = max_tweets - len(searched_tweets)
            try:
                new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1), tweet_mode='extended')
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
                    # remove retweets from interfering with sentiment analysis result 
                    if 'retweeted_status' not in dir(tweet):
                        line = tweet.full_text
                        # all tweets in the text file are separated by three newlines.
                        f.write(line + "\n\n\n")
            finally:
                print(query) 
