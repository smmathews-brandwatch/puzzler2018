import sys, pygame, simulator, requests, simulator, time
from flask import json
pygame.init()

# Define some colors
BACKGROUND_COLOR = (0, 0, 0)
EMPTY_COLOR = (255, 255, 255)
ENEMIES = [pygame.image.load("assets/cartoonHexy.png"),pygame.image.load("assets/humanHexy.png")]
COLLECTIBLES = [pygame.image.load("assets/brandWatch.png")]
PLAYER_COLOR = (128, 128, 128)
HOME_BASE_COLOR = (0, 255, 0)
ENEMY_BASE_COLOR = (128, 128, 0)
RED = (255, 0, 0)
MARGIN = 1

size = width, height = 700, 500

pygame.display.set_caption("PUZZLER 2018")

screen = pygame.display.set_mode(size)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

neverDrawn = True
sim = None

def getNewSim():
    url = 'http://127.0.0.1:5000/simulator/state'
    reason = 'unknown'
    try:
        r = requests.get(url)
        if(r.status_code==200):
            sim = simulator.Simulator(fromDict=r.json())
            return sim
    except:
        pass
    return None

def processInput(events): 
   for event in events: 
      if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  or (event.type == pygame.QUIT): 
         sys.exit(0)

entityToImage = dict({
    simulator.BoardPiece.Enemy:ENEMIES,
    simulator.BoardPiece.Diamond:COLLECTIBLES,
})
entityToColor = dict({
    simulator.BoardPiece.Bot:PLAYER_COLOR,
    simulator.BoardPiece.HomeBase:HOME_BASE_COLOR,
    simulator.BoardPiece.EnemyBase:ENEMY_BASE_COLOR
})

def draw(sim):
    global neverDrawn
    neverDrawn = False
    screen.fill(BACKGROUND_COLOR)
    if sim == None:
        textsurface = myfont.render('connecting...', True, RED)
        screen.blit(textsurface,(0,0))
    else:
        pieceWidth = width/sim.board.width - 2*MARGIN
        pieceHeight = height/sim.board.height - 2*MARGIN
        for x in range(sim.board.width):
            for y in range(sim.board.height):
                pygame.draw.rect(screen,
                                EMPTY_COLOR,
                                [(pieceWidth + 2*MARGIN) * x + MARGIN,
                                (pieceHeight + 2*MARGIN) * y + MARGIN,
                                pieceWidth,
                                pieceHeight])
        for entity in sim.board.entities:
            if(entity.boardPiece in entityToColor):
                pygame.draw.rect(screen,
                    entityToColor[entity.boardPiece],
                    [(pieceWidth + 2*MARGIN) * entity.position.x + MARGIN,
                    (pieceHeight + 2*MARGIN) * entity.position.y + MARGIN,
                    pieceWidth,
                    pieceHeight])
            else:
                images = entityToImage[entity.boardPiece]
                image = images[entity.id % len(images)]
                image = pygame.transform.scale(image, (int(pieceWidth),int(pieceHeight)))
                rect = pygame.Rect((pieceWidth + 2*MARGIN) * entity.position.x + MARGIN,
                    (pieceHeight + 2*MARGIN) * entity.position.y + MARGIN,
                    pieceWidth,
                    pieceHeight)
                print(entity.position.x)
                print(entity.position.y)
                screen.blit(image, rect)
    pygame.display.flip()

FPS = 60
clock = pygame.time.Clock() # Create a clock object

while 1:
    processInput(pygame.event.get())
    newSim = getNewSim()
    simChanged = False
    if((newSim is None) != (sim is None)):
        simChanged = True
    elif((newSim is not None) and (sim is not None)):
        simChanged = newSim.frame != sim.frame or newSim.simRound != sim.simRound
    sim = newSim
    if(simChanged or neverDrawn):
        draw(sim)
    clock.tick(FPS)