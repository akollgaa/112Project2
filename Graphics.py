from Object import Shape
import numpy as np
import math
import copy
from Model import Ship

class Graphics:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cameraPosition = [0, 0, 0] # x, y, z
        self.cameraOrientation = [0, 0, 0] # pitch, roll, yaw
        self.fov = math.pi / 2
        self.shapes = []
        self.ships = []

        # We only need to calculate the perspectiveMatrix once and then reference later
        # Aspect Ratio
        a = self.height / self.width
        f = 1 / math.tan(self.fov / 2)
        # normalization constant
        # Assuming camera is at origin looking down z axis
        znear = 0.1
        zfar =  100
        l = zfar / (zfar - znear)
        # Converts points based on fov, aspect ratio, and depth
        self.perspectiveMatrix = np.array([[f * a,  0, 0,          0],
                                        [    0,  f, 0,          0],
                                        [    0,  0, l, -l * znear],
                                        [    0,  0, 1,          0]])

    def addShip(self, shape, captain, speed, jerk):
        self.ships.append(Ship(shape, captain, speed, jerk))

    def addShape(self, shape, position=[0, 0, 0], orientation=[0, 0, 0]):
        self.shapes.append(Shape(shape, position, orientation))

    def resetCamera(self):
        self.cameraPosition = [0, 0, 0] # x, y, z
        self.cameraOrientation = [0, 0, 0] # pitch, roll, yaw

    def resetCameraToShip(self):
        if len(self.ships) == 0:
            return
        self.cameraPosition = copy.copy(self.ships[0].position)
        self.cameraPosition[2] += 12
        self.cameraPosition[1] += 4

    def resetShipToCamera(self):
        if len(self.ships) == 0:
            return
        self.ships[0].position = copy.copy(self.cameraPosition)
        self.ships[0].moveShip(0, -4, 12)

    # Might not be neccesary
    def getObjectIndex(self, object):
        if object in self.objects:
            return self.objects.find(object)
        else:
            return None

    # Moves the camera by some constant direction
    def moveCameraPosition(self, dx, dy, dz):
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
    def renderPoint(self, point, position, orientation):
        # Creates a 4x1 vector containing the direction of the point with respect to the origin(0,0,0)
        # Subtracting the camera will move the point relative to the position of the camera
        
        #camera = np.append(self.cameraPosition, [[2]])
        vector = np.transpose(np.array([point[0], point[1], point[2], 1]))
        #vector = camera - point

        modelMatrix = self.createModelMatrix(position, orientation)

        cameraTranslationMatrix = np.array([[1, 0, 0, self.cameraPosition[0]],
                                            [0, 1, 0, self.cameraPosition[1]],
                                            [0, 0, 1, self.cameraPosition[2]],
                                            [0, 0, 0, 1]])
        # Converts points based on camera yaw angle
        theta1 = (self.cameraOrientation[2]) * (math.pi / 180)
        theta2 = (self.cameraOrientation[0]) * (math.pi / 180)
        cameraRotationYMatrix = np.array([[ math.cos(theta1), 0, math.sin(theta1), 0],
                                            [               0, 1,               0, 0],
                                            [-math.sin(theta1), 0, math.cos(theta1), 0],
                                            [               0, 0,               0, 1]])
        
        cameraRotationXMatrix = np.array([[1,               0,                0, 0],
                                            [0, math.cos(theta2), -math.sin(theta2), 0],
                                            [0, math.sin(theta2),  math.cos(theta2), 0],
                                            [0,               0,                0, 1]])
        rotationMatrix = np.dot(cameraRotationYMatrix, cameraRotationXMatrix)
        cameraTransformMatrix = np.dot(rotationMatrix, cameraTranslationMatrix)
        
        clipSpace = np.dot(np.dot(np.dot(self.perspectiveMatrix, cameraTransformMatrix), modelMatrix), vector)
        w = abs(clipSpace[3])
        if w == 0:
            w = 1 # This is to avoid a divide by zero error.
        finalCoordinate = [clipSpace[0] / w, clipSpace[1] / w, clipSpace[2]]

        return (finalCoordinate[0], finalCoordinate[1], finalCoordinate[2])

    # Returns a list of points for that shape
    # as well as a zIndex from -1 to 1 for how close the shape is to the camera
    def renderPolygon(self, polygon, position, orientation):
        result = []
        zAverage = 0
        for point in polygon.points:
            newPoint = self.renderPoint(point, position, orientation)
            #print(newPoint)
            newPoint = self.convertImageSpaceToScreen(newPoint)
            result.append(newPoint[0])
            result.append(newPoint[1])
            zAverage += newPoint[2]
            #if shape.color == 'green':
                #print(newPoint[2])
        # Divide by the # of points, but result contains each x,y so divide by 2.
        zAverage = zAverage / (len(result) / 2) 
        return (result, zAverage)
    
    # Moves the points to the proper position relative to the world view
    # Deprecated
    def moveToWorldView(self, point, position):
        modelMatrix = np.array([[1, 0, 0, position[0]],
                                [0, 1, 0, position[1]],
                                [0, 0, 1, position[2]],
                                [0, 0, 0, 1]])
        point = np.transpose(np.array([point[0], point[1], point[2], 1]))
        movedPoint = np.dot(modelMatrix, point)
        return (movedPoint[0], movedPoint[1], movedPoint[2])
    
    def createModelMatrix(self, position, orientation):
        # The positions are negated to align with the axis of the camera.
        translationMatrix = np.array([[1, 0, 0, -position[0]],
                                        [0, 1, 0, -position[1]],
                                        [0, 0, 1, -position[2]],
                                        [0, 0, 0, 1]])
        theta1 = orientation[2] * (math.pi / 180)
        theta2 = orientation[0] * (math.pi / 180)
        theta3 = orientation[1] * (math.pi / 180)
        rotationYMatrix = np.array([[ math.cos(theta1), 0, math.sin(theta1), 0],
                                            [               0, 1,               0, 0],
                                            [-math.sin(theta1), 0, math.cos(theta1), 0],
                                            [               0, 0,               0, 1]])
        
        rotationXMatrix = np.array([[1,               0,                0, 0],
                                            [0, math.cos(theta2), -math.sin(theta2), 0],
                                            [0, math.sin(theta2),  math.cos(theta2), 0],
                                            [0,               0,                0, 1]])
        rotationZMatrix = np.array([[math.cos(theta3),    -math.sin(theta3),  0, 0],
                                            [math.sin(theta3), math.cos(theta3), 0, 0],
                                            [0,             0,                  1, 0],
                                            [0,               0,                0, 1]])
        rotationMatrix = np.dot(np.dot(rotationXMatrix, rotationYMatrix), rotationZMatrix)
        return np.dot(rotationMatrix, translationMatrix)
    
    # Scales values to screen width and height and flips the y
    def convertImageSpaceToScreen(self, point):
        screenX = int(point[0] * self.width) + self.width / 2
        screenY = int(point[1] * self.height) + self.height / 2
        return (screenX, screenY, point[2])
    
    # Takes in two tuples/lists of length 3 (x, y, z)
    def distance(self, p1, p2):
        return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5

    # This is O(nlogn) cause of the sorting at the end :(
    def render(self):
        shapes = dict()
        shapeIndexes = []
        for shape in self.shapes:
            shapeMidPoint = shape.calculateMidpoint(True)
            dist = self.distance(self.cameraPosition, shapeMidPoint)
            allPoints = dict()
            colors = dict()
            indexes = []
            for polygon in shape.polygons:
                points, zIndex = self.renderPolygon(polygon, shape.position, shape.orientation)
                allPoints[zIndex] = points
                colors[zIndex] = polygon.color
                indexes.append(zIndex)
            shapes[dist] = (allPoints, colors, sorted(indexes, reverse=False))
            shapeIndexes.append(dist)
        
        # By breaking this apart, it will run faster than combining shapes and ships.
        for ship in self.ships:
            shapeMidPoint = ship.calculateMidpoint(True)
            dist = self.distance(self.cameraPosition, shapeMidPoint)
            allPoints = dict()
            colors = dict()
            indexes = []
            for polygon in ship.polygons:
                points, zIndex = self.renderPolygon(polygon, ship.position, ship.orientation)
                allPoints[zIndex] = points
                colors[zIndex] = polygon.color
                indexes.append(zIndex)
            shapes[dist] = (allPoints, colors, sorted(indexes, reverse=False))
            shapeIndexes.append(dist)

        return (shapes, sorted(shapeIndexes, reverse=True))