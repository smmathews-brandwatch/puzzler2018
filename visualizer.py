import sys, pygame, simulator, requests, simulator, time
from flask import json
pygame.init()

# Define some colors
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = width, height = 700, 500
speed = [2, 2]

pygame.display.set_caption("PUZZLER 2018")

screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets/badHexy.png")
ballrect = ball.get_rect()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

sim = None

def updateSim():
    global sim
    url = 'http://127.0.0.1:5000/simulator/state'
    reason = 'unknown'
    try:
        r = requests.get(url)
        if(r.status_code==200):
            sim = simulator.Simulator(fromDict=r.json())
        else:
            reason = 'status code: ' + str(r.status_code)
    except:
        reason = 'can not connect'
    if sim == None:
        textsurface = myfont.render('connecting to ' + url + ' ...', False, RED)
        screen.blit(textsurface,(0,0))
    else:
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        screen.blit(ball, ballrect)

def processInput(events): 
   for event in events: 
      if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  or (event.type == pygame.QUIT): 
         sys.exit(0) 
      else: 
         print(event)

while 1:
    screen.fill(BACKGROUND_COLOR)

    processInput(pygame.event.get())
    updateSim()
    pygame.display.flip()