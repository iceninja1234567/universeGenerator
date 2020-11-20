"""
Module for creating and drawing moons orbiting planets
"""

import pygame
from pygame.locals import *
from math import sqrt, pi
from random import randint, choice, random
import planets

orbitalPeriodConstant = 500 # Multiplier for orbital speed of moons
rotationSpeedConstant = 1 # Multiplier for rotation speed of moons

class moon():

    def __init__(self, parentPlanet):

        maxSize = parentPlanet.size / 3 # Limit size based on planet it is orbiting
        self.size = randint(3, int(maxSize)) # Radius of moon
        self.exclusionRadius = self.size * 1.2 # Area around moon that no other object can generate in

        self.x = 0
        self.y = 0

        valid = False
        while not valid:
            valid = True

            self.orbitalRadius = randint(int(parentPlanet.size * 3), parentPlanet.exclusionRadius)  # Picks random orbital radius

            for otherMoon in parentPlanet.moons:  # Goes through all other moons

                dr = abs(self.orbitalRadius - otherMoon.orbitalRadius) # Works out distance between all other moons
                if dr < self.exclusionRadius + otherMoon.exclusionRadius: # If within the exclusion zone of another moon
                    valid = False # Discard this position

        self.rotation = 0 # Current axial rotation
        self.rotationSpeed = randint(1, 5) * choice([-1, 1]) * rotationSpeedConstant  # Degrees to rotate per second

        t2 = (self.orbitalRadius ** 3) / (parentPlanet.size ** 3) * orbitalPeriodConstant  # t^2 proportional to r^3 / M, M proportional to R^3 so t^2 = r^3 / R^3
        self.orbitalPeriod = sqrt(t2)  # Time in frames to complete 1 orbit
        self.orbitalSpeed = (2 * pi) / self.orbitalPeriod  # Radians per second to rotate through
        self.orbitalAngle = pi * random() * 2  # Picks a random starting point

        self.surface = pygame.Surface((self.size * 2, self.size * 2), flags=SRCALPHA) # Main moon surface
        c = randint(50,200) # Random gray colour
        self.mainColour = (c,c,c)  # Picks random grey colour
        c = randint(10, 100) # Darker gray colour for spots
        self.darkColour = (c,c,c)
        pygame.draw.circle(self.surface, self.mainColour, (self.size, self.size),self.size * 0.9)

        surfacePoints = []
        angle = 0
        while angle < 360:
            v = pygame.math.Vector2(0, randint(int(self.size * 0.9), self.size))
            v = v.rotate(angle)
            surfacePoints.append([self.size + v.x, self.size + v.y])
            angle += randint(5, 15)
        pygame.draw.polygon(self.surface, self.mainColour, surfacePoints)

        for x in range(0, self.size * 2):  # Goes through each pixel on the circle
            for y in range(0, self.size * 2):

                if self.surface.get_at((x, y))[3] != 0:  # if not transparent
                    if randint(0, 3) == 0:
                        self.surface.set_at((x, y), self.darkColour)  # Randomly darkens some pixels

        #pygame.image.save(self.surface, "image\\" + str(self.rotationSpeed) + str(self.orbitalSpeed) + ".png")

    def draw(self, screen, cameraPos, screenSize, parentStar, simulationSpeed):

        # move in orbit
        self.orbitalAngle += self.orbitalSpeed * simulationSpeed
        self.rotation += self.rotationSpeed * simulationSpeed

        # finds position to draw
        v = pygame.math.Vector2(0, self.orbitalRadius) # Creates vector with radius r
        v = v.rotate_rad(self.orbitalAngle) # Rotates to position
        pos = [parentStar.x, parentStar.y] + v # Finds location

        self.x = pos[0] # Stores co-ordinate for other purposes
        self.y = pos[1]

        drawX = pos[0] - cameraPos[0] + (screenSize[0] / 2)  # centre of planet
        drawY = pos[1] - cameraPos[1] + (screenSize[1] / 2)
        if drawX + self.size > 0 and drawX - self.size < screenSize[0] and drawY + self.size > 0 and drawY - self.size < screenSize[1]:

            rotatedImage = pygame.transform.rotate(self.surface, self.rotation)
            screen.blit(rotatedImage, (drawX - rotatedImage.get_width()/2, drawY - rotatedImage.get_height()/2))