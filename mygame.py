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
g = 0.5

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Testing')
clock = pygame.time.Clock()

class Circle:
    def __init__(self):
        self.pos = np.array([200,200])
        self.velocity = np.array([3,-2])
    def updade(self,mouse):
        s = 0
        prev_condition = False
        condition = ((radius + mRadius)**2 >= ((self.pos[0] - mouse[0])**2 +(self.pos[1] - mouse[1])**2))
        self.pos = np.add(self.velocity,self.pos)
        if ((self.pos[0] > width - radius - 1) or (self.pos[0] < 0 + radius)):
            self.velocity[0] *= -1
        if self.pos[1] > height - radius - base - 1:
            self.pos[1] = height - radius - base - 1
            self.velocity[1] *= -1
            s = 2
        elif ((radius + mRadius)**2 >= ((self.pos[0] - mouse[0])**2 +(self.pos[1] - mouse[1])**2)):
            p_ = (np.add(mRadius*self.pos,radius*mouse))/(mRadius+radius)
            p = np.subtract(self.pos,p_)
            p_mag = np.linalg.norm(p)
            mag = (radius - p_mag)*((mRadius+radius)/radius)
            q = (mag/p_mag)*p
            self.pos = np.add(self.pos,q)
            [lx,ly] = list(np.subtract(self.pos,mouse))
            A = (lx**2 - ly**2)/(lx**2 + ly**2)
            B = 2*lx*ly/(lx**2 + ly**2)
            M = np.array([[A,B],[B,(-1)*A]])
            self.velocity = list((-1)*M.dot(self.velocity))
            s = 1
            #print(str(self.pos)+"\t"+str(self.velocity)+"\t"+str(mouse))
        else:
            self.velocity = np.add(self.velocity,[0,g])
        prev_condition = condition
        pygame.draw.circle(screen, GREEN, [int(self.pos[0]),int(self.pos[1])], radius)
        return s

def score_update(score):
    font = pygame.font.SysFont(None,25)
    text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(text,(20,20))
    
def gameloop():
    Quit = False
    mouse = np.array([400,700])
    score = 0
    running = True
    ball = Circle()
    while running:
        mouse = np.array(pygame.mouse.get_pos())
        screen.fill(WHITE)
        pygame.draw.circle(screen, BLUE, list(mouse), mRadius)
        update_score = ball.updade(mouse)
        if(update_score == 1):
            score += 1
        score_update(score)
        if(update_score == 2):
            running = False
        pygame.draw.rect(screen,RED,(0,height-base,width,base))
        pygame.display.update()
        clock.tick(70)
        for event in pygame.event.get():
            if event.type == QUIT:
                Quit = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
    return (score,Quit)


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return (textSurface, textSurface.get_rect())


def message(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    (TextSurf, TextRect) = text_objects(text, largeText)
    TextRect.center = (width/2,height/2)
    screen.blit(TextSurf,TextRect)
    pygame.display.update()
    pygame.time.wait(2000)

 

if __name__ == '__main__':
    Quit = False
    while (not Quit):
        (score,Quit) = gameloop()
        if(not Quit):
            message("Your score: "+str(score))

    pygame.display.quit()







