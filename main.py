"""
112 Project Option 3 4/26/24
By: Adam Kollgaard

---------------
File structure:
main.py - This is the main file! Run the game from here. Make sure cmu_graphics is
in the same directory.

Graphics.py - This is all the stuff that creates a graphics engine. I choose to make
it into a class because I can create multiple graphics engines to run multiple scenes
at the same time or at different moments. This is why the beginning animation is possible

Object.py - This contains all the parent classes for most of the shape data. Sorry for
naming confusing, but I mix and match shape/object a little. A shape/object is anything
that gets rendering in the game.

Model.py - This contains all the data for creating arbitray shapes, ships, enemies,
buildings and other stuff.

test.py - Random stuff to test python things

Engine.py - An old version of the graphics engine. It is not used; deprecated :(
---------------

For my project, I created a game that is essientally very similiar to the game starfox.
It is a endless version of the game that is more of a snippet to the actual game.
Think of it like a demo or something similar. The main goal of the project was to
use 3D graphics to draw everything. 

The 3D graphics engine uses a Perspective Projection Matrix, however I have not
implemented any lighting/shadows/anything super complicated. Each shape is made
of multiple polygons that are of any 2D shape which are represented by vertices
in 3D space. Then those vertices are taken a vectors from some arbitrary origin point. 
The graphics engine converts these 3D points to 2D points that can then be represented
on the screen. At the end, I simply use drawPolygon to create the shapes. Then some
list sorting can be done to figure out which object is closer to the camera to find
what objects need to be drawn first. It is a relatively simple engine that uses a 
lot information from the following sources:
https://en.wikipedia.org/wiki/3D_projection
https://www.3dgep.com/understanding-the-view-matrix/
https://www.youtube.com/watch?v=EqNcqBdrNyI&ab_channel=pikuma

After hitting the play button, the game starts a little animation and then you enter
the actually playing part. The playing part uses WASD as the controls, space to shoot,
F to boost forward, then press H to change to first-person point of view. In this view
you can use the mouse to control the ship where the center of the screen centers the view
of the ship. You can not use WASD in first person mode! All other commands still work.
Try not to get hit by the other enemies and avoid the obstacles. The buildings to the left
and right are the bounds; do not leave! If you hit the ground or go to high you will also lose.
The bar in the bottom left corner shows your health in red and then the boost in blue.
You can also hit z for extra camera data in the top left corner, but this is mostly for 
debugging purposes.

GRADING SHORTCUTS:
You can press r at any moment to enter the actual playing part of the game. This works for any
screen. Mostly if you want to skip the beginning animation.
You can also press m while playing to enter back into the menu screen.

"""

from cmu_graphics import *
from Graphics import Graphics
from Model import *
import time
import math
import random

def onAppStart(app):
    app.width = 1024
    app.height = 768
    app.stars = [] # This is so the menu/animation screen can both use it.

class Star():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.color = 'white'
        self.growCounter = 0
        self.t = 0
        self.timeSteps = 25
        # This limits the likelyhood of the there being two stars
        # that are essientally the same
        self.uniqueCode = random.randrange(99999)

    def __repr__(self):
        return f"Star at ({self.x}, {self.y}): {self.uniqueCode}"
    
    def __eq__(self, other):
        return (isinstance(other, Star) and
                self.x == other.x and
                self.y == other.y and
                self.uniqueCode == other.uniqueCode)
    
    def __hash__(self):
        return hash(str(self))

    def startGrowing(self):
        self.growCounter += 1

    def moveStar(self, dx, dy):
        self.x += dx
        self.y += dy

    def growStar(self):
        if self.growCounter > 6:
            self.growCounter = 0
            self.width = 4
            self.height = 4
        elif self.growCounter > 3:
            self.height -= 1
            self.width -= 1
            self.growCounter += 1
        elif self.growCounter >= 1:
            self.width += 1
            self.height += 1
            self.growCounter += 1

def drawStars(app):
    for star in app.stars:
        drawRect(star.x, star.y, star.width, star.height, fill=star.color)

###############################################################################
# Menu Screen
###############################################################################

