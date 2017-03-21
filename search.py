#!/usr/bin/env python2

import tweepy
import sys

# Each of these will need to be replaced with the corresponding key (see
# 2NipBot.txt in Google Drive)
consumerKey = <key>
consumerSecret = <key>
accessKey = <key>
accessSecret = <key>

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)

word = 'word'
if len(sys.argv) > 1:
    word = sys.argv[1]

# get and print the 20 most recent tweets in English containing specified word
tweets = api.search(word,'en')
for tweet in tweets:
    print '> ' + ''.join([char for char in tweet.text if ord(char) < 128])
