import sys, pygame, simulator, requests, simulator, time, json, botActions
pygame.init()

# Define some colors
BACKGROUND_COLOR = (0, 0, 0)
EMPTY_COLOR = (255, 255, 255)
RED = (255, 0, 0)
MARGIN = 1

entityToImage = dict({
    simulator.BoardPiece.Bot:pygame.image.load("assets/cartoonHexy.png"),
    simulator.BoardPiece.Enemy:pygame.image.load("assets/cyborg-face.png"),
    simulator.BoardPiece.Collectible:pygame.image.load("assets/brandWatch.png"),
    simulator.BoardPiece.BotBase:pygame.image.load("assets/annexation.png"),
    simulator.BoardPiece.EnemyBase:pygame.image.load("assets/cryo-chamber.png"),
})

size = width, height = 700, 500

pygame.display.set_caption("PUZZLER 2018")

screen = pygame.display.set_mode(size)

pygame.font.init()
fontSize = 30
myfont = pygame.font.SysFont('Comic Sans MS', fontSize)

neverDrawn = True
sim = None
interactiveMode = False

networkBot = botActions.NetworkBot()

def getNewSim():
    return networkBot.getSim()

def processInput(events): 
   for event in events: 
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  or (event.type == pygame.QUIT): 
            sys.exit(0)
        elif(event.type == pygame.KEYDOWN and event.key == pygame.K_i):
            global interactiveMode
            interactiveMode = not interactiveMode
            print("interactive mode is: " + ("ON"  if interactiveMode else "OFF"))
            draw(sim)
        if(interactiveMode and event.type == pygame.KEYDOWN and sim is not None):
            if(event.key == pygame.K_DOWN):
                networkBot.sendMoveDown()
            if(event.key == pygame.K_UP):
                networkBot.sendMoveUp()
            if(event.key == pygame.K_LEFT):
                networkBot.sendMoveLeft()
            if(event.key == pygame.K_RIGHT):
                networkBot.sendMoveRight()
            if(event.key == pygame.K_r):
                networkBot.sendNextGame()
            if(event.key == pygame.K_e):
                networkBot.sendEndAllRounds()

def drawLeaderboard():
    scores = networkBot.getScores()
    if(scores == None):
        return False
    screen.fill(BACKGROUND_COLOR)
    rounds = len(scores)
    floatRounds = float(rounds)
    avgScore = 0.0
    highScore = 0
    lowScore = 11
    avgRescued = 0.0
    mostRescued = 0
    leastRescued = 11
    avgLost = 0.0
    mostLost = 0
    leastLost = 11
    for score in scores:
        pointScore = score.rescued - score.lost
        highScore = max(highScore,pointScore)
        lowScore = min(lowScore,pointScore)
        avgScore += float(pointScore)/floatRounds
        mostRescued = max(mostRescued,score.rescued)
        leastRescued = min(lowScore,score.rescued)
        avgRescued += float(score.rescued)/floatRounds
        mostLost = max(mostLost,score.lost)
        leastLost = min(lowScore,score.lost)
        avgLost += float(score.lost)/floatRounds
    textsurface = myfont.render('Score: avg=' + "{:.3f}".format(avgScore) + ' high=' + str(highScore) + ' low=' + str(lowScore), True, RED)
    screen.blit(textsurface,(0,0))
    textsurface = myfont.render('Rescued: avg=' + "{:.3f}".format(avgRescued) + ' high=' + str(mostRescued) + ' low=' + str(leastRescued), True, RED)
    screen.blit(textsurface,(0,fontSize))
    textsurface = myfont.render('Lost: avg=' + "{:.3f}".format(avgLost) + ' high=' + str(mostLost) + ' low=' + str(leastLost), True, RED)
    screen.blit(textsurface,(0,2*fontSize))
    pygame.display.flip()
    return True


def draw(sim):
    if(sim == None || sim == simulator.ALL_ROUNDS_DONE):
        return
    global neverDrawn
    neverDrawn = False
    screen.fill(BACKGROUND_COLOR)
    textMargin = fontSize
    textsurface = myfont.render('round:' + str(sim.simRound) + ' frame:' + str(sim.frame) + ' score:' + str(sim.score.rescued - sim.score.lost), True, RED)
    screen.blit(textsurface,(0,0))
    if(interactiveMode):
        textsurface = myfont.render('MODE: INTERACTIVE', True, RED)
        screen.blit(textsurface,(0,fontSize))
        textMargin += fontSize
    pieceWidth = width/sim.board.width - 2*MARGIN
    pieceHeight = (height-textMargin)/sim.board.height - 2*MARGIN
    for x in range(sim.board.width):
        for y in range(sim.board.height):
            pygame.draw.rect(screen,
                            EMPTY_COLOR,
                            [(pieceWidth + 2*MARGIN) * x + MARGIN,
                            (pieceHeight + 2*MARGIN) * y + MARGIN + textMargin,
                            pieceWidth,
                            pieceHeight])
    for entity in sim.board.entities:
        if(entity.ownerId is None):
                image = entityToImage[entity.boardPiece]
                image = pygame.transform.scale(image, (int(pieceWidth),int(pieceHeight)))
                rect = pygame.Rect((pieceWidth + 2*MARGIN) * entity.position.x + MARGIN,
                    (pieceHeight + 2*MARGIN) * entity.position.y + MARGIN + textMargin,
                    pieceWidth,
                    pieceHeight)
                screen.blit(image, rect)
    pygame.display.flip()

FPS = 30
clock = pygame.time.Clock() # Create a clock object

while 1:
    processInput(pygame.event.get())
    if(sim != simulator.ALL_ROUNDS_DONE):
        newSim = getNewSim()
        if(newSim == simulator.ALL_ROUNDS_DONE and drawLeaderboard()):
            sim = simulator.ALL_ROUNDS_DONE
        else:
            simChanged = False
            if((newSim is None) != (sim is None)):
                simChanged = True
            elif((newSim is not None) and (sim is not None)):
                simChanged = newSim.frame != sim.frame or newSim.simRound != sim.simRound
            sim = newSim
            if(simChanged or neverDrawn):
                draw(sim)
    clock.tick(FPS)