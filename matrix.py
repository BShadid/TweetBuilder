#import string
#import numpy
from operator import itemgetter

class masterM(object):

	def __init__(self):
		self.freq = dict()		# We also use this as a master list of words
		self.primusVerbus = dict()
		self.corr = dict()
		self.corr_markov = dict()
		self.pearsonMat = dict()
		self.markovMat = dict()
		#self.hapaxLegomenon = dict()
		self.pearsonized = False	#Just used as a safety check, will remove before final release
		self.m_pearsed = False


	def add_freq(self, word):
		if word in self.freq:
			self.freq[word] += 1;
		else:
			self.freq.update({word: 1})


	def get_wl(self):
		return [ x for x in self.freq ]


	def get_freq(self, word):
		return self.freq[word]


	def addPV(self, word):
		if word in self.primusVerbus:
			self.primusVerbus[word] += 1.0
		else:
			self.primusVerbus.update({word: 1.0})
	

	def getPV(self):
		temp = [ (x, self.primusVerbus[x]) for x in self.primusVerbus ]	# returns with frequencies
		temp.sort(key=itemgetter(1), reverse=True)
		return temp


	def add_corr(self, w1, body):
		if (len(body) < 1):
			return

		for w2 in body:
			if (w1 == w2):
				continue
			else:
				x = tuple(sorted([w1, w2]))
				#x = (y[0], y[1])
				if x in self.corr:
					self.corr[x] += 1.0 # We need floats for pearsonization
				else:
					self.corr.update({x:1.0})

	
	def add_markov_corr(self, w1, w2):
		x = tuple([w1, w2])

		if x in self.corr_markov:
			self.corr_markov[x] += 1.0
		else:
			self.corr_markov.update({x:1.0})
		

	def pearsonize(self): # Creates the pearson correlation matrix for words as a virtual 2D dict()
						  # VERY HEAVY COMPUTATION, should only be called once in a masterM's lifetime.
		#self.purgeHapax()
		for x in self.corr:
			self.pearsonMat.update( {x:( self.corr[x] / (self.freq[x[0]] + self.freq[x[1]] - self.corr[x]))} )
		self.pearsonized = True

	
	def markovPearsonize(self):
		for x in self.corr_markov:
			self.markovMat.update( {x:( self.corr_markov[x] / (self.freq[x[0]] + self.freq[x[1]] - self.corr_markov[x]))})
		self.m_pearsed = True


	def getPearson(self, w1, w2):
		if (self.pearsonized == False):
			return -1
		else:
			y = sorted(w1, w2)
			x = (y[0], y[1])
			if x in self.pearsonMat:
				return self.pearsonMat[x]
			else:
				return 0.0


	def getMark(self, w1, w2):
		if (self.m_pearsed == False):
			return -1
		else:
			y = sorted(w1, w2)
			x = (y[0], y[1])
			if x in self.markovMat:
				return self.markovMat[x]
			else:
				return 0.0


	def getTopN(self, w1, n, threshold, mode = ""): #VERY COSTLY COMPUTATION

		topN = []				# Will hold values as ((word, word), corrR)

		if (len(mode) == 0):
			for w2 in self.freq:
				if (w1 == w2):
					continue
	
				x = tuple(sorted([w1, w2]))
	
				if x not in self.corr:
					continue
	
				if (len(topN) < n):
					if (self.pearsonMat[x] >= threshold):
						topN.append((x, self.pearsonMat[x]))
	
				elif (self.pearsonMat[x] > topN[n-1][1]): # This is the slow part, insertion sort is O(n^2)
					topN.pop()
					topN.append((x, self.pearsonMat[x]))
					topN.sort(key=itemgetter(1))
		else:
			for w2 in self.freq:
				
				x = tuple([w1, w2])

				if x not in self.corr_markov:
					continue

				if (len(topN) < n):
					if (self.markovMat[x] >= threshold):
						topN.append((w2, self.markovMat[x]))

				elif (self.markovMat[x] > topN[n-1][1]):
					topN.pop()
					topN.append((w2, self.markovMat[x]))
					topN.sort(key=itemgetter(1),reverse=True)
		return topN


	def WORD_DEL(self, w1):

		if w1 in self.primusVerbus:
			del self.primusVerbus[w1]

		for w2 in self.freq:

			if (w1 == w2):
				continue

			x = tuple(sorted([w1, w2]))

			if x not in self.corr:
				continue

			del self.corr[x]
			del self.pearsonMat[x]

		del self.freq[w1]


	def TOP_FREQS(self):
		temp = [ x for x in self.freq ]
		temp.sort(key=itemgetter(1), reverse=True)
		return temp


	# Since the student machine's OOM killer hates us, we'll have to back up our progress
	def DUMP_VALUES(self, mode=""):

		if not (self.pearsonized or self.m_pearsed):
			return -1

		with open(".m_freqs.txt", 'w') as f:
			for i in self.freq:
				f.write(i+","+str(self.freq[i])+'\n')

		if (mode=="MARKOV"):
			with open(".m_corrM.txt", 'w') as f2:
				for i in self.corr_markov:
					f2.write(i[0]+','+i[1]+','+str(self.corr_markov[i])+'\n')

		else:
			with open(".m_corr.txt", 'w') as f3:
				for i in self.corr:
					f3.write(i[0]+','+i[1]+','+str(self.corr[i])+'\n')

		return 0
			
	# This should be called at the start of the program for starter data
	def LOAD_VALUES(self, mode=""):
		
		try:
			with open(".m_freqs.txt", 'r') as f:
				lines = [ line.rstrip('\n').split(',') for line in f ]
				for x in lines:
					self.freq.update({x[0]:int(x[1])})

			if (mode=="MARKOV"):
				with open(".m_corrM.txt", 'r') as f2:
					lines = [ line.rstrip('\n').split(',') for line in f2 ]
					for x in lines:
						self.corr_markov.update({(x[0], x[1]):float(x[2])})

			else:
				with open(".m_corr.txt", 'r') as f3:
					lines = [ line.rstrip('\n').split(',') for line in f3 ]
					for x in lines:
						self.corr.update({(x[0], x[1]):float(x[2])})

		except:
			return -1

	def purgeHapax(self): #Remove words that only occur once, might be used if pearsonizing computation becomes too heavy
		pass

