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
api.update_status(sys.argv[1])
