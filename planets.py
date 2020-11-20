import pygame
from pygame.locals import *
from random import randint, choice, random
from math import sqrt, pi
import stars, moons

orbitalPeriodConstant = 5000 # Multiplier for orbital speed of planets
rotationSpeedConstant = 1 # Multiplier for rotation speed of planets
shadeDim = 100 # Darkness of dark-side of planets (lower is darker)
atmDim = 0.4 # Dimness of atmosphere

gasGiantColours = pygame.image.load("gasGiantColours.png")

class planet():

    def __init__(self, parentStar):

        self.size = randint(10, int(parentStar.size / 2.5)) # Planet radius
        self.exclusionRadius = self.size * 5

        self.x = 0
        self.y = 0

        valid = False
        while not valid:
            valid = True

            self.orbitalRadius = randint(int(parentStar.size * 3), parentStar.exclusionRadius) # Distance to orbit at

            for otherPlanet in parentStar.planets: # Goes through all other stars

                dr = abs(self.orbitalRadius - otherPlanet.orbitalRadius)
                if dr < self.exclusionRadius + otherPlanet.exclusionRadius:
                    valid = False

        self.rotation = 0
        self.rotationSpeed = randint(1, 5) * choice([-1, 1]) * rotationSpeedConstant # Degrees to rotate per second

        t2 = (self.orbitalRadius ** 3) / (parentStar.size ** 3) * orbitalPeriodConstant # t^2 proportional to r^3 / M, M proportional to R^3 so t^2 = r^3 / R^ 3
        self.orbitalPeriod = sqrt(t2) # Time in frames to complete 1 orbit
        self.orbitalSpeed = (2 * pi) / self.orbitalPeriod# Radians per second to rotate through

        self.orbitalAngle = pi * random() * 2 # Picks a random starting point

        self.moons = []
        maxMoons = randint(0,1)
        if self.size > 20:
            maxMoons = 2
        for i in range(maxMoons):
            self.moons.append(moons.moon(self))
            if i == 2:
                print(0)

        # generate surface
        self.type = choice(["gas", "terrain"]) # Picks random planet type
        self.surface = pygame.Surface((self.size * 2, self.size * 2), flags=SRCALPHA)
        self.ring = False
        if self.type == "gas":
            self.mainColour = randint(0, 99) # Picks random main colour
            pygame.draw.circle(self.surface, gasGiantColours.get_at((self.mainColour, 0)), (self.size, self.size), self.size) # Creates base circle

            # create bands of random colours
            for i in range(5, 10 + self.size // 10): # Random number of bands

                bandHeight = randint(2, 10) # Height of band
                bandY = randint(0, self.size*2 - bandHeight) # Y position of top of band
                newColour = -1 # Picks a random colour
                while newColour < 0 or newColour > 99:
                    newColour = self.mainColour + (randint(5, 10) * choice([-1, 1])) # Picks random colour that is close to planet colour
                c = gasGiantColours.get_at((newColour, 0)) # Gets RGB value of colour

                for x in range(self.size * 2):

                    for y in range(bandHeight):

                        if self.surface.get_at((x, bandY + y))[3] != 0: # not empty
                            if randint(0,3) != 0: # Random specks
                                self.surface.set_at((x, bandY + y), c)

            # random swirls
            for i in range(3, 5):

                newColour = -1
                while newColour < 0 or newColour > 99:
                    newColour = self.mainColour + (randint(5, 10) * choice([-1, 1])) # Picks random colour
                c = gasGiantColours.get_at((newColour, 0))

                x, y = randint(0, self.size * 2), randint(0, self.size * 2) # Picks random point on surface
                for ox in range(randint(-10, -2), randint(2, 10)): # Goes through nearby tiles
                    for oy in range(randint(-10, -2), randint(2, 10)):

                        if 0 < x + ox < self.size * 2 and 0 < y + oy < self.size * 2: # If within planet

                            if self.surface.get_at((x + ox, y + oy))[3] != 0:  # not empty
                                if randint(0, 3) != 0: # Random specks
                                    self.surface.set_at((x + ox, y + oy), c)

            if randint(1, 5) == 1: # Rings
                self.ring = True
                self.ringRadius = randint(int(self.size * 2), int(self.size * 3)) # Inner radius of ring
                self.ringThickness = randint(3, 8) # Thickness of ring
                self.outerRadius = self.ringRadius + self.ringThickness # Outer radius of ring
                self.ringSurface = pygame.Surface((self.outerRadius * 2, self.outerRadius * 2), flags=SRCALPHA)
                for i in range(2, 5): # Random number of stripes

                    newColour = -1  # Picks a random colour
                    while newColour < 0 or newColour > 99:
                        newColour = self.mainColour + (randint(2, 5) * choice([-1, 1]))  # Picks random colour that is close to planet colour
                    c = gasGiantColours.get_at((newColour, 0))  # Gets RGB value of colour

                    pygame.draw.circle(self.ringSurface, c, (self.outerRadius, self.outerRadius), self.ringRadius + randint(2, self.ringThickness), randint(2, self.ringThickness))

            #pygame.image.save(self.surface, "image\\" + str(self.rotationSpeed) + str(self.orbitalSpeed) + ".png")

        elif self.type == "terrain":
            self.mainColour = randint(0, 99)  # Picks random main colour
            pygame.draw.circle(self.surface, gasGiantColours.get_at((self.mainColour, 0)), (self.size, self.size), self.size * 0.9)  # Creates base circle

            surfacePoints = []
            angle = 0
            while angle < 360: # Goes around planet and picks random angles to make protrusions
                v = pygame.math.Vector2(0, randint(int(self.size * 0.9), self.size))
                v = v.rotate(angle)
                surfacePoints.append([self.size + v.x, self.size + v.y])
                angle += randint(5, 15)
            pygame.draw.polygon(self.surface, gasGiantColours.get_at((self.mainColour, 0)), surfacePoints)

            # random swirls
            newColour = -1
            while newColour < 0 or newColour > 99:
                newColour = self.mainColour + (randint(5, 10) * choice([-1, 1]))  # Picks random colour
            c = gasGiantColours.get_at((newColour, 0))

            for i in range(5, 10):

                x, y = randint(0, self.size * 2), randint(0, self.size * 2)  # Picks random point on surface
                for ox in range(randint(-10, -2), randint(2, 10)):  # Goes through nearby tiles
                    for oy in range(randint(-10, -2), randint(2, 10)):

                        if 0 < x + ox < self.size * 2 and 0 < y + oy < self.size * 2:  # If within planet

                            if self.surface.get_at((x + ox, y + oy))[3] != 0:  # not empty
                                if randint(0, 5) != 0:  # Random specks
                                    self.surface.set_at((x + ox, y + oy), c)

            # Atmosphere
            self.atmRadius = self.size * (randint(20, 30) / 10.0)
            self.atmSurface = pygame.Surface((self.atmRadius * 2, self.atmRadius * 2), flags=SRCALPHA)
            self.atmColour = randint(0, 99)
            self.atmColour = gasGiantColours.get_at((self.atmColour, 0))

            for r in range(int(self.size), int(self.atmRadius)): # Goes from planet surface to outer radius
                d = 1 - ((r - self.size) / (self.atmRadius - self.size)) # Dims colour as distance increases
                pygame.draw.circle(self.atmSurface, (self.atmColour[0] * atmDim * d, self.atmColour[1] * atmDim * d, self.atmColour[2] * atmDim * d), (self.atmRadius, self.atmRadius), r, 3)

            #pygame.image.save(self.surface, "image\\" + str(self.rotationSpeed) + str(self.orbitalSpeed) + ".png")

        # Shade
        self.shadeSurface = pygame.Surface((self.size * 2, self.size * 2)) # Surface to hold a black semi-circle
        self.shadeSurface.fill((255,255,255))
        halfSurface = pygame.Surface((self.size * 2, self.size), flags=SRCALPHA) # Half a circle size
        pygame.draw.circle(halfSurface, (shadeDim, shadeDim, shadeDim), (self.size, self.size), self.size) # Draws semi-circle
        self.shadeSurface.blit(halfSurface, (0, 0))

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

            # rotate
            if self.type == "terrain":
                screen.blit(self.atmSurface, (drawX - self.atmRadius, drawY - self.atmRadius))

            rotatedImage = pygame.transform.rotate(self.surface, self.rotation)
            screen.blit(rotatedImage, (drawX - rotatedImage.get_width()/2, drawY - rotatedImage.get_height()/2))

            # shade angle
            sAngle = v.angle_to(pygame.math.Vector2(0, 1)) # Angle between rotation and upwards vertical
            rotatedShade = pygame.transform.rotate(self.shadeSurface, sAngle + 180) # Rotates image
            screen.blit(rotatedShade, (drawX - rotatedShade.get_width()/2, drawY - rotatedShade.get_height()/2), special_flags=BLEND_RGBA_MULT) # Uses MULT flag to darken existing colours

            if self.ring:
                screen.blit(self.ringSurface, (drawX - self.outerRadius, drawY - self.outerRadius))

        # draws moons
        for moon in self.moons:
            moon.draw(screen, cameraPos, screenSize, self, simulationSpeed)