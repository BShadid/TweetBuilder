#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import pygame

# pygame initial settings
pygame.init()
win = pygame.display.set_mode((640,480))
pygame.display.set_caption("TwitterRNN")
clock = pygame.time.Clock()

# main interaction loop :: updates screen and checks for events
while(1):
  clock.tick(60)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      exit()
