import pygame
from pygame.rect import Rect

running = True

# set window size
width = 360
height = 100

pygame.init()
screen = pygame.display.set_mode((width, height), 1, 16)

# title
pygame.display.set_caption("3DAB")
# starting position
x = 100
pygame.draw.rect(screen, (255,0,0), Rect(x, 5, 10, 90))
pygame.display.update(pygame.Rect(0,0,width,height))

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    button = pygame.mouse.get_pressed()
    if button[0] != 0:
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        a = x - 5
        if a < 0:
            a = 0
        pygame.draw.rect(screen, (0,0,0), Rect(0, 0, width, height))
        # pygame.display.update(pygame.Rect(0,0,width,height))
        pygame.draw.rect(screen, (255,0,0), Rect(a, 5, 10, 90))
        pygame.display.update(pygame.Rect(0, 0, width, height))

    # makes the pygame update every frame
    pygame.display.update()