def menuScreen_onScreenActivate(app):
    app.stepsPerSecond = 10
    app.mx = 0
    app.my = 0
    app.hovering = False
    app.playAnimation = False
    createStars(app, 150) # Creates 150 stars

    # Stuff for the starting animation
    app.titleX = app.width / 2
    app.titleY = app.height / 4
    app.playButtonX = app.width / 3
    app.playButtonY = app.height * 3/4
    app.playButtonTextX = app.width / 2
    app.playButtonTextY = app.height * 3/4 + 50

def createStars(app, starCount): 
    for i in range(starCount):
        randx = random.randrange(app.width)
        randy = random.randrange(app.height)
        app.stars.append(Star(randx, randy))
        # These stars are special because they change from
        # moving to the left to moving to the center.
        timeStep = 60
        if randx <= app.width / 3 or randx > app.width * 2/3:
            timeStep += 80
        if randy <= app.height / 3 or randy > app.height * 2/3:
            timeStep += 80
        app.stars[-1].timeSteps = timeStep

def menuScreen_redrawAll(app):
    # Draw background
    drawRect(0, 0, app.width, app.height, fill='black')

    drawStars(app)

    # Draw the mouse positions for debugging/testing
    drawLabel(f'({app.mx}, {app.my})', 30, 30, fill='white')

    if app.titleY > -50:
        drawLabel('StarFox-112', app.titleX, app.titleY, size=80, bold=True, fill='white')

    if app.playButtonY < app.height:
        color = 'lightgreen' if app.hovering else 'black'
        drawRect(app.playButtonX, app.playButtonY, app.width / 3, 100, fill=color, border='lightgreen')
        textColor = 'black' if app.hovering else 'lightgreen'
        drawLabel('Play', app.playButtonTextX, app.playButtonTextY, size=20, fill=textColor)

def menuScreen_onMouseMove(app, mouseX, mouseY):
    app.mx = mouseX
    app.my = mouseY
    app.hovering = (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100)

def menuScreen_onMousePress(app, mouseX, mouseY):
    if (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100):
        app.stepsPerSecond = 30
        app.playAnimation = True

def menuScreen_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('playScreen')

def menuScreen_onStep(app):
    star = random.choice(app.stars)
    star.startGrowing()

    # Checks every star and if allowed twinkles/grows them
    for star in app.stars:
        star.growStar()

    if app.playAnimation:
        app.titleY -= 8
        app.playButtonY += 8
        app.playButtonTextY += 8
        if app.titleY <= -50:
            setActiveScreen('animationScreen')

###############################################################################
# Animation Screen
###############################################################################

def animationScreen_onScreenActivate(app):
    app.stepsPerSecond = 20
    app.mx = 0
    app.my = 0
    app.starsToRemove = set()
    app.engine = Graphics(app.width, app.height)
    app.engine.resetCamera()
    app.engine.moveCameraOrientation(-15, 0, 0.1)
    app.engine.addShip(shipModel(0.5), 'Adam', 2, 4, 30)
    app.player = 0
    app.engine.ships[app.player].moveShip(-15, -5, 15)
    app.engine.ships[app.player].tiltShip(0, 0, 90)
    app.shipCounter = 0
    app.moveOtherShips = False
    app.moveStarsLeft = True
    app.movePlanetCounter = 0
    app.planetY = app.width * 3/2
    app.showPlayText = False
    app.moveShipsForward = False

def animationScreen_redrawAll(app):
    # Draw background
    drawRect(0, 0, app.width, app.height, fill='black')

    drawStars(app)

    # Draw the mouse positions for debugging/testing
    drawLabel(f'({app.mx}, {app.my})', 30, 30, fill='white')

    drawCircle(app.width / 2, app.planetY, app.width / 2, fill=gradient('green', 'blue', 'blue', 'blue', start='top'))

    if app.showPlayText:
        drawLabel('Press P to save the city', app.width / 2, app.height * 4/5, fill='white', size=30, bold=True)

    # Drawing any ship/stuff
    # Note: there is no ground in space so we don't use it 
    shapes, shapeIndexes, ground, groundIndexes = app.engine.render(True)

    for i in shapeIndexes:
        allPoints = shapes[i][0]
        colors = shapes[i][1]
        indexes = shapes[i][2]
        for index in indexes:
            drawPolygon(*allPoints[index], fill=colors[index], border='black')

