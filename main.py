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
    app.stepsPerSecond = 20
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
    app.engine.addShip(createRectangularPrism(1, 2, 1), 'Adam', 2, 2)

    for i in range(0, 20):
        height = random.randrange(20, 50)
        building1 = createRectangularPrism(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createRectangularPrism(10, 10, height2)
        app.engine.addShape(building1, [20, height / 2, 15 * i])
        app.engine.addShape(building2, [-20, height2 / 2, 15 * i])
        app.endOfBuidlings += 1
    #app.engine.addShape(createRectangularPrism(1, 1, 1), [0, 0, 0])
    #app.engine.addShape(floor)
    #app.engine.addShape(createRectangularPrism(1, 1, 1), [0, 0, 5])
    return
    for i in range(0, 10):
        for j in range(0, 10):
            floor = [(-20, 0, 20),
                    (20, 0, 20),
                    (20, 0, -20),
                    (-20, 0, -20)]
            color = 'black' if (i + j) % 2 == 0 else 'white'
            floor = [(floor, color)]
            app.engine.addShape(floor, [20 * i, 0, 20 * j])
    #app.engine.addShape(cube, [0, 0, 2])
    #app.engine.addShape(floor, [0, -2, 0])

def playScreen_redrawAll(app):
    #allPoints, colors, indexes = app.engine.render()
    shapes, shapeIndexes = app.engine.render()
    for i in shapeIndexes: # Loops through a sorted list of the z-indexes
        allPoints = shapes[i][0]
        colors = shapes[i][1]
        indexes = shapes[i][2]
        for index in indexes:
            drawPolygon(*allPoints[index], fill=colors[index], border='black')
    drawCameraStatus(app)

    drawMouseBox(app)

def drawCameraStatus(app):
    drawLabel(f'({app.engine.cameraPosition[0]:0.1f}, {app.engine.cameraPosition[1]:0.1f}, {app.engine.cameraPosition[2]:0.1f})', 50, 20)
    drawLabel(f'({app.engine.cameraOrientation[0]:0.1f}, {app.engine.cameraOrientation[1]:0.1f}, {app.engine.cameraOrientation[2]:0.1f})', 50, 50)
    drawLabel(f'({app.engine.fov:0.1f})', 50, 80)
    drawLabel(f'FPS: {app.fps}', 50, 110)
    drawLabel(f'({app.engine.ships[app.player].position[0]:0.1f}, {app.engine.ships[app.player].position[1]:0.1f}, {app.engine.ships[app.player].position[2]:0.1f})', 50, 140)

def drawMouseBox(app):
    drawLine(app.width / 3, 0, app.width / 3, app.height, lineWidth=3)
    drawLine(app.width * 2/3, 0, app.width * 2/3, app.height, lineWidth=3)
    drawLine(0, app.height / 3, app.width, app.height / 3, lineWidth=3)
    drawLine(0, app.height * 2/3, app.width, app.height * 2/3, lineWidth=3)

def playScreen_onKeyPress(app, key):
    if key == 'r':
        app.engine.resetCamera()

    if key == 'w':
        #app.engine.moveCameraPosition(0, 0, 1)
        app.move.append('w')
    elif key == 's':
        app.move.append('s')
        #app.engine.moveCameraPosition(0, 0, -1)
    elif key == 'd':
        app.move.append('d')
        #app.engine.moveCameraPosition(1, 0, 0)
    elif key == 'a':
        app.move.append('a')
        #app.engine.moveCameraPosition(-1, 0, 0)
    elif key == 'up':
        app.engine.moveCameraPosition(0, 1, 0)
    elif key == 'down':
        app.engine.moveCameraPosition(0, -1, 0)
    elif key == 'left':
        app.engine.moveCameraOrientation(0, 0, 5) # 5 degrees at a time
    elif key == 'right':
        app.engine.moveCameraOrientation(0, 0, -5) # 5 degrees at a time
    elif key == 'z':
        app.engine.moveCameraOrientation(-5, 0, 0)
    elif key == 'x':
        app.engine.moveCameraOrientation(5, 0, 0)
    elif key == 't':
        app.engine.moveFOV(0.1)
    elif key == 'y':
        app.engine.moveFOV(-0.1)
    elif key == 'space':
        laser = createRectangularPrism(0.5, 2, 0.5)
        app.engine.addProjectile(laser, 8, 10, 2, app.engine.ships[app.player].position)
    elif key == 'm':
        setActiveScreen('menuScreen')

def playScreen_onKeyRelease(app, key):
    if key == 'w' and 'w' in app.move:
        app.move.remove('w')
    elif key == 's' and 's' in app.move:
        app.move.remove('s')
    elif key == 'd' and 'd' in app.move:
        app.move.remove('d')
    elif key == 'a' and 'a' in app.move:
        app.move.remove('a')

def playScreen_onMouseMove(app, mouseX, mouseY):
    y = ((mouseX / app.width)) * 180 - 90
    r = app.engine.cameraOrientation[1]
    x = (1 - (mouseY / app.height)) * 180 - 90
    app.engine.cameraOrientation = [x, r, y]

    # Below is an different way of controlling the camera orientation

    # if mouseX < app.width / 3:
    #     app.direction.append('left')
    # elif 'left' in app.direction:
    #     app.direction.remove('left')

    # if mouseX > app.width * 2/3:
    #     app.direction.append('right')
    # elif 'right' in app.direction:
    #     app.direction.remove('right')

    # if mouseY < app.height / 3:
    #     app.direction.append('up')
    # elif 'up' in app.direction:
    #     app.direction.remove('up')

    # if mouseY > app.height * 2/3:
    #     app.direction.append('down')
    # elif 'down' in app.direction:
    #     app.direction.remove('down')

def playScreen_onStep(app):

    #app.engine.ships[app.player].moveShip(0, 0, app.engine.ships[app.player].speed)
    app.engine.moveCameraPosition(0, 0, app.engine.ships[app.player].speed)
    # This is basically not used; however I'm keeping it for debugging purposes
    rate = 0.1
    for direction in app.direction:
        if direction == 'left': app.engine.moveCameraOrientation(0, 0, rate)
        elif direction == 'right': app.engine.moveCameraOrientation(0, 0, -rate)
        elif direction == 'up': app.engine.moveCameraOrientation(rate, 0, 0)
        elif direction == 'down': app.engine.moveCameraOrientation(-rate, 0, 0)
    
    rate = 0.1
    for move in app.move:
        if move == 'w': app.engine.moveCameraPosition(0, 1, 0)
        elif move == 's': app.engine.moveCameraPosition(0, -1, 0)
        elif move == 'd': app.engine.moveCameraPosition(-1, 0, 0)
        elif move == 'a': app.engine.moveCameraPosition(1, 0, 0)

    app.fpsCounter += 1
    if (time.time() - app.startTime) >= 1:
        app.fps = app.fpsCounter
        app.fpsCounter = 0
        app.startTime = time.time()

    # for shape in app.engine.shapes:
    #     if isinstance(shape, Ship):
    #         shape.moveShip(0, 0, shape.speed / 10)
    #         #print(shape.position)

    #app.engine.resetCameraToShip()
    app.engine.resetShipToCamera()

    removed = app.engine.removeShapes()
    if removed: # If we removed shapes we then need to create a new building
        height = random.randrange(20, 50)
        building1 = createRectangularPrism(10, 10, height)
        height2 = random.randrange(20, 50)
        building2 = createRectangularPrism(10, 10, height2)
        app.endOfBuidlings += 1
        app.engine.addShape(building1, [20, height / 2, 15 * app.endOfBuidlings])
        app.engine.addShape(building2, [-20, height2 / 2, 15 * app.endOfBuidlings])

    for projectile in app.engine.projectiles:
        projectile.move()

    app.engine.removeProjectile()

    checkPlayerBounds(app)

    #app.engine.shapes[0].moveOrientation(1, 1, 1)

def checkPlayerBounds(app):
    player = app.engine.ships[app.player]
    if (player.position[0] > 15 or player.position[0] < -15 or player.position[1] < 0 or player.position[1] > 80):
        setActiveScreen('losingScreen')

def main():
    runAppWithScreens(initialScreen='menuScreen', height=768, width=1024)

main()