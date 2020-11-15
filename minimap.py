"""
Module for drawing a minimap in the corner of the screen
"""

import pygame

def draw(screen, universeSize, cameraPos, screenSize, allStars):

    mapScale = universeSize[0] / 200.0 # determines the scale factor so that minimap is always 200px in size

    mmWidth = universeSize[0] / mapScale # width of map to display
    mmHeight = universeSize[1] / mapScale # height of map to display

    pygame.draw.rect(screen, (255, 255, 255), (0, 0, int(mmWidth), int(mmHeight)), 2) # draws black background
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, int(mmWidth), int(mmHeight))) # white border

    # camera view
    mmX = cameraPos[0] / mapScale # scales the camera position and viewing area
    mmY = cameraPos[1] / mapScale
    mmW = screenSize[0] / mapScale
    mmH = screenSize[1] / mapScale

    # draw stars
    for star in allStars:
        sX = star.x / mapScale # scales each star position and size
        sY = star.y / mapScale
        sS = star.size / mapScale * 2

        pygame.draw.circle(screen, star.colour, (sX + mmWidth / 2, sY + mmHeight / 2), sS) # draws each star

    pygame.draw.rect(screen, (255, 0, 0), (int(mmX - mmW / 2 + mmWidth / 2), int(mmY - mmH / 2 + mmHeight / 2), int(mmW), int(mmH)), 1) # draws camera view