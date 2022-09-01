import tweepy
import logging
from tweepy import parsers
import numpy as np
import pandas as pd
import re
from textblob import TextBlob

logging.basicConfig(level=logging.DEBUG)

# access token 835499518225444864-QQZBLOfwSzkC85NEWEbFNAj4vywjlQe
# access token secret 3eRJZj9cHfHiz0rIhZsvLdC7hU9GCJcSoHwgPaUR2Hcuq

# consumer key 5ILWz2QmpSPppTSOwdMvj2q5a
# consumer secret: rKjQ8KB5QYdkq6a3Ab29n6ydc9N6YjezpdDzcALTOXaxPV1nDN

access_token = "835499518225444864-QQZBLOfwSzkC85NEWEbFNAj4vywjlQe"
access_token_secret = "3eRJZj9cHfHiz0rIhZsvLdC7hU9GCJcSoHwgPaUR2Hcuq"
consumer_key = "5ILWz2QmpSPppTSOwdMvj2q5a"
consumer_secret = "rKjQ8KB5QYdkq6a3Ab29n6ydc9N6YjezpdDzcALTOXaxPV1nDN"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Generating list of all public tweets from timeline
public_tweets = api.home_timeline()

# creating a tweet dictionary
# tweet = public_tweets[0]
# picking text from the tweet dictonary
# print (tweet['text'])

# tweets['text'] = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweets['text']).split()

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

#def sentiment_analyser():
#    analysis = TextBlob('.join(temp_df[].values.tolist())')

    # for tweets in public_tweets:
    #    analysis = TextBlob(-----)

#    if analysis.sentiment.polarity > 0:
#        return 'positive'

#    elif analysis.sentiment.polarity == 0:
#        return 'neutral'

#    else:
#        return 'negative'




# picking positive tweets from tweets
#    ptweets = []
#    for tweet in tweets:
#        if tweet["sentiment"] == "positive":
#            ptweets.append(tweet)
#    # percentage of positive tweets
#    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
#    # picking negative tweets from tweets
#    ntweets = []
#    for tweet in tweets:
#       if tweet["sentiment"] == "negative":
#            ntweets.append(tweet)
#    # percentage of negative tweets
#    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
#    # percentage of neutral tweets
#    print("Neutral tweets percentage: {} % \
#        ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

# printing first 5 positive tweets
#    print("\n\nPositive tweets:")
#    for tweet in ptweets[:10]:
#        print(Temp_text)

# printing first 5 negative tweets
#    print("\n\nNegative tweets:")
#    for tweet in ntweets[:10]:
#        print(Temp_text)

print(tweets_df)

tweets_df.to_csv('testSet.csv')
