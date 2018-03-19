import pygame
from pygame.locals import *
import numpy as np

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

width = 800
height = 600
radius = 40
mRadius = 60
base  = 20
g = 0.2

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Testing')
clock = pygame.time.Clock()

class Circle:
    def __init__(self):
        self.pos = np.array([100,100])
        self.velocity = np.array([2,0])
    def upgrade(self,mouse):
        self.pos = np.add(self.velocity,self.pos)
        if ((self.pos[0] > width - radius - 1) or (self.pos[0] < 0 + radius)):
            self.velocity[0] *= -1
        if self.pos[1] > height - radius - base - 1:
            self.velocity[1] *= -1
            #print(str(self.velocity[1])+"\t"+str(self.pos[1]))
        else:
            self.velocity = np.add(self.velocity,[0,g])
        if ((radius + mRadius)**2 >= ((self.pos[0] - mouse[0])**2 +(self.pos[1] - mouse[1])**2)):
            self.pos = np.subtract(self.pos,self.velocity)
            lx = self.pos[0] - mouse[0]
            ly = self.pos[1] - mouse[1]
            A = (lx**2 - ly**2)/(lx**2 + ly**2)
            B = 2*lx*ly/(lx**2 + ly**2)
            M = np.array([[A,B],[B,(-1)*A]])
            self.velocity = list((-1)*M.dot(self.velocity))
            print(str(lx)+"\t"+str(ly)+"\t"+str(mouse))
            
            
        pygame.draw.circle(screen, GREEN, [int(self.pos[0]),int(self.pos[1])], radius)
        return True
def main():
    mouse = [100,100]
    running = True
    ball = Circle()
    while running:
        (mouse[0],mouse[1]) = pygame.mouse.get_pos()
        screen.fill(WHITE)
        pygame.draw.circle(screen, BLUE, mouse, mRadius)
        running = ball.upgrade(mouse)
        pygame.draw.rect(screen,RED,(0,height-base,width,base))
        pygame.display.update()
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False


    pygame.display.quit()

if __name__ == '__main__':
   main()