def animationScreen_onStep(app):
    star = random.choice(app.stars)
    star.startGrowing()

    # Checks every star and if allowed twinkles/grows them
    for star in app.stars:
        star.growStar()

    if app.moveStarsLeft:
        moveStars(app)
    else:
        moveStarsToCenter(app)
        # Adds a sufficient amount of stars
        addSurroundingStars(app)
        addSurroundingStars(app)
        addSurroundingStars(app)
        app.movePlanetCounter += 1
    removeStars(app)

    if app.engine.ships[app.player].position[0] != 0:
        app.engine.ships[app.player].moveShip(1, 0, 0)
    else:
        app.moveStarsLeft = False
        if app.engine.cameraPosition != (15, 0, 15):
            x, y, z = app.engine.cameraPosition
            x = math.cos(((1 - (app.shipCounter / 15)) * 90) * (math.pi / 180)) * 15
            z = math.sin((((app.shipCounter / 15)) * 90) * (math.pi / 180)) * 15
            app.engine.cameraPosition = (x, y, z)
            app.shipCounter += 1

        if app.engine.cameraOrientation != (0, -15, 90.1):
            app.engine.moveCameraOrientation(1, -1, 6)
        else:
            # After the camera is oriented properly start the next
            # sequence of animations where the other ships move in
            if not app.moveOtherShips:
                app.engine.addShip(shipModel(0.5), 'left1', 2, 4, 30)
                app.engine.ships[-1].moveShip(-5, -5, 0)
                app.engine.ships[-1].tiltShip(0, 0, 90)
                app.engine.addShip(shipModel(0.5), 'right1', 2, 4, 30)
                app.engine.ships[-1].moveShip(-5, -5, 30)
                app.engine.ships[-1].tiltShip(0, 0, 90)
            app.moveOtherShips = True
            
    if app.moveOtherShips:
        if app.engine.ships[1].position[2] != 10:
            app.engine.ships[1].moveShip(0, 0, 1)
        if app.engine.ships[2].position[2] != 20:
            app.engine.ships[2].moveShip(0, 0, -1)

    if app.moveShipsForward:
        for ship in app.engine.ships:
            ship.moveShip(1, 0, 0)
        
        if app.engine.ships[1].position[0] > 14:
            setActiveScreen('playScreen')

    # This is just to wait some time
    if app.movePlanetCounter >= 1 and app.planetY >= app.height * 5/4:
        app.planetY -= 5
    
    if app.movePlanetCounter >= 1 and app.planetY <= app.height * 5/4:
        app.showPlayText = True

def removeStars(app):
    for star in app.starsToRemove:
        app.stars.remove(star)
    app.starsToRemove = set()

def moveStars(app):
    starsToAdd = 0
    for star in app.stars:
        star.moveStar(5, 0)
        if star.x > app.width:
            app.starsToRemove.add(star)
            starsToAdd += 1

    for i in range(starsToAdd):
        # Have them created off screen so they move in nicely
        app.stars.append(Star(-10, random.randrange(app.height)))

def moveStarsToCenter(app):
    for star in app.stars:
        # We create an equation of a line to the center of the 
        # screen and then have the dot (x,y) move along that 
        # line so it essientally steps to the center no
        # matter it's current location
        cx = app.width / 2
        cy = app.height / 2

        mx = (star.x - cx) / -star.timeSteps
        bx = star.x
        my = (star.y - cy) / -star.timeSteps
        by = star.y
        
        dx = ((mx *star.t) + bx) - star.x
        dy = ((my * star.t) + by) - star.y

        star.moveStar(dx, dy)
        if star.t >= star.timeSteps:
            app.starsToRemove.add(star)
        star.t += 1

def addSurroundingStars(app):
    outline = random.randrange(app.height * 2 + app.width * 2)
    if outline < app.height:
        app.stars.append(Star(-10, random.randrange(app.height)))
    elif outline < app.width + app.height:
        app.stars.append(Star(random.randrange(app.width), -10))
    elif outline < app.width + app.height * 2:
        app.stars.append(Star(app.width, random.randrange(app.height)))
    elif outline < app.width * 2 + app.height * 2:
        app.stars.append(Star(random.randrange(app.width), app.height))

def animationScreen_onMouseMove(app, mx, my):
    app.mx = mx
    app.my = my

