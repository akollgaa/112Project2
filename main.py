from cmu_graphics import *
from Graphics import Graphics
from Model import *
import time

def onAppStart(app):
    app.width = 1024
    app.height = 768
    app.direction = []
    app.move = []
    app.stepsPerSecond = 10
    app.fpsCounter = 0
    app.fps = 0
    app.startTime = time.time()
    app.engine = Graphics(app.width, app.height)
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
    floor = [(-5, 0, 5),
             (5, 0, 5),
             (5, 0, -5),
             (-5, 0, -5)]
    cube = [(front, 'red'),
             (back, 'yellow'),
             (left, 'green'),
             (right, 'blue'),
             (bottom, 'purple'),
             (top, 'orange')]
    floor = [(floor, 'green')]
    app.engine.addShip(createRectangularPrism(1, 1, 1), 'Adam', 2, 2)
    app.engine.addShape(createRectangularPrism(1, 1, 1), [0, 0, 0])
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

def redrawAll(app):
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
    drawLabel(f'({app.engine.ships[0].position[0]:0.1f}, {app.engine.ships[0].position[1]:0.1f}, {app.engine.ships[0].position[2]:0.1f})', 50, 140)

def drawMouseBox(app):
    drawLine(app.width / 3, 0, app.width / 3, app.height, lineWidth=3)
    drawLine(app.width * 2/3, 0, app.width * 2/3, app.height, lineWidth=3)
    drawLine(0, app.height / 3, app.width, app.height / 3, lineWidth=3)
    drawLine(0, app.height * 2/3, app.width, app.height * 2/3, lineWidth=3)

def onKeyPress(app, key):
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

def onKeyRelease(app, key):
    if key == 'w' and 'w' in app.move:
        app.move.remove('w')
    elif key == 's' and 's' in app.move:
        app.move.remove('s')
    elif key == 'd' and 'd' in app.move:
        app.move.remove('d')
    elif key == 'a' and 'a' in app.move:
        app.move.remove('a')

def onMouseMove(app, mouseX, mouseY):
    p = app.engine.cameraOrientation[0]
    r = app.engine.cameraOrientation[1]
    y = app.engine.cameraOrientation[2]
    y = ((mouseX / app.width)) * 360 - 180
    app.engine.cameraOrientation = [p, r, y]
    # if mouseX < app.width / 3:
    #     app.direction.append('left')
    # elif 'left' in app.direction:
    #     app.direction.remove('left')

    # if mouseX > app.width * 2/3:
    #     app.direction.append('right')
    # elif 'right' in app.direction:
    #     app.direction.remove('right')

    if mouseY < app.height / 3:
        app.direction.append('up')
    elif 'up' in app.direction:
        app.direction.remove('up')

    if mouseY > app.height * 2/3:
        app.direction.append('down')
    elif 'down' in app.direction:
        app.direction.remove('down')

def onStep(app):
    rate = 0.1
    for direction in app.direction:
        if direction == 'left': app.engine.moveCameraOrientation(0, 0, rate)
        elif direction == 'right': app.engine.moveCameraOrientation(0, 0, -rate)
        elif direction == 'up': app.engine.moveCameraOrientation(rate, 0, 0)
        elif direction == 'down': app.engine.moveCameraOrientation(-rate, 0, 0)
    
    rate = 0.1
    for move in app.move:
        if move == 'w': app.engine.moveCameraPosition(0, 0, 1)
        elif move == 's': app.engine.moveCameraPosition(0, 0, -1)
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

    #app.engine.shapes[0].moveOrientation(1, 1, 1)

def main():
    runApp(height=768, width=1024)

main()