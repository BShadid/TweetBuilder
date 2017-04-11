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
def addTweet(M, tweet, mode = ""): #take in mastermatrix, list as arguments
	if (len(mode) == 0):
		if (len(tweet) > 0):
			M.addPV(tweet[0])
	
			while (len(tweet) > 0):
				current = tweet.pop(0)
				M.add_freq(current)
				M.add_corr(current, tweet)
	
	elif (mode == "MARKOV"):
		if len(tweet) > 0):
			M.addPV(tweet[0])
			
			while (len(tweet) > 0):
				current = tweet.pop(0)
				M.add_freq(current)

				try:
					M.add_markov_corr(current, tweet[0])
				except IndexError:
					break



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

# Pearsonize the matrix after everything is set in place
def process(M, mode = ""):
	if (mode == "MARKOV"):
		if (M.getMark(" ", " ") == -1):
			M.markovPearsonize()
			return 0
	else:
		if (M.getParson(" ", " ") == -1):		
			M.pearsonize()
			return 0

	return 1

# Return a list of top-correlated words for a given word in the matrix
def getTops(M, word, N_ITEMS, threshold = 0.01, mode = ""):
	if (mode == "MARKOV"):
		return M.getTopN(word, N_ITEMS, threshold, "MARKOV")
	else:
		return M.getTopN(word, N_ITEMS, threshold)