def animationScreen_onKeyPress(app, key):
    if key == 'p' and app.showPlayText:
        app.moveShipsForward = True
    elif key == 'r':
        setActiveScreen('playScreen')

###############################################################################
# Losing Screen
###############################################################################

def losingScreen_onScreenActivate(app):
    app.stepsPerSecond = 20
    app.stars = []
    createLosingScreenStars(app, 150)

def createLosingScreenStars(app, starCount):
    for i in range(starCount):
        x = random.randrange(app.width)
        y = random.randrange(app.height)
        app.stars.append(Star(x, y))

def losingScreen_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')

    drawStars(app)

    drawLabel('You lost!', app.width / 2, app.height / 2, size=50, fill='white')
    drawLabel("Press r to restart", app.width / 2, app.height / 2 + 40, size=40, fill='white')

def losingScreen_onStep(app):
    star = random.choice(app.stars)
    star.startGrowing()

    # Checks every star and if allowed twinkles/grows them
    for star in app.stars:
        star.growStar()

def losingScreen_onKeyPress(app, key):
    if key == 'r':
        setActiveScreen('menuScreen')

###############################################################################
# Play Screen
###############################################################################

def playScreen_onScreenActivate(app):
    app.direction = []
    app.move = []
    app.tilt = []
    app.xBounds = 40
    app.buildingDistance = 35
    app.stepsPerSecond = 25
    app.fpsCounter = 0
    app.fps = 0
    app.startTime = time.time()
    app.engine = Graphics(app.width, app.height)
    app.player = 0 # Index for the ship array
    app.endOfBuildings = 0
    app.thirdPerson = True
    app.startCameraBarrelRoll = False
    addShapes(app)
    app.showCameraStatus = False

