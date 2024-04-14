"""
This was a test in order to try and create a 3D-graphics engine using a different
way of structuring the perspective matrix using the specific coordinates of the 
frustum. Basically the same as the actual version, but for now it is deprecated.
4/12/24
"""

from cmu_graphics import *
from Object import Shape
import numpy as np
import math

# There might not be a neccesity for having a class here
class Engine:
    def __init__(self, width, height):
        self.cameraPosition = [0, 0, 0]
        self.cameraAngle = [0, 0, 0]
        self.shapes = []
        self.width = width
        self.height = height

        # Here we define our frustum values
        self.fov = math.pi / 2
        self.aspectRatio = self.width / self.height
        self.znear = 1
        self.zfar = self.znear + 3

    def moveCamera(self, x, y, z):
        self.cameraPosition[0] += x
        self.cameraPosition[1] += y
        self.cameraPosition[2] += z

    def addShapes(self, shape):
        self.shapes.append(shape)

    # Takes in a 3D point to render as a tuple
    def renderPoint(self, point):
        # Moves the position to render the point based on where the camera 
        # is currently. The extra 2 is to make sure the vector has
        # a w-value of 1.
        camera = np.transpose(np.array([self.cameraPosition[0], 
                                       self.cameraPosition[1], 
                                       self.cameraPosition[2], 
                                       2]))
        point = np.transpose(np.array([point[0], point[1], point[2], 1]))
        vector = camera - point

        top = math.tan(self.fov / 2) * self.znear
        bottom = -top

        right = self.aspectRatio * top
        left = -right
        print(right)
        perspectiveMatrix = np.array([[(2 * self.znear) / (right - left), 0, (right + left) / (right - left), 0],
                                      [0, (2 * self.znear) / (top - bottom), (top + bottom) / (top - bottom), 0],
                                      [0, 0, -(self.zfar - self.znear) / (self.zfar - self.znear), -(2 * self.zfar * self.znear) / (self.zfar - self.znear)],
                                      [0, 0, -1, 0]])
        imageSpace = np.dot(perspectiveMatrix, vector)
        w = imageSpace[3]
        screenSpace = [0, 0, 0]
        if w != 0:
            screenSpace = imageSpace / w

        # Returns the z value in order to figure out what order to place the z coordinate
        return (screenSpace[0], screenSpace[1], screenSpace[2]) 

    def renderShape(self, shape):
        points = []
        for point in shape.points:
            screenPoints = self.renderPoint(point)
            # Here we convert the coordinates to screen coords
            x = (screenPoints[0] * (self.width / 2)) + (self.width / 2)
            y = (screenPoints[1] * (self.height / 2)) + (self.height / 2)
            #if (x >= 0 and x <= self.width and y >= 0 and y <= self.height): 
            points.append(int(x))
            points.append(int(y))
            #else:
            #    print('Could not renderPoint: ', x, y)
        return points
    
    # Takes all the shapes in self.shapes and returns the render coordinates for them
    def render(self):
        shapePoints = []
        for shape in self.shapes:
            shapePoints.append(self.renderShape(shape))
        return shapePoints
    
def onAppStart(app):
    app.width = 400
    app.height = 300
    app.engine = Engine(app.width, app.height)
    app.shape0 = Shape([(-1, 1, 2),
                        (1, 1, 2),
                        (1, -1, 2),
                        (-1, -1, 2)])
    app.floor = Shape([(-20, -1, 20),
                       (20, -1, 20),
                       (20, -1, -20),
                       (-20, -1, -20)])
    app.engine.addShapes(app.shape0)
    app.engine.addShapes(app.floor)

def redrawAll(app):
    points = app.engine.render()
    for point in points:
        drawPolygon(*point, fill='red', border='black')

    # Here we draw the camera statistics
    drawLabel(f"{(app.engine.cameraPosition[0], app.engine.cameraPosition[1], app.engine.cameraPosition[2])}", 20, 20)
    drawLabel(f"{(app.engine.cameraAngle[0], app.engine.cameraAngle[1], app.engine.cameraAngle[2])}", 20, 40)

def onKeyPress(app, key):
    if key == 'w':
        app.engine.moveCamera(0, 0, 1)
    elif key == 's':
        app.engine.moveCamera(0, 0, -1)
    elif key == 'a':
        app.engine.moveCamera(1, 0, 0)
    elif key == 'd':
        app.engine.moveCamera(-1, 0, 0)

def main():
    runApp(width=400, height=300)
main()
