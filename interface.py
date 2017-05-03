#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import math, random
import tweepy
import pygame
from pygame.locals import *
from matrixLib import *
import matrix
from getTweets import getTweets
from keys import *

###### helper functions

### graphics

def generate_word_cloud(pairs):
	# two separate lists, one for tracking the source, destination, and text of a word
	# generated for graphics reasons
	cloud = []
	# the other is for collision tracking purposes, and only contains the destination
	# position of each word
	posList = []
	
	# handles up to 20 words
	for pair in pairs[0:(min(19,len(pairs)))]:
		# initialize the font. font size is dependent on the frequency
		font = pygame.font.Font(None,math.floor(20 + 3*pair[1]))
		# render the word
		text = font.render(pair[0],1,(0,0,0))
	
		### find a place for the word using wordle algorithm
		# place in random location
		if random.randrange(0,10) > 7:
			text = pygame.transform.rotate(text,90)
		pos = text.get_rect(center=(random.randrange(240,400),random.randrange(180,280)))

		# move along a spiral until we find an empty place
		i_pos = pos
		theta = 0
		r = 0
		while pos.collidelist(posList) >= 0:
			pos.move_ip(r*math.cos(theta),r*math.sin(theta))
			r = r+.1
			theta = theta + math.pi/4

		# add source, destination, and text to the cloud list
		cloud.append((text,pos,pair[0]))
		posList.append(pos)
	return cloud

# print the tweet in progress at the bottom of the graphics display
def tweet_to_text_object(tweet):
	# up to two separate text objects required, one for each line
	text_objs = []

	# initialize font
	font = pygame.font.Font(None,20)

	# the general rule is if the tweet is less than 90 characters it only needs 1 line
	if len(tweet) < 90:
		text = font.render(tweet,1,(0,0,0))
		pos = text.get_rect(x=4,y=440)
		text_objs.append((text,pos))
	else:
		# otherwise we make two text objects
		i = 89
		while tweet[i] != " ":
			i = i-1
		text = font.render(tweet[:i],1,(0,0,0))
		pos = text.get_rect(x=4,y=440)
		text_objs.append((text,pos))
		text = font.render(tweet[i+1:],1,(0,0,0))
		pos = text.get_rect(x=4,y=460)
		text_objs.append((text,pos))
	return text_objs 

### tweepy interactions

# sends a tweet with the given message and exits the program
def pushtweet(tweet):
	try:
		# authorization
		auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
		auth.set_access_token(accessKey, accessSecret)
		api = tweepy.API(auth)
		# tweet our tweet
		api.update_status(tweet)
	except TweepError:
		print("TweepError: coud not tweet at this time")

	# add data to the files and exit
	master.DUMP_VALUES("MARKOV")
	exit()

###### initial settings

### interacting with tweepy and the matrix library

# command line argument handling
try:
	term = sys.argv[1]
except:
	term = "data"

# loads the correlation matrix and adds info from the new tweets
master = masterM();
master.LOAD_VALUES("MARKOV")
for i in getTweets(term, 1000):
	addTweet(master, i, "MARKOV")

process(master, "MARKOV")
words = master.getPV()

### pygame setup

pygame.init()
flags = DOUBLEBUF 

# 640x480 display
win = pygame.display.set_mode((640,480), flags)
pygame.display.set_caption("TweetBuilder")
win.set_alpha(None)
# clock to regulate interactions and animations
clock = pygame.time.Clock()

# font for tweet button
font = pygame.font.Font(None,20)
button_src = font.render("Tweet",1,(255,255,255))
button_dst = button_src.get_rect(x = 585,y = 450)

# tweet string
TWEET = ""

# make tweet for bottom of screen
tweet_objs = tweet_to_text_object(TWEET)

# make word cloud
cloud = generate_word_cloud(words)

# create the display's surface
bg = pygame.Surface(win.get_size())
bg = bg.convert()

###### main interaction loop :: updates screen and checks for events
while(1):
	# 60 fps
	clock.tick(60)

	# event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			for word in cloud:
				# if you click on a word in the cloud
				if word[1].collidepoint(pygame.mouse.get_pos()):
					# check to make sure the tweet isn't too long
					if len(TWEET) + len(word[2] + " ") > 140:
						print("exceeded character limit")
					else:
						# add word to tweet
						TWEET += word[2] + " "
						# create new word cloud with top correlated words
						cloud = generate_word_cloud(getTops(master, word[2], 5, 0.0, "MARKOV"))
						# update tweet at bottom of screen
						tweet_objs = tweet_to_text_object(TWEET)
			# if you click on the tweet button
			if len(TWEET) > 0 and tweet_button.collidepoint(pygame.mouse.get_pos()):
				# tweet our tweet
				pushtweet(TWEET)
	 
	# update graphics
	bg.fill((255,255,255))	  

	# word cloud
	for word in cloud:
		bg.blit(word[0],word[1])	

	# tweet
	for tweet_obj in tweet_objs:
		bg.blit(tweet_obj[0],tweet_obj[1])
	
	# tweet button
	tweet_button = pygame.draw.rect(bg,(29,161,242),(565,440,70,35))
	bg.blit(button_src,button_dst)

	# blit surface to window
	win.blit(bg,(0,0))

	# show updates to user
	pygame.display.flip()

# vim: set sts=8 sw=8 ts=8 noexpandtab:
