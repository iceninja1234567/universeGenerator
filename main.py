import pygame
from pygame.locals import *
import minimap

pygame.init()
clock = pygame.time.Clock()
windowSize = [1500, 750]  # size of window
mainScreen = pygame.display.set_mode(windowSize)

screenSize = windowSize # Size of camera view
screen = pygame.Surface(windowSize) # Main surface to blit everything on to which is then scaled and blitted to mainScreen

universeScale = 10  # Automatically sets settings based on this value
universeSize = [universeScale * 1000, universeScale * 1000]  # size of the entire universe

import starField
starField.generate(universeScale * 500, universeSize[0] / 2, universeSize[1] / 2)  # create background stars

import stars
allStars = [] # List of all stars in universe
for i in range(0, int(universeScale * 0.8)): # Creates 0.8 stars per 1 universeScale
    allStars.append(stars.star(universeSize[0] / 2 - 1000, universeSize[1] / 2 - 1000, allStars)) # Randomly creates star with 1000px buffer around edge of universe
    allStars[-1].surface.convert()
    for planet in allStars[-1].planets:
        planet.surface.convert_alpha()

cameraPos = [0, 0]  # centre of the camera view
dragging = False # If the camera is being dragged by the mouse
targetStar = 0 # Current star to focus camera on
targetPlanet = 0 # Current planet to focus camera on
autoCamera = False # If the camera is automatically scrolling between stars
autoCameraTimer = 0 # Timer to record how long the camera is focused on an object
targetZoom = 1 # What zoom value the autoCamera requires

minimapOn = True # If the minimap is displayed

messageTimer = 0 # Timer for on screen messages
message = "" # Message to display on screen
gameFont = pygame.font.Font("gameFont.otf", 30) # Main font for messages
titleFont = pygame.font.Font("gameFont.otf", 100) # Font size for title
titleTimer = 0 # Timer to determine when to hide the title
titleOn = True # If the title is shown or not

zoom = 1 # Zoom of camera
simulationSpeed = 1 # Speed of planets' motion

def updateZoom(): # Updates the screen when the zoom changes

    global zoom, screenSize, windowSize, screen

    screenSize = [windowSize[0] / zoom, windowSize[1] / zoom] # Creates a smaller surface is zoomed in
    screen = pygame.Surface(screenSize)

