from Object import Shape
import numpy as np
import math

class Graphics:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cameraPosition = [0, 0, 0] # x, y, z
        self.cameraOrientation = [0, 0, 0] # pitch, roll, yaw
        self.fov = math.pi / 2
        self.shapes = []

    def addShape(self, pointList, color):
        self.shapes.append(Shape(pointList, color))

    # Might not be neccesary
    def getObjectIndex(self, object):
        if object in self.objects:
            return self.objects.find(object)
        else:
            return None

    # Moves the camera by some constant direction
    def moveCameraPosition(self, dx, dy, dz):
        #theta = self.cameraOrientation[2] * (math.pi / 180)
        #dx = dx * math.cos(theta) + dz * math.sin(theta)
        #dz = -dx * math.sin(theta) + dz * math.cos(theta)
        self.cameraPosition[0] += dx
        self.cameraPosition[1] += dy
        self.cameraPosition[2] += dz

    # Moves the camera orientation by some constant direction
    def moveCameraOrientation(self, dp, dr, dy):
        self.cameraOrientation[0] += dp
        self.cameraOrientation[1] += dr
        self.cameraOrientation[2] += dy

    # Takes angles in radians
    def moveFOV(self, angle):
        self.fov += angle

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
        f = 1 / math.tan(self.fov / 2)
        # normalization constant
        # Assuming camera is at origin looking down z axis
        znear = self.cameraPosition[2] + 1
        zfar = self.cameraPosition[2] + 6
        znear = 1
        zfar = 6
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
        rotationMatrix = np.dot(rotationXMatrix, rotationYMatrix)
        imageSpace = np.dot(np.dot(rotationMatrix, perspectiveMatrix), vector)
        w = imageSpace[3]
        finalCoordinate = [0, 0, 0]
        if w != 0:
            finalCoordinate[0] = imageSpace[0] / w
            finalCoordinate[1] = imageSpace[1] / w
            finalCoordinate[2] = imageSpace[2]
        return (finalCoordinate[0], finalCoordinate[1], finalCoordinate[2])

    # Returns a list of points for that shape
    # as well as a zIndex from -1 to 1 for how close the shape is to the camera
    def renderShape(self, shape):
        result = []
        zAverage = 0
        for point in shape.points:
            newPoint = self.renderPoint(point)
            newPoint = self.convertImageSpaceToScreen(newPoint)
            result.append(newPoint[0])
            result.append(newPoint[1])
            zAverage += newPoint[2]
            #if shape.color == 'green':
                #print(newPoint[2])
        # Divide by the # of points, but result contains each x,y so divide by 2.
        zAverage = zAverage / (len(result) / 2) 
        return (result, zAverage)
    
    def convertImageSpaceToScreen(self, point):
        screenX = int(point[0] * self.width) + self.width / 2
        screenY = int(point[1] * self.height) + self.height / 2
        return (screenX, screenY, point[2])

    # This is O(nlogn) cause of the sorting at the end :(
    def render(self):
        allPoints = dict()
        colors = dict()
        indexes = []
        for shape in self.shapes:
            points, zIndex = self.renderShape(shape)
            allPoints[zIndex] = points
            colors[zIndex] = shape.color
            indexes.append(zIndex)
        return allPoints, colors, sorted(indexes)