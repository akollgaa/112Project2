from cmu_graphics import *
import Object as obj
import numpy as np
import math

class Graphics:
    
    cameraPosition = [0, 0, 0] # x, y, z
    cameraOrientation = [0, 0, 0] # pitch, roll, yaw
    displaySurface = [0, 0, 0]# x, y, z
    
    def __init__(self):
        self.objects = []

    def addObject(self, object):
        self.objects.append(object)
    
    def getObjectIndex(self, object):
        if object in self.objects:
            return self.objects.find(object)
        else:
            return None
    
    # Moves the camera by some constant direction
    def moveCameraPosition(self, dx, dy, dz):
        theta = Graphics.cameraOrientation[2] * (math.pi / 180)
        dx = dx * math.cos(theta) + dz * math.sin(theta)
        dz = -dx * math.sin(theta) + dz * math.cos(theta)
        Graphics.cameraPosition[0] += dx
        Graphics.cameraPosition[1] += dy
        Graphics.cameraPosition[2] += dz
        # Must move the display surface as well
        self.moveDisplaySurface(dx, dy, dz)
    
    # Moves the camera orientation by some constant direction
    def moveCameraOrientation(self, dp, dr, dy):
        Graphics.cameraOrientation[0] += dp
        Graphics.cameraOrientation[1] += dr
        Graphics.cameraOrientation[2] += dy

    # Moves the display surface by some constant direction
    def moveDisplaySurface(self, dx, dy, dz):
        Graphics.displaySurface[0] += dx
        Graphics.displaySurface[1] += dy
        Graphics.displaySurface[2] += dz
    

# Here we actually do some rendering

# Stores everything as we would use it in numpy
class Render:
    def __init__(self, cameraPosition, cameraOrientation, displaySurface, width, height):
        self.cameraPosition = np.transpose(np.array(cameraPosition))
        self.cameraOrientation = np.transpose(np.array(cameraOrientation))
        self.displaySurface = np.transpose(np.array(displaySurface))
        self.width = width
        self.height = height

    # Point is a tuple (x, y, z)
    # All of the math is from https://en.m.wikipedia.org/wiki/3D_projection
    # Returns a (x, y) that can be placed on the screen
    def renderPoint(self, point):
        # Creates a 4x1 vector containing the direction of the point with respect to the origin(0,0,0)
        # Subtracting the camera will move the point relative to the position of the camera
        camera = np.append(self.cameraPosition, [[2]])
        vector = camera - np.transpose(np.array([point[0], point[1], point[2], 1]))

        # Aspect Ratio
        a = self.height / self.width
        # Assumes a 90 degree fov
        fov = math.pi / 2
        f = 1 / math.tan(fov / 2)
        # normalization constant
        # Assuming camera is at origin looking down z axis
        znear = self.cameraPosition[2] + 1
        zfar = self.cameraPosition[2] + 3
        l = zfar / (zfar - znear)
        # Converts points based on fov, aspect ratio, and depth
        perspectiveMatrix = np.array([[f * a,  0, 0,          0],
                                      [    0,  f, 0,          0],
                                      [    0,  0, l, -l * znear],
                                      [    0,  0, 1,          0]])
        # Converts points based on camera yaw angle
        theta1 = (self.cameraOrientation[2]) * (math.pi / 180)
        theta2 = (self.cameraOrientation[0]) * (math.pi / 180)
        rotationYMatrix = np.array([[ math.cos(theta1), 0, math.sin(theta1), 0],
                                    [               0, 1,               0, 0],
                                    [-math.sin(theta1), 0, math.cos(theta1), 0],
                                    [               0, 0,               0, 1]])
        
        rotationXMatrix = np.array([[1,               0,                0, 0],
                                    [0, math.cos(theta2), -math.sin(theta2), 0],
                                    [0, math.sin(theta2),  math.cos(theta2), 0],
                                    [0,               0,                0, 1]])
        rotationMatrix = np.dot(rotationYMatrix, rotationXMatrix)
        imageSpace = np.dot(np.dot(rotationMatrix, perspectiveMatrix), vector)
        w = imageSpace[3]
        finalCoordinate = [0, 0, 0]
        if w != 0:
            finalCoordinate[0] = imageSpace[0] / w
            finalCoordinate[1] = imageSpace[1] / w
            finalCoordinate[2] = imageSpace[2] / w
        return (finalCoordinate[0], finalCoordinate[1], finalCoordinate[2])
    
    def convertImageSpaceToScreen(self, point):
        screenX = int(point[0] * self.width) + self.width / 2
        screenY = int(point[1] * self.height) + self.height / 2

        return (screenX, screenY, point[2])

    # Returns a list of points for that object
    # as well as a zIndex from -1 to 1 for how close the object is to the camera
    def renderObject(self, object):
        result = []
        for point in object.points:
            newPoint = self.renderPoint(point)
            if (newPoint[0] > 1 or newPoint[0] < 1 or
                newPoint[1] > 1 or newPoint[1] < 1):
                newPoint = self.convertImageSpaceToScreen(newPoint)
                result.append(newPoint[0])
                result.append(newPoint[1])
        return (result, newPoint[2])
    
    # This is like really slow
    def render(self, objects):
        allPoints = dict()
        indexes = []
        for object in objects:
            points, zIndex = self.renderObject(object)
            allPoints[zIndex] = points
            indexes.append(zIndex)
        return allPoints, sorted(indexes)

