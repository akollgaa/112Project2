from cmu_graphics import *
from Graphics import Graphics
from Model import *
import time
import random

def onAppStart(app):
    app.width = 1024
    app.height = 768

###############################################################################
# Menu Screen
###############################################################################

def menuScreen_onScreenActivate(app):
    app.mx = 0
    app.my = 0
    app.hovering = False

def menuScreen_redrawAll(app):
    # Draw the mouse positions for debugging/testing
    drawLabel(f'({app.mx}, {app.my})', 30, 30)

    drawLabel('StarFox', app.width / 2, app.height / 4, size=80, bold=True)
    color = 'lightgreen' if app.hovering else 'white'
    drawRect(app.width / 3, app.height * 3/4, app.width / 3, 100, fill=color, border='lightgreen')
    textColor = 'white' if app.hovering else 'lightgreen'
    drawLabel('Play', app.width / 2, app.height * 3/4 + 50, size=20, fill=textColor)

def menuScreen_onMouseMove(app, mouseX, mouseY):
    app.mx = mouseX
    app.my = mouseY
    app.hovering = (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100)

def menuScreen_onMousePress(app, mouseX, mouseY):
    if (app.width / 3 < mouseX < app.width * 2/3 and 
        app.height * 3/4 < mouseY < app.height * 3/4 + 100):
        setActiveScreen('playScreen')

###############################################################################
# Losing Screen
###############################################################################

def losingScreen_onScreenActivate(app):
    pass

def losingScreen_redrawAll(app):
    drawLabel('You lost! Out of Bounds', app.width / 2, app.height / 2, size=50)
    drawLabel("Press r to restart", app.width / 2, app.height / 2 + 40, size=40)

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
    app.xBounds = 15
    app.stepsPerSecond = 25
    app.fpsCounter = 0
    app.fps = 0
    app.startTime = time.time()
    app.engine = Graphics(app.width, app.height)
    app.player = 0 # Index for the ship array
    app.endOfBuidlings = 0
    addShapes(app)

def addShapes(app):
    front = [(-1, 1, 0),
            (1, 1, 0),
            (1, -1, 0),
            (-1, -1, 0)]
    back = [(-1, 1, 2),
            (1, 1, 2),
            (1, -1, 2),
            (-1, -1, 2)]
    left = [(-1, 1, 0),
            (-1, 1, 2),
            (-1, -1, 2),
            (-1, -1, 0)]
    right = [(1, 1, 0),
            (1, 1, 2),
            (1, -1, 2),
            (1, -1, 0)]
    top = [(-1, 1, 0),
            (-1, 1, 2),
            (1, 1, 2),
            (1, 1, 0)]
    bottom = [(-1, -1, 0),
            (-1, -1, 2),
            (1, -1, 2),
            (1, -1, 0)]
    floor = [(-1000, 0, 1000),
             (1000, 0, 1000),
             (1000, 0, -1000),
             (-1000, 0, -1000)]
    cube = [(front, 'red'),
             (back, 'yellow'),
             (left, 'green'),
             (right, 'blue'),
             (bottom, 'purple'),
             (top, 'orange')]
    floor = [(floor, 'green')]
    # We must have a ship
    app.engine.addShip(createRectangularPrism(1, 2, 1), 'Adam', 2, 4)
    # Create a sequences of random heights of buildings
    for i in range(0, 20):
        height = random.randrange(20, 50)
        building1 = createRectangularPrism(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createRectangularPrism(10, 10, height2)
        # Center of buildings are 20 units from middle
        app.engine.addShape(building1, [app.xBounds + 5, height / 2, 15 * i])
        app.engine.addShape(building2, [-(app.xBounds + 5), height2 / 2, 15 * i])
        app.endOfBuidlings += 1

def playScreen_redrawAll(app):
    shapes, shapeIndexes = app.engine.render()
    for i in shapeIndexes: # Loops through a sorted list of the z-indexes
        allPoints = shapes[i][0]
        colors = shapes[i][1]
        indexes = shapes[i][2]
        for index in indexes:
            drawPolygon(*allPoints[index], fill=colors[index], border='black')
    drawCameraStatus(app)

def drawCameraStatus(app):
    drawLabel(f'({app.engine.cameraPosition[0]:0.1f},\
{app.engine.cameraPosition[1]:0.1f},\
{app.engine.cameraPosition[2]:0.1f})', 50, 20)
    drawLabel(f'({app.engine.cameraOrientation[0]:0.1f},\
{app.engine.cameraOrientation[1]:0.1f},\
{app.engine.cameraOrientation[2]:0.1f})', 50, 50)
    drawLabel(f'({app.engine.fov:0.1f})', 50, 80)
    drawLabel(f'FPS: {app.fps}', 50, 110)
    drawLabel(f'({app.engine.ships[app.player].position[0]:0.1f},\
{app.engine.ships[app.player].position[1]:0.1f},\
{app.engine.ships[app.player].position[2]:0.1f})', 50, 140)

def playScreen_onKeyPress(app, key):
    if key == 'w':
        app.move.append('w')
        app.tilt.append('w')
    elif key == 's':
        app.move.append('s')
        app.tilt.append('s')
    elif key == 'd':
        app.move.append('d')
        app.tilt.append('d')
    elif key == 'a':
        app.move.append('a')
        app.tilt.append('a')
    elif key == 'space':
        laser = createRectangularPrism(0.5, 2, 0.5)
        app.engine.addProjectile(laser, 8, 10, 2, app.engine.ships[app.player].position)
    elif key == 'm':
        setActiveScreen('menuScreen')

def playScreen_onKeyRelease(app, key):
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
    # Controlling camera orientation based on mouse position
    y = ((mouseX / app.width)) * 180 - 90
    r = app.engine.cameraOrientation[1]
    x = (1 - (mouseY / app.height)) * 180 - 90
    app.engine.cameraOrientation = [x, r, y]

def playScreen_onStep(app):

    #app.engine.ships[app.player].moveShip(0, 0, app.engine.ships[app.player].speed)
    app.engine.moveCameraPosition(0, 0, app.engine.ships[app.player].speed)
    
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

    app.engine.resetShipToCamera()

    removed = app.engine.removeShapes()
    if removed: # If we removed shapes we then need to create a new building
        height = random.randrange(20, 50)
        building1 = createRectangularPrism(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createRectangularPrism(10, 10, height2)
        app.engine.addShape(building1, [app.xBounds + 5, height / 2, 15 * app.endOfBuidlings])
        app.engine.addShape(building2, [-(app.xBounds + 5), height2 / 2, 15 * app.endOfBuidlings])
        app.endOfBuidlings += 1

    for projectile in app.engine.projectiles:
        projectile.move()

    app.engine.removeProjectile()

    checkPlayerBounds(app)

def checkPlayerBounds(app):
    player = app.engine.ships[app.player]
    if (player.position[0] > app.xBounds or player.position[0] < -app.xBounds or player.position[1] < 0 or player.position[1] > 80):
        setActiveScreen('losingScreen')

def main():
    runAppWithScreens(initialScreen='menuScreen', height=768, width=1024)

main()