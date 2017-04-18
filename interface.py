#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3

# interface.py :: interface for twitterRNN
#	       :: main driver for project, integrates graphics

import os, sys
import math, random
import pygame

# helper functions
def generate_word_cloud(pairs):
  cloud = []
  posList = []
  collide = True
  for pair in pairs[0:19]:
    font = pygame.font.Font(None,math.floor(12 + pair[1]));
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
pygame.init()
win = pygame.display.set_mode((640,480))
pygame.display.set_caption("TwitterRNN")
clock = pygame.time.Clock()

words = [('Samuel',65),('Jacob',54),('Benjamin',37),('Twitter',35),('project',32),('pal',21),('buddy',13)]
cloud = generate_word_cloud(words)

bg = pygame.Surface(win.get_size())
bg = bg.convert()

# main interaction loop :: updates screen and checks for events
while(1):
  clock.tick(60)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      for word in cloud:
        if word[1].collidepoint(pygame.mouse.get_pos()):
          print(word[2])
  
  bg.fill((255,255,255))	  
  for word in cloud:
    bg.blit(word[0],word[1])

  win.blit(bg,(0,0))
  pygame.display.flip()
