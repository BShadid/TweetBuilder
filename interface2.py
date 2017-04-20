#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import random
import tweepy
import time
from matrixLib import *
import matrix
from getTweets import getTweets
from keys import *
import time


master = masterM()
master.LOAD_VALUES("MARKOV")
for i in getTweets('test', 1000):
	addTweet(master, i, "MARKOV")

process(master, "MARKOV")
words = master.getPV()
try:
	next_search = words[random.randrange(len(words)-1)][0]
except:
	next_search = "the"

TWEET = next_search + " "


next_word = words[0][0]

while (len(TWEET) <= 140):

	try:
		words = getTops(master, next_word, 5, 0.05, "MARKOV")
		next_word = words[random.randrange(len(words)-1)][0]
	except IndexError:
		break
	except ValueError:
		break

	if len(TWEET) + len(next_word) + 1 > 140:
		break
	else:
		TWEET += next_word + " "

if (len(TWEET.split()) > 2):
	auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessSecret)
	api = tweepy.API(auth)
	api.update_status(TWEET)

master.DUMP_VALUES("MARKOV")
