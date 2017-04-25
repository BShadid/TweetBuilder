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

# helper functions
def generate_word_cloud(pairs):
	cloud = []
	posList = []
	collide = True
	for pair in pairs[0:(min(19,len(pairs)))]:
		font = pygame.font.Font(None,math.floor(20 + 3*pair[1]))
		text = font.render(pair[0],1,(0,0,0))
		if random.randrange(0,10) > 7:
			text = pygame.transform.rotate(text,90)
		pos = text.get_rect(center=(random.randrange(240,400),random.randrange(180,280)))
		i_pos = pos
		theta = 0
		r = 0
		while pos.collidelist(posList) >= 0:
			pos.move_ip(r*math.cos(theta),r*math.sin(theta))
			r = r+.1
			theta = theta + math.pi/4
		cloud.append((text,pos,pair[0]))
		posList.append(pos)
	return cloud

# pygame initial settings

try:
	term = sys.argv[1]
except:
	term = "data"

master = masterM();
master.LOAD_VALUES("MARKOV")
for i in getTweets(term, 1000):
	addTweet(master, i, "MARKOV")


process(master, "MARKOV")
words = master.getPV()

pygame.init()
flags = DOUBLEBUF 
win = pygame.display.set_mode((640,480), flags)
pygame.display.set_caption("TwitterRNN")
win.set_alpha(None)
clock = pygame.time.Clock()

TWEET = ""

#words = [('Samuel',65),('Jacob',54),('Benjamin',37),('Twitter',35),('project',32),('pal',21),('buddy',13)]
cloud = generate_word_cloud(words)

bg = pygame.Surface(win.get_size())
bg = bg.convert()


def pushtweet(tweet):
	try:
		auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
		auth.set_access_token(accessKey, accessSecret)
		api = tweepy.API(auth)
		api.update_status(tweet)
	except TweepError:
		print("TweepError: coud not tweet at this time")

	master.DUMP_VALUES("MARKOV")
	exit()

# main interaction loop :: updates screen and checks for events
while(1):
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pushtweet(TWEET)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			for word in cloud:
				if word[1].collidepoint(pygame.mouse.get_pos()):
					if len(TWEET) + len(word[2] + " ") > 140:
						pushtweet(TWEET)
					TWEET += word[2] + " "
					print(word[2])
					cloud = generate_word_cloud(getTops(master, word[2], 5, 0.0, "MARKOV"))
	 
	bg.fill((255,255,255))	  
	for word in cloud:
		bg.blit(word[0],word[1])	

	win.blit(bg,(0,0))
	pygame.display.flip()
