import tweepy
import logging
from tweepy import parsers
import numpy as np
import pandas as pd
import re
from textblob import TextBlob

logging.basicConfig(level=logging.DEBUG)

access_token = "835499518225444864-QQZBLOfwSzkC85NEWEbFNAj4vywjlQe"
access_token_secret = "3eRJZj9cHfHiz0rIhZsvLdC7hU9GCJcSoHwgPaUR2Hcuq"
consumer_key = "5ILWz2QmpSPppTSOwdMvj2q5a"
consumer_secret = "rKjQ8KB5QYdkq6a3Ab29n6ydc9N6YjezpdDzcALTOXaxPV1nDN"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Generating list of all public tweets from timeline
public_tweets = api.home_timeline()

# Creating dataframe for holding data
tweets_df = pd.DataFrame()
# Collecting Data:
i = 1
for tweets in public_tweets:
    print('{} tweets added'.format(i))
    Temp_text = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets['text'])

    input_data = {
        'created_at': tweets['created_at'],
        'text': Temp_text,
        'hashtags': tweets['entities']['hashtags'],
        'source': tweets['source']
    }
    temp_df = pd.DataFrame(columns=['created_at', 'text', 'hashtags', 'source'], data=input_data)
    tweets_df = pd.concat([tweets_df, temp_df])
    i = i + 1


# Finding sentiment analysis (+ve, -ve and neutral)
pos = 0
neg = 0
neu = 0
for text in tweets_df['text']:
    analysis = TextBlob(text)
    if analysis.sentiment[0] > 0:
        pos = pos + 1
    elif analysis.sentiment[0] < 0:
        neg = neg + 1
    else:
        neu = neu + 1
print("Total Positive = ", pos)
print("Total Negative = ", neg)
print("Total Neutral = ", neu)

print(tweets_df)

tweets_df.to_csv('testSet.csv')
