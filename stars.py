"""
Module for creating and drawing the main stars
"""

import pygame
from pygame.locals import *
from random import randint

starColours = pygame.image.load("starGradient.png") # Loads star colours from file

dimLight = 0.15 # Brightness of flairs around star

class star:

    def __init__(self, maxX, maxY, allStars):

        self.temp = randint(0, 29) # encoded using temp = (T-3000) / 10000
        self.size = randint(30, 50 + (self.temp * 2)) # Creates size, slightly influenced by temperature

        self.exclusionRadius = self.size * 10 # Radius that no other stars can be within

        placed = False
        while not placed: # Repeats until valid location found

            placed = True
            self.x = randint(-1 * maxX, maxX) # Randomly chooses location
            self.y = randint(-1 * maxY, maxY)

            # search nearby stars
            for s in allStars: # Goes through all current stars

                dx = s.x - self.x
                dy = s.y - self.y
                d = dx ** 2 + dy ** 2 # Works out distance to star
                if d < (s.exclusionRadius + self.exclusionRadius) ** 2: # If it is less than the exclusion zones
                    placed = False # Mark as invalid location

        # generate surface
        self.surface = pygame.Surface((self.size * 2, self.size * 2), flags=SRCALPHA) # Creates surface to draw
        self.colour = starColours.get_at((self.temp, 0)) # Fetches colour from file based on temperature

        if self.temp > 1: # Also fetches a slightly darker/cooler colour
            self.darkColour = starColours.get_at((self.temp - 2, 0))
        else:
            self.darkColour = starColours.get_at((self.temp + 1, 0))

        pygame.draw.circle(self.surface, self.colour, (self.size, self.size), self.size) # Draws base circle

        # add dark spots
        for x in range(0, self.size * 2): # Goes through each pixel on the circle
            for y in range(0, self.size * 2):

                if self.surface.get_at((x, y))[3] != 0: # if not transparent
                    if randint(0,3) == 0:
                        self.surface.set_at((x, y), self.darkColour) # Randomly darkens some pixels

        # flares
        self.flairs = []
        max = int(self.size * (float(randint(110, 130)) / 100.0)) # Determines the max length of the flairs
        angle = 0
        while angle < 360: # Goes in a full circle creating new flair verticies

            v = pygame.math.Vector2(0, randint(self.size, max)) # Creates a new vertical vector
            v = v.rotate(angle) # Rotates to required angle
            self.flairs.append(v)

            angle += randint(5, 20)

    def draw(self, screen, cameraPos, screenSize):

        drawX = self.x - cameraPos[0] + (screenSize[0] / 2) # centre of star
        drawY = self.y - cameraPos[1] + (screenSize[1] / 2)

        # If on screen
        if drawX + self.size > 0 and drawX - self.size < screenSize[0] and drawY + self.size > 0 and drawY - self.size < screenSize[1]:

            # draw flairs
            flairPoints = [] # Flairs that are a part of the body of the star
            glowPoints = [] # Glowing around the star
            glowPoints2 = [] # Faint glowing extending further around the star
            for flair in self.flairs:
                flairPoints.append([drawX + flair.x, drawY + flair.y]) # Adds the vector to the centre of the star
                glowPoints.append([drawX + flair.x * 1.5, drawY + flair.y * 1.5]) # Adds same vector but scales
                glowPoints2.append([drawX + flair.x * 2, drawY + flair.y * 2]) # Scales even larger

            # move flairs
            for f in range(len(self.flairs)):
                l = self.flairs[f].magnitude() # Gets current size
                l += randint(-12, 10) / 10.0 # Randomly shifts size, generally tends to shrink
                if l < self.size: # If length of flair goes inside of star, push it out
                    l = self.size
                if l > self.size * 2: # If flair gets too large, hold it back
                    l = self.size * 2
                self.flairs[f].scale_to_length(l)

            # Draws different levels of flairs
            pygame.draw.polygon(screen, (self.colour[0] * dimLight / 2, self.darkColour[1] * dimLight / 2, self.darkColour[2] * dimLight / 2), glowPoints2)
            pygame.draw.polygon(screen, (self.darkColour[0] * dimLight, self.darkColour[1] * dimLight, self.darkColour[2] * dimLight), glowPoints)
            pygame.draw.polygon(screen, self.colour, flairPoints)

            screen.blit(self.surface, (drawX - self.size, drawY - self.size)) # Draws main surface