"""
Module for drawing background stars with parallax
"""

import pygame
from random import randint

starScale = 1 # how much the z value effects star scale
flattenFactor = 1 # < 1, how much the z value of a star effects the parallax

class star:

    def __init__(self, maxX, maxY):

        self.x = randint(-maxX, maxX) # Random x position within the universe size
        self.y = randint(-maxY, maxY)
        self.z = randint(1, 20) # higher = further, the z value is how far back the star will appear

        self.size = randint(5, 10)

        self.apparentSize = float(self.size) / (self.z * starScale) # The actual size to draw the star based on it's physical size and z-distance from camera

        self.c = randint(100, 255 - self.size) # Dims stars that are further back

        if self.apparentSize < 1:
            self.apparentSize = randint(1,2)

    def draw(self, screen, cameraPos, screenSize):

        global drawn

        # Finds co-ordinates to draw based on camera position and z-value
        drawX = self.x - (float(cameraPos[0]) / self.z * flattenFactor) + (screenSize[0]/2)
        drawY = self.y - (float(cameraPos[1]) / self.z * flattenFactor) + (screenSize[1]/2)

        # if on screen, draw
        if drawX + self.apparentSize > 0 and drawX - self.apparentSize < screenSize[0] and drawY + self.apparentSize > 0 and drawY - self.apparentSize < screenSize[1]:
            drawn += 1
            if self.apparentSize < 1:
                pygame.draw.circle(screen, (255, 0, 0), (drawX, drawY), 2)
            pygame.draw.circle(screen, (self.c, self.c, self.c), (drawX, drawY), self.apparentSize)

allStarField = []
def generate(density, maxX, maxY): # function for generating many stars at once

    global allStarField

    for i in range(density):
        allStarField.append(star(maxX, maxY))

    allStarField = sorted(allStarField, key=lambda x: x.z, reverse=True)

drawn = 0
def allDraw(screen, cameraPos, screenSize): # function for drawing all stars at once
    global drawn
    drawn = 0
    for star in allStarField:
        star.draw(screen, cameraPos, screenSize)
    print(drawn)