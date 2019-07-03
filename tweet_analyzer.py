import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from langdetect import detect
from google.cloud import translate

import os

# nltk modules for preprocessing and sentiment classification
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')

# sentiment analyzer function
def sentiment_scores(sentence):

    sentimentAnalyzer = SentimentIntensityAnalyzer()
    sentimentDict = sentimentAnalyzer.polarity_scores(sentence)

    print("Overall Sentiment Dictionary is: ", sentimentDict)
    print("Sentiment is rated as ", sentimentDict['neg'] * 100, "% negative.")
    print("Sentiment is rated as ", sentimentDict['neu'] * 100, "% neutral.")
    print("Sentiment is rated as ", sentimentDict['pos'] * 100, "% positive.")
    print("Sentence Overall Rated As", end = " ") 
  
    if sentimentDict['compound'] >= 0.05 : 
        print("Positive") 
    elif sentimentDict['compound'] <= - 0.05 : 
        print("Negative") 
    else : 
        print("Neutral") 

# file operations to find tweets
current_dir = os.getcwd()
prefix = 'data/'
uni_name = input("Enter a university name(lowercase and abbreviation if possible): ")
date = input("Enter the date of tweets to be processed(formatted as Month_day_year where Month is a word, day and year are numbers): ")
path = os.path.join(current_dir, prefix, uni_name, date)
tweet_file = open(path, 'r')
tweets = tweet_file.read().split('\n\n\n') 


# tweet preprocessing for sentiment analysis 
stop_words = set(stopwords.words('english'))
translate_client = translate.Client()

for tweet in tweets:

    # tweet language detection
    tweet_language = detect(tweet)
    
    if tweet_language != "en":
        tweet = translate_client.translate(tweet, target_language='en', model=translate.NMT)
        tweet = tweet['translatedText']

    tweet = word_tokenize(tweet)
    filtered_tweet = [w for w in tweet if w not in stop_words]
    tweet = ''.join(str(ele + ' ') for ele in filtered_tweet)

    print("Current Tweet: ", tweet)
    
    # sentiment analysis with vader sentiment analyzer
    sentiment_scores(tweet)







