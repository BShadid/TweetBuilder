#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import random
import tweepy
import time
import re
import string
from matrixLib import *
import matrix
from getTweets import getTweets
from keys import *
import time


search = sys.stdin.read()
if search.startswith('@'):
	search = search[1:len(search)-1]

if search.endswith('.'):
	search = re.sub('["\.]', '', search)

#print(search)
master = masterM()
master.LOAD_VALUES("MARKOV")
for i in getTweets(search, 600):
	addTweet(master, i, "MARKOV")

process(master, "MARKOV")
words = master.getPV()
#print(words)
try:
	next_word = random.choice(words)[0]
except:
	next_word = search

TWEET = next_word + " "

while (len(TWEET) <= 140):

	try:
		words = getTops(master, next_word, 2, 0.0, "MARKOV")
		next_word = random.choice(words)[0]
		#print(next_word)
	except IndexError:
		break

	if len(TWEET) + len(next_word) + 1 > 140:
		break
	else:
		TWEET += next_word + " "

if (len(TWEET.split()) > 1):
	auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessSecret)
	api = tweepy.API(auth)
	api.update_status(TWEET)
	#print(TWEET)

with open("history.log", "a") as f:
	f.write(search.rstrip('\n') + ": " + TWEET + '\n')

master.DUMP_VALUES("MARKOV")
