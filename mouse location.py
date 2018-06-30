#!/usr/bin/python
import pygame
from pygame.locals import *

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def main():
   pygame.init()
   screen = pygame.display.set_mode((800,600))
   screen.fill(WHITE)
   pygame.display.set_caption('Testing')
   running = True
   while running:
      for event in pygame.event.get():
         if event.type == QUIT:
            running = False
         if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
         if event.type == MOUSEBUTTONDOWN:
            print (event.button)
            print (pygame.mouse.get_pos())
            pygame.draw.circle(screen, BLUE, list(pygame.mouse.get_pos()), 10)
         pygame.display.flip()
   pygame.display.quit()

if __name__ == '__main__':
   main()