def onAppStart(app):
    app.width = 400
    app.height = 300
    blockPosition = [(-1, 1, 2),
                     (1, 1, 2),
                     (1, -1, 2),
                     (-1, -1, 2)]
    block2Position = [(-0.5, 1, 2.5),
                     (1.5, 1, 2.5),
                     (1.5, -1, 2.5),
                     (-0.5, -1, 2.5)]
    app.block = obj.Object(blockPosition)
    app.block2 = obj.Object(block2Position)
    app.graphics = Graphics()
    app.graphics.addObject(app.block)

def redrawAll(app):
    # Possibly change this so you don't recreate an entire render class everytime we redrawall
    render = Render(app.graphics.cameraPosition, app.graphics.cameraOrientation, app.graphics.displaySurface, app.width, app.height)
    objects = [app.block, app.block2]
    allPoints, indexes = render.render(objects)
    for index in indexes:
        drawPolygon(*allPoints[index], fill='red', border='black')
    # otherPoints = render.renderObject(app.block2)
    # drawPolygon(*otherPoints, fill='blue', border='black')
    # points = render.renderObject(app.block)
    # drawPolygon(*points, fill='red', border='black')
    # for i in range(len(points) - 1):
    #     drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], lineWidth = 3)
    drawCameraStatus(app)

def drawCameraStatus(app):
    drawLabel(f'({app.graphics.cameraPosition[0]:0.1f}, {app.graphics.cameraPosition[1]:0.1f}, {app.graphics.cameraPosition[2]:0.1f})', 40, 20)
    drawLabel(f'({app.graphics.cameraOrientation[0]:0.1f}, {app.graphics.cameraOrientation[1]:0.1f}, {app.graphics.cameraOrientation[2]:0.1f})', 40, 50)

def onKeyPress(app, key):
    if key == 'w':
        app.graphics.moveCameraPosition(0, 0, 1)
    elif key == 's':
        app.graphics.moveCameraPosition(0, 0, -1)
    elif key == 'd':
        app.graphics.moveCameraPosition(1, 0, 0)
    elif key == 'a':
        app.graphics.moveCameraPosition(-1, 0, 0)
    elif key == 'up':
        app.graphics.moveCameraPosition(0, 1, 0)
    elif key == 'down':
        app.graphics.moveCameraPosition(0, -1, 0)
    elif key == 'left':
        app.graphics.moveCameraOrientation(0, 0, 5) # 5 degrees at a time
    elif key == 'right':
        app.graphics.moveCameraOrientation(0, 0, -5) # 5 degrees at a time
    elif key == 'z':
        app.graphics.moveCameraOrientation(-5, 0, 0)
    elif key == 'x':
        app.graphics.moveCameraOrientation(5, 0, 0)

def main():
    runApp(height=300, width=400)

main()