title_surf = titleFont.render("UNIVERSE SIMULATOR", False, (255, 255, 255))
msg_cache = {}  # store message surfaces so that they only need to be rendered once
running = True
while running:

    clock.tick(60)
    fps = int(clock.get_fps())
    pygame.display.set_caption("Universe | FPS: " + str(fps))

    screen.fill((0, 0, 0))

    if autoCamera: # If autoCamera is enabled

        if targetZoom > zoom: # If the autoCamera requires a higher zoom than the current value
            zoom += 0.01 # Slowly zoom in
        elif targetZoom < zoom: # If zoomed in too far
            zoom -= 0.01 # Slowly zoom out

        updateZoom() # Updates surface

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == K_c: # Toggles autoCamera
                autoCamera = not autoCamera
            elif event.key == K_m: # Toggles minimap
                minimapOn = not minimapOn

            elif event.key == 61: # + key

                if simulationSpeed >= 1:
                    simulationSpeed += 1 # Increases simulation speed
                elif simulationSpeed < 1:
                    simulationSpeed = round(simulationSpeed + 0.1, 1)

                message = str(round(simulationSpeed, 1)) + "x simulation speed"
                messageTimer = fps * 2 # Shows message for 2 seconds

            elif event.key == 45: # - key

                if simulationSpeed > 1:
                    simulationSpeed -= 1 # Slows simulation
                elif simulationSpeed > 0: # If already below 1x speed
                    simulationSpeed = round(simulationSpeed - 0.1, 1) # Decrease in 0.1 increments

                message = str(round(simulationSpeed, 1)) + "x simulation speed"
                messageTimer = fps * 2

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1: # Left click
                dragging = True  # start dragging when mouse down

            elif event.button == 4: # Zoom in (scroll wheel up)
                if zoom >= 1:
                    zoom += 1 # Increase zoom
                elif zoom < 1:
                    zoom = round(zoom, 1) + 0.1

                updateZoom()

                message = str(round(zoom, 1)) + "x zoom"
                messageTimer = fps * 2

            elif event.button == 5: # Zoom out (scroll wheel down)
                if zoom > 1:
                    zoom -= 1
                elif 0.15 < zoom <= 1: # If between 0.15x and 1x zoom
                    zoom = round(zoom, 1) - 0.1 # Decrease in 0.1 increments

                    viewX = windowSize[0] / zoom # Work out new camera view
                    viewY = windowSize[1] / zoom
                    if viewX > universeSize[0] or viewY > universeSize[1]: # If camera view is larger than the actual universe
                        zoom = round(zoom, 1) + 0.1 # Zoom back in

                updateZoom()

                message = str(round(zoom, 1)) + "x zoom"
                messageTimer = fps * 2

        elif event.type == pygame.MOUSEBUTTONUP:

            dragging = False  # stop dragging when mouse up

        elif event.type == pygame.MOUSEMOTION:

            if dragging:  # if mouse down

                cameraPos[0] -= event.rel[0] / zoom  # move camera
                cameraPos[1] -= event.rel[1] / zoom

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
        star.draw(screen, cameraPos, screenSize, simulationSpeed)

    # camera scroll
    if autoCamera:
        tolerance = screenSize[1]/2 # Area in centre of screen that counts as 'in focus'
        if allStars[targetStar].planets[targetPlanet].x - tolerance < cameraPos[0] < allStars[targetStar].planets[targetPlanet].x + tolerance and allStars[targetStar].planets[targetPlanet].y - tolerance < cameraPos[1] < allStars[targetStar].planets[targetPlanet].y + tolerance:
            autoCameraTimer += 1 # If the star is 'in focus', increment timer
            targetZoom = 3 # Attempt to go to 3x zoom
        else:
            targetZoom = 1 # Zoom back to original

        if autoCameraTimer > fps * 5: # After 5 seconds of being 'in focus'
            autoCameraTimer = 0
            targetPlanet += 1 # Move to next planet
            if targetPlanet > len(allStars[targetStar].planets) - 1: # If already targetted all planets
                targetPlanet = 0
                targetStar += 1 # Move to next star

                if targetStar > len(allStars) - 1: # If all stars visited
                    targetStar = 0 # Restart

        speed = 0.02 # autoCamera scroll speed
        dx = allStars[targetStar].planets[targetPlanet].x - cameraPos[0] # Speed based on distance to target
        dy = allStars[targetStar].planets[targetPlanet].y - cameraPos[1]
        cameraPos[0] += dx * speed
        cameraPos[1] += dy * speed

    if zoom != 1:
        screen2 = pygame.transform.scale(screen, windowSize) # Scales surface to size of screen
        mainScreen.blit(screen2, (0,0))
    else:
        mainScreen.blit(screen, (0,0))

    if minimapOn:
        minimap.draw(mainScreen, universeSize, cameraPos, screenSize, allStars)  # draws minimap

    # Messages
    if messageTimer > 0:
        messageTimer -= 1
        msg_surf = msg_cache.get(message)
        if msg_surf is None:
            msg_surf = gameFont.render(message, False, (255, 255, 255), (0, 0, 0))
            msg_cache[message] = msg_surf
        
        mainScreen.blit(msg_surf, (10, windowSize[1] - 10 - l.get_height()))

    # Title
    if (titleTimer < fps * 5 and titleOn) or (titleOn and fps < 10):
        titleTimer += 1

        # l = titleFont.render("UNIVERSE SIMULATOR", False, (255,255,255))
        x = windowSize[0]/2 - title_surf.get_width()/2
        y = windowSize[1]/2 - title_surf.get_height()/2
        mainScreen.blit(title_surf, (x, y))

    else:
        titleOn = False

    pygame.display.update()

pygame.quit()
