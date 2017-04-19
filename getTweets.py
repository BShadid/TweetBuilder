import tweepy
import re
import matrix
from matrixLib import *
from keys import consumerKey, consumerSecret, accessKey, accessSecret

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessKey, accessSecret)
api = tweepy.API(auth)

# get and print the specified amount(default 20) of most recent English tweets containing specified word
def getTweets(word,numTweets=20):
	tweets = api.search(word,'en',count=numTweets)
	for tweet in tweets:
		tw = str(''.join([char for char in tweet.text if ord(char) < 128]))
		tw = re.sub('https://[^\s]*', '', tw)
		tw = re.sub('RT @[^\s]*', '', tw)
		tw = re.sub('@[^\s]*', '', tw)
		tw = re.sub('[^a-zA-Z0-9\s]', '', tw)
		tw = re.sub('\s+', ' ', tw).strip().lower()
		yield tw.split(' ')

'''
master = masterM();

for i in getTweets("test", 1000):
	addTweet(master, i, "MARKOV")

process(master)
'''
