#!/usr/bin/env python2.7

# This is the main library for interacting with the masterM class,
# which holds correlation and frequency information

from matrix import masterM
from autocorrect import spell

# ---------- TWEET PROCESSING FUNCTIONS ------------ #

# Passing in a tweet, this function will filter out words from a commons list
def filterCommons(tweet, commons):
	return [ word for word in tweet if set(word) & set(commons) ]

# Uses spellcheck to replace words, VERY costly build time of Matrix using this function
def wordCheck(tweet):
	return list(map(spell, word for word in tweet))

# Takes in a list of words from a tweet, adds them to the 
def addTweet(M, tweet): #take in mastermatrix, list as arguments
	if (len(tweet) > 0):
		M.addPV(tweet[0])

		while (len(tweet) > 0):
			current = tweet.pop(0)
			M.add_freq(current)
			M.add_corr(current, tweet)


# -------------- MATRIX-RELATED FUNCTIONS ----------- #

# Get the first words and their frequencies for word-cloud generation
def getFirsts(M, commons):
	return [ x for x in M.getPV() if x[0] not in set(commons) ]

# Remove words from matrix whose frequencies are below a specific threshold
def purgeTable(M, minimum): # This will be costly
	toBeCleansed = [ word  for word in M.get_wl() if M.get_freq(word) < mininum ]
	for word in toBeCleansed:
		M.WORD_DEL(word)

# Remove one word only from the Matrix
def removeSingle(M, w1):
	M.WORD_DEL(w1)
