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

    def addShape(self, shape, position):
        self.shapes.append(Shape(shape, position))

    def resetCamera(self):
        self.cameraPosition = [0, 0, 0] # x, y, z
        self.cameraOrientation = [0, 0, 0] # pitch, roll, yaw

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
    def renderPoint(self, point, position):
        # Creates a 4x1 vector containing the direction of the point with respect to the origin(0,0,0)
        # Subtracting the camera will move the point relative to the position of the camera
        
        #camera = np.append(self.cameraPosition, [[2]])
        vector = np.transpose(np.array([point[0], point[1], point[2], 1]))
        #vector = camera - point

        modelMatrix = np.array([[1, 0, 0, position[0]],
                                [0, 1, 0, position[1]],
                                [0, 0, 1, position[2]],
                                [0, 0, 0, 1]])

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
        #print(cameraTransformMatrix)

        # Aspect Ratio
        a = self.height / self.width
        f = 1 / math.tan(self.fov / 2)
        # normalization constant
        # Assuming camera is at origin looking down z axis
        znear = 0.1
        zfar =  100
        l = zfar / (zfar - znear)
        # Converts points based on fov, aspect ratio, and depth
        perspectiveMatrix = np.array([[f * a,  0, 0,          0],
                                        [    0,  f, 0,          0],
                                        [    0,  0, l, -l * znear],
                                        [    0,  0, 1,          0]])
        clipSpace = np.dot(np.dot(np.dot(perspectiveMatrix, cameraTransformMatrix), modelMatrix), vector)
        w = abs(clipSpace[3])
        if w == 0:
            w = 1 # This is to avoid a divide by zero error.
        finalCoordinate = [clipSpace[0] / w, clipSpace[1] / w, clipSpace[2]]

        return (finalCoordinate[0], finalCoordinate[1], finalCoordinate[2])

    # Returns a list of points for that shape
    # as well as a zIndex from -1 to 1 for how close the shape is to the camera
    def renderPolygon(self, polygon, position):
        result = []
        zAverage = 0
        for point in polygon.points:
            newPoint= self.renderPoint(point, position)
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
    def moveToWorldView(self, point, position):
        modelMatrix = np.array([[1, 0, 0, position[0]],
                                [0, 1, 0, position[1]],
                                [0, 0, 1, position[2]],
                                [0, 0, 0, 1]])
        point = np.transpose(np.array([point[0], point[1], point[2], 1]))
        movedPoint = np.dot(modelMatrix, point)
        return (movedPoint[0], movedPoint[1], movedPoint[2])
    
    # Scales values to screen width and height and flips the y
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
            for polygon in shape.polygons:
                points, zIndex = self.renderPolygon(polygon, shape.position)
                allPoints[zIndex] = points
                colors[zIndex] = polygon.color
                indexes.append(zIndex)
        return allPoints, colors, sorted(indexes, reverse=True)