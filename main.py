import pygame
from pygame.locals import *
import minimap

universeScale = 10  # Uses recommended settings for this size
universeSize = [universeScale * 1000, universeScale * 1000]  # size of the entire universe

import starField

starField.generate(universeScale * 500, universeSize[0] / 2, universeSize[1] / 2)  # create background stars

import stars

allStars = []
for i in range(0, universeScale):  # creates 5 large stars
    allStars.append(stars.star(universeSize[0] / 2, universeSize[1] / 2, allStars))

pygame.init()
clock = pygame.time.Clock()
screenSize = [1500, 750]  # size of window
screen = pygame.display.set_mode(screenSize)

cameraPos = [0, 0]  # centre of the camera view
dragging = False
currentTarget = 0
autoCamera = False

running = True
while running:

    clock.tick(60)
    fps = int(clock.get_fps())
    pygame.display.set_caption("Universe | FPS: " + str(fps))

    screen.fill((0, 0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == K_c:
                autoCamera = not autoCamera

        elif event.type == pygame.MOUSEBUTTONDOWN:

            dragging = True  # start dragging when mouse down

        elif event.type == pygame.MOUSEBUTTONUP:

            dragging = False  # stop dragging when mouse up

        elif event.type == pygame.MOUSEMOTION:

            if dragging:  # if mouse down

                cameraPos[0] -= event.rel[0]  # move camera
                cameraPos[1] -= event.rel[1]

                if cameraPos[0] - (screenSize[0] / 2) < universeSize[0] / -2:  # if camera goes outside of universe size, move back in
                    cameraPos[0] = universeSize[0] / -2 + (screenSize[0] / 2)
                elif cameraPos[0] + (screenSize[0] / 2) > universeSize[0] / 2:
                    cameraPos[0] = universeSize[0] / 2 - (screenSize[0] / 2)

                if cameraPos[1] - (screenSize[1] / 2) < universeSize[1] / -2:
                    cameraPos[1] = universeSize[1] / -2 + (screenSize[1] / 2)
                elif cameraPos[1] + (screenSize[1] / 2) > universeSize[1] / 2:
                    cameraPos[1] = universeSize[1] / 2 - (screenSize[1] / 2)

    starField.allDraw(screen, cameraPos, screenSize)  # renders background stars

    for star in allStars:  # draws each main star
        star.draw(screen, cameraPos, screenSize)

    minimap.draw(screen, universeSize, cameraPos, screenSize, allStars)  # draws minimap

    # camera scroll
    if autoCamera:
        tolerance = 20
        if allStars[currentTarget].x - tolerance < cameraPos[0] < allStars[currentTarget].x + tolerance and allStars[currentTarget].y - tolerance < cameraPos[1] < allStars[currentTarget].y + tolerance:
            currentTarget += 1
            if currentTarget > len(allStars) - 1:
                currentTarget = 0

        speed = 0.02
        dx = allStars[currentTarget].x - cameraPos[0]
        dy = allStars[currentTarget].y - cameraPos[1]
        cameraPos[0] += dx * speed
        cameraPos[1] += dy * speed

    pygame.display.update()

pygame.quit()