def addShapes(app):
    # We must have a ship
    app.engine.addShip(shipModel(0.5), 'Adam', 2, 4, 30)
    # We must have a ground
    floor = [(-(app.xBounds + 25), 0, 500),
             (-(app.xBounds + 25), 0, -500),
             ((app.xBounds + 25), 0, -500),
             ((app.xBounds + 25), 0, 500)]
    ground = [(floor, 'green')]
    app.engine.addGround(ground)
    # Create a sequences of random heights of buildings
    for i in range(0, 20):
        height = random.randrange(20, 50)
        building1 = createBuilding(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createBuilding(10, 10, height2)
        # Center of buildings are 20 units from middle
        app.engine.addShape(building1, [app.xBounds + 5, height / 2, app.buildingDistance * i])
        app.engine.addShape(building2, [-(app.xBounds + 5), height2 / 2, app.buildingDistance * i])
        app.endOfBuildings += 1

def playScreen_redrawAll(app):
    # First we must draw the sky
    drawRect(0, 0, app.width, app.height, fill='lightblue')

    shapes, shapeIndexes, ground, groundIndexes = app.engine.render(app.thirdPerson)
    # Then we must draw the ground
    allPoints = ground[groundIndexes[0]][0]
    colors = ground[groundIndexes[0]][1]
    indexes = ground[groundIndexes[0]][2]
    for index in indexes:
        # Based on the y position of the rendered ground we can create a new ground
        # that looks better because it is drawn in all directions
        y1 = allPoints[index][3]
        x1 = allPoints[index][2]
        y2 = allPoints[index][5]
        x2 = allPoints[index][4]
        if (x2 - x1) != 0:
            m = (y2 - y1) / (x2 - x1)
        else:
            m = (y2 - y1) / 0.0001
        b = y1 - (m * x1)
        y1 = b
        y2 = m * app.width + b
        drawPolygon(0, y1, app.width, y2, app.width, app.height, 0, app.height, fill=colors[index], border='black')
    # Loops through a sorted list of the z-indexes
    for i in shapeIndexes:
        allPoints = shapes[i][0]
        colors = shapes[i][1]
        indexes = shapes[i][2]
        for index in indexes:
            drawPolygon(*allPoints[index], fill=colors[index], border='black')

    # Draw player health
    drawRect(20, app.height - 75, 75, 25, fill='white', border='black')
    width = 71 * (app.engine.ships[app.player].health / 30)
    if width <= 0: # We don't want a negative health bar
        width = 1
    drawRect(22, app.height - 73, width, 21, fill='red')

    # Draw player boost
    drawRect(100, app.height - 75, 75, 25, fill='white', border='black')
    width = 71 * (app.engine.ships[app.player].boostCooldown / 40)
    if width <= 0: # We don't want a negative boost bar
        width = 1
    drawRect(102, app.height - 73, width, 21, fill='blue')

    if app.showCameraStatus:
        drawCameraStatus(app)
    drawLabel(f'FPS: {app.fps}', 30, 30)

def drawCameraStatus(app):
    drawLabel(f'({app.engine.cameraPosition[0]:0.1f},\
{app.engine.cameraPosition[1]:0.1f},\
{app.engine.cameraPosition[2]:0.1f})', 50, 50)
    drawLabel(f'({app.engine.cameraOrientation[0]:0.1f},\
{app.engine.cameraOrientation[1]:0.1f},\
{app.engine.cameraOrientation[2]:0.1f})', 50, 70)
    drawLabel(f'({app.engine.fov:0.1f})', 50, 90)
    drawLabel(f'({app.engine.ships[app.player].position[0]:0.1f},\
{app.engine.ships[app.player].position[1]:0.1f},\
{app.engine.ships[app.player].position[2]:0.1f})', 50, 110)

def playScreen_onKeyPress(app, key):
    if key == 'w' and app.thirdPerson:
        app.move.append('w')
        app.tilt.append('w')
    elif key == 's' and app.thirdPerson:
        app.move.append('s')
        app.tilt.append('s')
    elif key == 'd' and app.thirdPerson:
        app.move.append('d')
        app.tilt.append('d')
    elif key == 'a' and app.thirdPerson:
        app.move.append('a')
        app.tilt.append('a')
    elif key == 'space':
        laser = projectileModel(0.25)
        # Make sure the laser is not inside in the ship
        app.engine.addProjectile(laser, 8, 10, 2, app.engine.ships[app.player].position)
    elif key == 'm':
        setActiveScreen('menuScreen')
    elif key == 'f':
        app.engine.ships[app.player].startBoost()
    elif key == 'h':
        app.thirdPerson = not app.thirdPerson
        if app.thirdPerson:
            app.engine.cameraOrientation = (-15, 0, 0.5)
            app.engine.moveCameraPosition(0, 4, -12)
        else:
            app.move = []
            app.tilt = []
            app.engine.cameraPosition = app.engine.ships[app.player].position
    elif key == 'z':
        app.showCameraStatus = not app.showCameraStatus

def playScreen_onKeyRelease(app, key):
    if not app.thirdPerson: return
    if key == 'w' and 'w' in app.move and 'w' in app.tilt:
        app.move.remove('w')
        app.tilt.remove('w')
    elif key == 's' and 's' in app.move and 's' in app.tilt:
        app.move.remove('s')
        app.tilt.remove('s')
    elif key == 'd' and 'd' in app.move and 'd' in app.tilt:
        app.move.remove('d')
        app.tilt.remove('d')
    elif key == 'a' and 'a' in app.move and 'a' in app.tilt:
        app.move.remove('a')
        app.tilt.remove('a')

def playScreen_onMouseMove(app, mouseX, mouseY):
    if app.thirdPerson: return
    # Controlling camera orientation based on mouse position
    y = ((mouseX / app.width)) * 180 - 90
    r = app.engine.cameraOrientation[1]
    x = (1 - (mouseY / app.height)) * 180 - 90

    if x > 5: 
        if 'w' not in app.move: app.move.append('w')
    elif x < -5:
        if 's' not in app.move: app.move.append('s')
    else:
        if 'w' in app.move:
            app.move.remove('w')
        if 's' in app.move:
            app.move.remove('s')

    if y > 5: 
        if 'd' not in app.move: app.move.append('d')
        r -= 2 if r > -25 else 0
    elif y < -5:
        if 'a' not in app.move: app.move.append('a')
        r += 2 if r < 25 else 0
    else:
        if 'd' in app.move:
            app.move.remove('d')
        if 'a' in app.move:
            app.move.remove('a')
        if r > 0:
            r -= 2
        elif r < 0:
            r += 2

    app.engine.cameraOrientation = (x, r, y)

def playScreen_onMousePress(app, mx, my):
    if app.thirdPerson:
        app.engine.ships[app.player].startBarrelRoll()
    else: # Perform a barrel roll with the camera
        app.startCameraBarrelRoll = True

def playScreen_onStep(app):
    
    app.engine.moveCameraPosition(0, 0, app.engine.ships[app.player].speed)
    # There is only one ground so we can index at 0
    app.engine.ground[0].updateGround(app.engine.ships[app.player].speed)

    if app.startCameraBarrelRoll:
        app.engine.moveCameraOrientation(0, 36, 0)
        if app.engine.cameraOrientation[1] >= 360:
            p, r, y = app.engine.cameraOrientation
            app.engine.cameraOrientation = (p, 0, y)
            app.startCameraBarrelRoll = False

    rate = 1
    for move in app.move:
        if move == 'w': app.engine.moveCameraPosition(0, rate, 0)
        elif move == 's': app.engine.moveCameraPosition(0, -rate, 0)
        elif move == 'd': app.engine.moveCameraPosition(-rate, 0, 0)
        elif move == 'a': app.engine.moveCameraPosition(rate, 0, 0)

    # We check tilt seperately than move in order to account for max tilts
    rate = app.engine.ships[app.player].jerk
    for tilt in app.tilt:
        if tilt == 'w' and app.engine.ships[app.player].orientation[0] > -20: 
            app.engine.ships[app.player].tiltShip(-rate, 0, 0)
        elif tilt == 's' and app.engine.ships[app.player].orientation[0] < 20: 
            app.engine.ships[app.player].tiltShip(rate, 0, 0)
        elif tilt == 'd' and app.engine.ships[app.player].orientation[2] > -20: 
            app.engine.ships[app.player].tiltShip(0, 0, -rate)
        elif tilt == 'a' and app.engine.ships[app.player].orientation[2] < 20: 
            app.engine.ships[app.player].tiltShip(0, 0, rate)

    if 'w' not in app.tilt and app.engine.ships[app.player].orientation[0] < 0:
        app.engine.ships[app.player].tiltShip(rate, 0, 0)
    elif 's' not in app.tilt and app.engine.ships[app.player].orientation[0] > 0:
        app.engine.ships[app.player].tiltShip(-rate, 0, 0)
    if 'd' not in app.tilt and app.engine.ships[app.player].orientation[2] < 0:
        app.engine.ships[app.player].tiltShip(0, 0, rate)
    elif 'a' not in app.tilt and app.engine.ships[app.player].orientation[2] > 0:
        app.engine.ships[app.player].tiltShip(0, 0, -rate)

    # Check the FPS counter
    app.fpsCounter += 1
    if (time.time() - app.startTime) >= 1:
        app.fps = app.fpsCounter
        app.fpsCounter = 0
        app.startTime = time.time()

    # Most of what is below is updating shape data 
    if app.thirdPerson:
        app.engine.resetShipToCamera()
    else:
        app.engine.ships[app.player].position = app.engine.cameraPosition
        app.engine.ships[app.player].moveShip(0, 0, 5) # Move the ship so obstacle detection still works

    removed = app.engine.removeShapes()
    if removed: # If we removed shapes we then need to create a new building
        height = random.randrange(20, 50)
        building1 = createBuilding(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createBuilding(10, 10, height2)
        app.engine.addShape(building1, (app.xBounds + 5, height / 2, app.buildingDistance * app.endOfBuildings))
        app.engine.addShape(building2, (-(app.xBounds + 5), height2 / 2, app.buildingDistance * app.endOfBuildings))
        app.endOfBuildings += 1

    for projectile in app.engine.projectiles:
        projectile.move()

    for enemy in app.engine.enemies:
        if enemy.shoot():
            laser = projectileModel(0.75)
            pos = (enemy.position[0], enemy.position[1], enemy.position[2] - 5)
            app.engine.addProjectile(laser, -6, 5, 2, pos)
        for projectile in app.engine.projectiles:
            if shapeCollision(enemy, projectile):
                enemy.health -= projectile.power
                app.engine.projectilesToRemove.add(projectile)
                enemy.hit += 1
        if enemy.hit >= 5:
            enemy.hit = 0
        enemy.moveToStandPosition()

    for projectile in app.engine.projectiles:
        if shapeCollision(app.engine.ships[app.player], projectile):
            app.engine.ships[app.player].health -= projectile.power
            app.engine.projectilesToRemove.add(projectile)
            app.engine.ships[app.player].hit += 1

    for obstacle in app.engine.obstacles:
        if obstacleCollision(app.engine.ships[app.player], obstacle):
            app.engine.ships[app.player].health -= obstacle.power
            app.engine.ships[app.player].hit += 1

    for powerup in app.engine.powerups:
        if powerupCollision(app.engine.ships[app.player], powerup):
            app.engine.ships[app.player].health += powerup.healthValue
            if app.engine.ships[app.player].health >= 30: # 30 is the max health
                app.engine.ships[app.player].health = 30
            app.engine.ships[app.player].heal += 1
            app.engine.powerupsToRemove.add(powerup)
        powerup.rotateOrbs()

    app.engine.removeProjectile()
    app.engine.removeEnemies()
    app.engine.removePowerUps()

    if app.engine.ships[app.player].hit >= 3:
        app.engine.ships[app.player].hit = 0
    if app.engine.ships[app.player].heal >= 3:
        app.engine.ships[app.player].heal = 0

    checkPlayerBounds(app)
    app.engine.ships[app.player].performBarrelRoll()
    app.engine.ships[app.player].performBoost()

    # Randomly create an enemy
    if random.randrange(0, 40) < 1:
        enemy = shipModel(2, True)
        x = random.randrange(-15, 15)
        y = random.randrange(10, 25)
        shipZ = app.engine.ships[app.player].position[2]
        shipY = app.engine.ships[app.player].position[1]
        app.engine.addEnemy(enemy, (0, shipY + 30, shipZ + 5), (x, y, shipZ + 150), 20, 5)

    # Randomly create an obstacle
    if random.randrange(0, 40) < 1:
        obstacle = createObstacle(5, 5, 40)
        x = random.randrange(-20, 20)
        app.engine.addObstacle(obstacle, (x, 20, app.buildingDistance * app.endOfBuildings), 5)

    # Randomly create a powerup
    if random.randrange(0, 40) < 1:
        orb = createRectangularPrism(1, 1, 1)
        x = random.randrange(-20, 20)
        y = random.randrange(5, 60)
        shipZ = app.engine.ships[app.player].position[2]
        app.engine.addPowerUp(orb, (x, y, shipZ + 100), 10)

    if app.engine.ships[app.player].health <= 0:
        setActiveScreen('losingScreen')

def distance(p1, p2):
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5

# shape2 must be a projectile
def shapeCollision(shape1, shape2):
    if ((type(shape1) == Ship and shape2.speed > 0) or 
        type(shape1) == Enemy and shape2.speed < 0):
        return False
    isProjectileInfront = shape2.midpoint[2] + shape2.speed >= shape1.midpoint[2]
    if shape2.speed < 0:
        isProjectileInfront = shape2.midpoint[2] + shape2.speed <= shape1.midpoint[2]
    if (shape1.midpoint[0] - shape1.radius < shape2.midpoint[0] < shape1.midpoint[0] + shape1.radius and 
        shape1.midpoint[1] - shape1.radius < shape2.midpoint[1] < shape1.midpoint[1] + shape1.radius and 
        isProjectileInfront):
        return True

# shape2 must be a obstacle
def obstacleCollision(shape1, shape2):
    if (shape2.midpoint[0] - shape2.radius < shape1.midpoint[0] < shape2.midpoint[0] + shape2.radius and
        shape1.midpoint[2] >= shape2.midpoint[2] - shape2.radius and
        shape1.midpoint[1] < shape2.height):
        return True
    
# shape2 must be a powerup
def powerupCollision(shape1, shape2):
    if (shape2.midpoint[0] - shape2.radius < shape1.midpoint[0] < shape2.midpoint[0] + shape2.radius and
        shape2.midpoint[1] - shape2.radius < shape1.midpoint[1] < shape2.midpoint[1] + shape2.radius and
        shape2.midpoint[2] < shape1.midpoint[2]):
        return True

def checkPlayerBounds(app):
    player = app.engine.ships[app.player]
    if (player.position[0] > app.xBounds or player.position[0] < -app.xBounds or player.position[1] < 0 or player.position[1] > 80):
        setActiveScreen('losingScreen')

def main():
    runAppWithScreens(initialScreen='menuScreen', height=768, width=1024)

main()