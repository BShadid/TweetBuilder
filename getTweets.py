#!/usr/bin/env python2

import tweepy
import re

from keys import consumerKey, consumerSecret, accessKey, accessSecret

# get and print the specified amount(default 20) of most recent English tweets containing specified word
def getTweets(word,numTweets=20):
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    tweets = api.search(word,'en',count=numTweets)
    for tweet in tweets:
	tw = ''.join([char for char in tweet.text if ord(char) < 128])
	tw = re.sub('https://[^\s]*', '', tw)
	tw = re.sub('RT @[^\s]*', '', tw)
	tw = re.sub('@[^\s]*', '', tw)
	tw = re.sub('[^a-zA-Z0-9\s]', '', tw)
	tw = re.sub('\s+', ' ', tw).strip().lower()
	yield tw.split(' ')
