import sys, pygame, simulator
pygame.init()

# Define some colors
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = width, height = 700, 500
speed = [2, 2]
black = 0, 0, 0

pygame.display.set_caption("PUZZLER 2018")

screen = pygame.display.set_mode(size)

ball = pygame.image.load("assets/badHexy.png")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()