# matrix.py/pyc
# This is the matrix object designed to handle the processing of tweets and word data.
# The methods used here are mostly used by the functions in matrixLib.py
# At some point in the future, those functions may be migrated to this class as 
# static methods rather than as its own separate file.

from operator import itemgetter # used for sorting lists of tuples

# This is a custom object for dealing with the large volumes of words we are
# working with. Every list of words is stored as a dictionary for 2 main
# purposes:
# 1. Every search and comparison is O(1) due to hash comparisons
# 2. Dictionaries are hash maps that support linear rehashing, so the time cost
# of resizing the table is distributed over its total build time.
# I failed to come up with a successful algorithm for implementing both pearson
# and Markov coefficients, so many of these methods are unused.
#
# A dictionary is the perfect data structure for this matrix because it uses
# linear rehashing of a hash map and not a threadsafe hash table. This
# asynchrounousness allows this object to process ~30,000 words in less than
# 1 second, which allows for near interactive speed in our main driver

class masterM(object):

	def __init__(self):
		self.freq = dict()		# We also use this as a master list of words
		self.primusVerbus = dict() # Dictionary of first words and their freqs
		self.corr = dict()			# Not currently being used
		self.corr_markov = dict()	# keys: two word tuples, value: No. of occurences
		self.pearsonMat = dict()	# Not currently used
		self.markovMat = dict()		# "two-dimensional" dictionary for correlation coefficients
		#self.hapaxLegomenon = dict() NOT USED
		self.pearsonized = False	# Just used as a safety check, will likely remove before final release
		self.m_pearsed = False		# Same with this one, changed to true if process() has been run.


	# Reads in one word at a time, adjusts it frequency value accordingly
	def add_freq(self, word):
		if word in self.freq:
			self.freq[word] += 1;
		else:
			self.freq.update({word: 1})

	# Return the word list (i.e. every key in the freq dict)
	def get_wl(self):
		return [ x for x in self.freq ]

	# Get frequency of a single word (O(1) time complexity)
	def get_freq(self, word):
		return self.freq[word]

	# Add first word of a tweet to first words list or update value if it
	# already exists
	def addPV(self, word):
		if word in self.primusVerbus:
			self.primusVerbus[word] += 1.0
		else:
			self.primusVerbus.update({word: 1.0})
	
	# Returns the list of first words, arranged by their frequencies in
	# descending order. O(nlog(n))
	def getPV(self):
		temp = [ (x, self.primusVerbus[x]) for x in self.primusVerbus ]	# returns with frequencies
		temp.sort(key=itemgetter(1), reverse=True) # Sorts into descending order by second item in tuple. O(nlog(n))
		return temp


	# Not currently used
	# If one word and another word exists in a tweet, their overlap increases by
	# 1. The overlap frequency is stored as a dict of two-word tuples. Think of
	# this as an overlap matrix updater.
	# For each word in the remaining tweet body, overlap between this word and
	# the other increases by 1. 
	# This is done for each word by passing a tweet into addTweet in matrixLib.
	# Time: O(n^2)
	def add_corr(self, w1, body):
		if (len(body) < 1):
			return

		for w2 in body:
			if (w1 == w2): # Overlap of same word is not dangerous, this can be removed later
				continue
			else:
				x = tuple(sorted([w1, w2])) # I did this in an effort to minimize the costly space complexity, which is O(n^2)
				if x in self.corr:
					self.corr[x] += 1.0 # We need floats for pearsonization
				else:
					self.corr.update({x:1.0})

	# Works pretty much the same way as the previous method, but only adds one
	# overlap value for the word passed in, w1, and the word that follows it,
	# w2. Again, this is managed in matrixLib
	def add_markov_corr(self, w1, w2):
		x = (w1, w2) # Here, we don't want to sort the tuple because
					 # order matters. This drives up memory requirement, but we
					 # value better time complexity over better space.
		if x in self.corr_markov:
			self.corr_markov[x] += 1.0
		else:
			self.corr_markov.update({x:1.0})
		
	# O(n)
	def pearsonize(self): # Creates the pearson correlation matrix for words as a 2D dict()
						  # RELATIVELY COSTLY COMPUTATION, should only be called once in a masterM's lifetime.
		# For each overlap pairing, coeff =
		# (intersection(word1,word2))/(freq(word1)+freq(word2)-intersection(word1,word2))
		# This is just applying basic principles of set theory
		for x in self.corr:
			self.pearsonMat.update( {x:( self.corr[x] / (self.freq[x[0]] + self.freq[x[1]] - self.corr[x]))} )
		self.pearsonized = True # masterM has been processed

	# This serves the same purpose as the pearsonize method, but for the Markov
	# correlation coefficient matrix instead of the pearson once. Again (O(n))
	def markovPearsonize(self):
		for x in self.corr_markov:
			self.markovMat.update( {x:( self.corr_markov[x] / (self.freq[x[0]] + self.freq[x[1]] - self.corr_markov[x]))})
		self.m_pearsed = True # masterM has been processed

	
	# Not used, would return the pearson correlation coefficient if possible
	def getPearson(self, w1, w2):
		if (self.pearsonized == False):
			return -1
		else:
			x = tuple(sorted([w1, w2]))
			if x in self.pearsonMat:
				return self.pearsonMat[x]
			else:
				return 0.0

	# Returns the Markov correlation coefficient between w1 and w2 if possible
	def getMark(self, w1, w2):
		if (self.m_pearsed == False): # If masterM has not been processed, this is not possible.
			return -1
		else:
			x = (w1, w2)
			if x in self.markovMat:
				return self.markovMat[x]
			else:
				return 0.0


	# Uses a priority queue to return the n most common words related to w1 with
	# a correlation coefficient above threshold. If in MARKOV mode, returns the
	# markov correlation coeffiecnt rather than the peason one. Returns the
	# sorted list of likely next words in descending order by coefficient.
	def getTopN(self, w1, n, threshold, mode = ""): 

		topN = []				# Will hold values as ((word, word), corrR)

		# Regular (pearson) mode, NOT currently used
		if (len(mode) == 0):
			for w2 in self.freq:
				if (w1 == w2):
					continue
	
				x = tuple(sorted([w1, w2]))
	
				if x not in self.corr:
					continue
	
				if (len(topN) < n):
					if (self.pearsonMat[x] > threshold):
						topN.append((x, self.pearsonMat[x]))
						if len(topN) == n:
							topN.sort(key=itemgetter(1),reverse=True)
	
				elif (self.pearsonMat[x] > topN[n-1][1]): # This is the slow part, insertion sort is O(n^2)
					topN.pop()
					topN.append((x, self.pearsonMat[x]))
					topN.sort(key=itemgetter(1))

		# MARKOV mode
		else:
			for w2 in self.freq: # Checks every word in the frequency dictionary
				
				x = (w1, w2) # We want to check for word pairs in order (w1, w2)

				if x not in self.corr_markov: # Search is O(1), so this is quick
					continue

				if (len(topN) < n): # If the length of this is under what our desired length is
					if (self.markovMat[x] > threshold): # Only append to list if the correlation is above the desired value
						topN.append((w2, self.markovMat[x]))
						if len(topN) == n: # If we've reached the desired number of next words, we need to keep the list sorted now.
							topN.sort(key=itemgetter(1),reverse=True)

				elif (self.markovMat[x] > topN[n-1][1]): # If the markov correlation coefficient is greater than that of the last element
														 # in the list, pop that last element and append the new one
					topN.pop()
					topN.append((w2, self.markovMat[x]))
					topN.sort(key=itemgetter(1),reverse=True) # It's like insertion sort but worse

		# This list has now been built, so return it
		return topN


	# This method is never called in our current version of the code. If a word needed
	# to be deleted from the matrix, it would purge all elements containing it.
	def WORD_DEL(self, w1):

		if w1 in self.primusVerbus:  # Remove from first words list
			del self.primusVerbus[w1]

		for w2 in self.freq: # For each key in the frequency dict, if it correlated with w1, remove it

			if (w1 == w2):	# This is handled separately
				continue

			x = tuple(sorted([w1, w2])) # Remove from intersection matrix

			if x not in self.corr:
				continue

			del self.corr[x]		# Remove from intersections
			del self.pearsonMat[x]	# Remove correlation coefficient too

		del self.freq[w1] # After this, any trace of that word has been erased 


	def TOP_FREQS(self): # Get the most common words in the matrix sorted in desceding order by frequency
		temp = [ x for x in self.freq ]
		temp.sort(key=itemgetter(1), reverse=True)
		return temp


	# Dump all of the intersection and frequency information to a text file that stores all of it. We need
	# large samples of data to make the markov chain algorithm more reliable, so this is a way to back it up
	def DUMP_VALUES(self, mode=""):

		with open(".freqs.txt", 'w') as f: # Write word frequencies to an intermediate text file, overwrites previous version
			for i in self.freq:
				f.write(i+"\t"+str(self.freq[i])+'\n') # Written to file as tab separated fields: word	freq

		if (mode=="MARKOV"): # Dump markov intersection values in a similar fashion
			with open(".corrM.txt", 'w') as f2:
				for i in self.corr_markov:
					f2.write(i[0]+'\t'+i[1]+'\t'+str(self.corr_markov[i])+'\n')

		else: # Dump regular intersection values if necessary, not currently used
			with open(".corr.txt", 'w') as f3:
				for i in self.corr:
					f3.write(i[0]+'\t'+i[1]+'\t'+str(self.corr[i])+'\n')

		return 0 # method ran successfully
			
	# Read in the previous frequency and intersection values from the intermediate text files if they are available
	# These are read into the masterM object before any tweets are fetched or processed.
	def LOAD_VALUES(self, mode=""):
		
		try: # Try to read in all of the indicated files. Processese lines in same format as DUMP_VALUES writes
			with open(".freqs.txt", 'r') as f:
				lines = [ line.rstrip('\n').split('\t') for line in f ]
				for x in lines:
					if not x[0].startswith('@'): # The only thing we don't want to keep so far is @USERS, words as intented
						self.freq.update({x[0]:int(x[1])})

			if (mode=="MARKOV"):
				with open(".corrM.txt", 'r') as f2:
					lines = [ line.rstrip('\n').split('\t') for line in f2 ]
					for x in lines:
						if not (x[0].startswith('@') or x[1].startswith('@')): # Same reasoning here.
							self.corr_markov.update({(x[0], x[1]):float(x[2])})

			else:
				with open(".corr.txt", 'r') as f3:
					lines = [ line.rstrip('\n').split('\t') for line in f3 ]
					for x in lines:
						self.corr.update({(x[0], x[1]):float(x[2])})

		except:
			return -1

	# This method was never used, but may be developed in the future
	def purgeHapax(self): #Remove words that only occur once, might be used if pearsonizing computation becomes too heavy
		pass

