from Object import Shape
import numpy as np
import math
from Model import Ship
from Model import Projectile
from Model import Ground
from Model import Enemy
from Model import Obstacle
from Model import PowerUp

class Graphics:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cameraPosition = (0, 5, 0) # x, y, z
        self.cameraOrientation = (-15, 0, 0.5) # pitch, roll, yaw
        self.fov = math.pi / 2
        self.shapes = []
        self.ships = []
        self.projectiles = []
        self.ground = []
        self.enemies = []
        self.obstacles = []
        self.powerups = []
        self.shapesToRemove = set()
        self.projectilesToRemove = set()
        self.powerupsToRemove = set()

        # We only need to calculate the perspectiveMatrix once and then reference later
        # Aspect Ratio
        a = self.height / self.width
        f = 1 / math.tan(self.fov / 2)
        # normalization constant
        # Assuming camera is at origin looking down z axis
        znear = 1
        zfar =  100
        l = zfar / (zfar - znear)
        # Converts points based on fov, aspect ratio, and depth
        self.perspectiveMatrix = np.array([[f * a,  0, 0,          0],
                                        [    0,  f, 0,          0],
                                        [    0,  0, l, -l * znear],
                                        [    0,  0, 1,          0]])

    def addProjectile(self, shape, speed, power, direction, position=(0, 0, 0), orientation=(0, 0, 0)):
        self.projectiles.append(Projectile(shape, speed, power, direction, position, orientation))

    def addShip(self, shape, captain, speed, jerk, health):
        self.ships.append(Ship(shape, captain, speed, jerk, health))

    def addShape(self, shape, position=(0, 0, 0), orientation=(0, 0, 0)):
        self.shapes.append(Shape(shape, position, orientation))

    def addGround(self, shape):
        self.ground.append(Ground(shape))

    def addEnemy(self, shape, position, standPosition, health, shootRate):
        self.enemies.append(Enemy(shape, position, standPosition, health, shootRate))
    
    def addObstacle(self, shape, position, length):
        self.obstacles.append(Obstacle(shape, position, length))

    def addPowerUp(self, shape, position, healthValue):
        self.powerups.append(PowerUp(shape, position, healthValue))

    # Removes both shapes and obstacles 
    def removeShapes(self):
        removed = False
        for shape in self.shapesToRemove:
            if type(shape) == Shape:
                self.shapes.remove(shape)
            elif type(shape) == Obstacle:
                self.obstacles.remove(shape)
            removed = True
        self.shapesToRemove = set()
        return removed
    
    def removeProjectile(self):
        for projectile in self.projectiles:
            if (projectile.distanceTraveled > 200 or 
                projectile.position[2] < self.cameraPosition[2]):
                self.projectilesToRemove.add(projectile)
        for projectile in self.projectilesToRemove:
            self.projectiles.remove(projectile)
        self.projectilesToRemove = set()

    def removePowerUps(self):
        for powerup in self.powerups:
            if powerup.position[2] < self.cameraPosition[2]:
                self.powerupsToRemove.add(powerup)
        for powerup in self.powerupsToRemove:
            self.powerups.remove(powerup)
        self.powerupsToRemove = set()

    def removeEnemies(self):
        enemiesToRemove = []
        for enemy in self.enemies:
            if enemy.health <= 0 or enemy.position[2] < self.cameraPosition[2]:
                enemiesToRemove.append(enemy)
        for enemy in enemiesToRemove:
            self.enemies.remove(enemy)

    def resetCamera(self):
        self.cameraPosition = [0, 0, 0] # x, y, z
        self.cameraOrientation = [0, 0, 0] # pitch, roll, yaw

    # This is quite buggy
    def resetCameraToShip(self):
        if len(self.ships) == 0:
            return
        dx = self.ships[0].position[0] - self.cameraPosition[0]
        dy = self.ships[0].position[1] - (self.cameraPosition[1])
        dz = self.ships[0].position[2] - (self.cameraPosition[2])
        self.moveCameraPosition(dx, dy + 4, dz + 12)

    def resetShipToCamera(self):
        if len(self.ships) == 0:
            return
        self.ships[0].position = (self.cameraPosition[0], self.cameraPosition[1], self.cameraPosition[2])
        self.ships[0].moveShip(0, -4, 12)

    # Moves the camera by some constant direction
    def moveCameraPosition(self, dx, dy, dz):
        self.cameraPosition = (self.cameraPosition[0] + dx, 
                               self.cameraPosition[1] + dy, 
                               self.cameraPosition[2] + dz)

    # Moves the camera orientation by some constant direction
    def moveCameraOrientation(self, dp, dr, dy):
        self.cameraOrientation = (self.cameraOrientation[0] + dp,
                                  self.cameraOrientation[1] + dr,
                                  self.cameraOrientation[2] + dy)

    # Takes angles in radians
    def moveFOV(self, angle):
        self.fov += angle

    # Point and position is a tuple (x, y, z)
    # Orientation is a tuple of (pitch, roll, yaw)
    # Some of the math was learned from
    # https://www.3dgep.com/understanding-the-view-matrix/
    # https://www.youtube.com/watch?v=EqNcqBdrNyI&ab_channel=pikuma
    # Returns a (x, y) that can be placed on the screen
    def renderPoint(self, point, modelMatrix, cameraTransformMatrix):
        # We must convert our point tuple to a np array
        vector = np.transpose(np.array([point[0], point[1], point[2], 1]))
        
        # Combines all spaces together in one big matrix
        clipSpace = np.dot(np.dot(np.dot(self.perspectiveMatrix, cameraTransformMatrix), modelMatrix), vector)
        w = abs(clipSpace[3])

        # This is to avoid a divide by zero error.
        if w == 0:
            w = 1
        finalCoordinate = [clipSpace[0] / w, clipSpace[1] / w, clipSpace[2]]

        return (finalCoordinate[0], finalCoordinate[1], finalCoordinate[2])

    # Returns a list of points for that shape
    # as well as a zIndex from -1 to 1 for how close the shape is to the camera
    def renderPolygon(self, polygon, modelMatrix, cameraTransformMatrix):
        result = []
        zAverage = 0
        calculatedPoints = dict()
        for point in polygon.points:
            if point in calculatedPoints:
                result.append(calculatedPoints[point][0])
                result.append(calculatedPoints[point][1])
                zAverage += calculatedPoints[point][2]
                continue
            newPoint = self.renderPoint(point, modelMatrix, cameraTransformMatrix)
            newPoint = self.convertImageSpaceToScreen(newPoint)
            result.append(newPoint[0])
            result.append(newPoint[1])
            zAverage += newPoint[2]
            calculatedPoints[point] = newPoint
        # Divide by the # of points, but result contains each x,y so divide by 2.
        zAverage = zAverage / (len(result) / 2) 
        return (result, zAverage)
    
    def createCameraTransformMatrix(self):
        cameraTranslationMatrix = np.array([[1, 0, 0, self.cameraPosition[0]],
                                            [0, 1, 0, self.cameraPosition[1]],
                                            [0, 0, 1, self.cameraPosition[2]],
                                            [0, 0, 0, 1]])
        theta1 = (self.cameraOrientation[2]) * (math.pi / 180)
        theta2 = (self.cameraOrientation[0]) * (math.pi / 180)
        theta3 = (self.cameraOrientation[1]) * (math.pi / 180)
        cameraRotationYMatrix = np.array([[ math.cos(theta1), 0, math.sin(theta1), 0],
                                          [                0, 1,                0, 0],
                                          [-math.sin(theta1), 0, math.cos(theta1), 0],
                                          [                0, 0,                0, 1]])
        
        cameraRotationXMatrix = np.array([[1,                0,                 0, 0],
                                          [0, math.cos(theta2), -math.sin(theta2), 0],
                                          [0, math.sin(theta2),  math.cos(theta2), 0],
                                          [0,                0,                 0, 1]])
        cameraRotationZMatrix = np.array([[math.cos(theta3), -math.sin(theta3), 0, 0],
                                          [math.sin(theta3),  math.cos(theta3), 0, 0],
                                          [               0,                 0, 1, 0],
                                          [               0,                 0, 0, 1]])
        rotationMatrix = np.dot(np.dot(cameraRotationYMatrix, cameraRotationXMatrix), cameraRotationZMatrix)
        return np.dot(rotationMatrix, cameraTranslationMatrix)
    
    def createModelMatrix(self, position, orientation):
        # The positions are negated to align with the axis of the camera.
        translationMatrix = np.array([[1, 0, 0, -position[0]],
                                      [0, 1, 0, -position[1]],
                                      [0, 0, 1, -position[2]],
                                      [0, 0, 0,            1]])
        theta1 = orientation[2] * (math.pi / 180)
        theta2 = orientation[0] * (math.pi / 180)
        theta3 = orientation[1] * (math.pi / 180)
        rotationYMatrix = np.array([[ math.cos(theta1), 0, math.sin(theta1), 0],
                                    [                0, 1,                0, 0],
                                    [-math.sin(theta1), 0, math.cos(theta1), 0],
                                    [                0, 0,                0, 1]])
        
        rotationXMatrix = np.array([[1,                0,                 0, 0],
                                    [0, math.cos(theta2), -math.sin(theta2), 0],
                                    [0, math.sin(theta2),  math.cos(theta2), 0],
                                    [0,                0,                 0, 1]])
        rotationZMatrix = np.array([[math.cos(theta3), -math.sin(theta3), 0, 0],
                                    [math.sin(theta3),  math.cos(theta3), 0, 0],
                                    [               0,                 0, 1, 0],
                                    [               0,                 0, 0, 1]])
        rotationMatrix = np.dot(np.dot(rotationXMatrix, rotationYMatrix), rotationZMatrix)
        return np.dot(translationMatrix, rotationMatrix)
    
    # Scales values to screen width and height and flips the y
    def convertImageSpaceToScreen(self, point):
        screenX = int(point[0] * self.width) + self.width / 2
        screenY = int(point[1] * self.height) + self.height / 2
        return (screenX, screenY, point[2])
    
    # Takes in two tuples or lists of length 3 (x, y, z)
    def distance(self, p1, p2):
        return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5

    # Mutates both shapes and shapeIndexes
    def renderListOfShapes(self, shapes, shapeIndexes, listOfShapes, isRemoving=True):
        cameraTransformMatrix = self.createCameraTransformMatrix()
        for shape in listOfShapes:
            # Check to make sure only objects only from the shape class are being considered
            if ((type(shape) == Shape or type(shape) == Obstacle) and 
                shape.midpoint[2] <= self.cameraPosition[2] and isRemoving):
                self.shapesToRemove.add(shape)
                continue
            color = None
            if (type(shape) == Ship or type(shape) == Enemy) and shape.hit >= 1:
                color = 'white'
                shape.hit += 1
            elif (type(shape) == Ship or type(shape) == Enemy) and shape.heal >= 1:
                color = 'brown'
                shape.heal += 1
            dist = self.distance(self.cameraPosition, shape.midpoint)
            allPoints = dict()
            colors = dict()
            indexes = []
            modelMatrix = self.createModelMatrix(shape.position, shape.orientation)
            for polygon in shape.polygons:
                points, zIndex = self.renderPolygon(polygon, modelMatrix, cameraTransformMatrix)
                allPoints[zIndex] = points
                colors[zIndex] = color if color != None else polygon.color
                indexes.append(zIndex)
            shapes[dist] = (allPoints, colors, sorted(indexes, reverse=False))
            shapeIndexes.append(dist)

    def render(self, pov):
        shapes = dict()
        shapeIndexes = []
        self.renderListOfShapes(shapes, shapeIndexes, self.shapes)
        if pov: # only render the player ship if in third person mode
            self.renderListOfShapes(shapes, shapeIndexes, self.ships)
        self.renderListOfShapes(shapes, shapeIndexes, self.projectiles)
        self.renderListOfShapes(shapes, shapeIndexes, self.enemies)
        self.renderListOfShapes(shapes, shapeIndexes, self.obstacles)
        for powerup in self.powerups:
            # We do not want to remove the powerup shapes because they
            # are not contained within the shapes list
            self.renderListOfShapes(shapes, shapeIndexes, powerup.orbs, False)
        ground = dict()
        groundIndexes = []
        self.renderListOfShapes(ground, groundIndexes, self.ground)
        return (shapes, sorted(shapeIndexes, reverse=True), ground, groundIndexes)