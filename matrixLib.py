#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# This is the main library for interacting with the masterM class,
# which holds correlation and frequency information for words in tweets

from matrix import masterM # This is the object for handling all the pertinent information

# ---------- TWEET PROCESSING FUNCTIONS ------------ #

# Passing in a tweet, this function will filter out words from a commons list
# This function is not yet used.
def filterCommons(tweet, commons=[]):
	return [ word for word in tweet if set(word) & set(commons) ] # Set comparisons are O(1) time

# Takes in a list of words from a tweet, adds them to the masterM object
def addTweet(M, tweet, mode = ""): #take in masterM, list, mode as arguments
	
	# Run in regular mode
	if (len(mode) == 0):
		if (len(tweet) > 0):
			M.addPV(tweet[0]) # Add first word to M's first word list
	
			while (len(tweet) > 0): # Keep popping words until the tweet has been processed.
				current = tweet.pop(0) 
				M.add_freq(current)			# Update word's value in M's frequency list
				M.add_corr(current, tweet)	# Update intersection values in M
	
	elif (mode == "MARKOV"):
		if (len(tweet) > 0):
			M.addPV(tweet[0]) # Add first word to M's list of first words
			
			while (len(tweet) > 0): # Keep processing pairs of adjacent words until tweet has been processed.
				current = tweet.pop(0)
				M.add_freq(current)

				try:
					M.add_markov_corr(current, tweet[0])
				except IndexError:
					break # Breaks while loop if last pairing does not exist



# -------------- MATRIX-RELATED FUNCTIONS ----------- #

# Get the first words and their frequencies for word-cloud generation
# In our current implementation, this function is bypassed entirely by the top-level driver
def getFirsts(M, commons=[]):
	return [ x for x in M.getPV() if x[0] not in set(commons) ]

# Remove words from matrix whose frequencies are below a specific threshold
def purgeTable(M, minimum): # This will be costly
	toBeCleansed = [ word  for word in M.get_wl() if M.get_freq(word) < mininum ]
	for word in toBeCleansed:
		M.WORD_DEL(word)

# Remove one word only from the Matrix
def removeSingle(M, w1):
	M.WORD_DEL(w1)

# Pearsonize the matrix after everything is set in place, everything is handled internally
def process(M, mode = ""):
	if (mode == "MARKOV"):
		if (M.getMark(" ", " ") == -1):
			M.markovPearsonize()
	else:
		if (M.getPearson(" ", " ") == -1):		
			M.pearsonize()

# Return a list of top-correlated words for a given word in the matrix, everything handled internally
def getTops(M, word, N_ITEMS=5, threshold = 0.01, mode = ""):
	if (mode == "MARKOV"):
		return M.getTopN(word, N_ITEMS, threshold, "MARKOV")
	else:
		return M.getTopN(word, N_ITEMS, threshold)

# Return a list of the most common words in the matrix, may not be used in final release
def getMostCommon(M):
	return M.TOP_FREQS()
