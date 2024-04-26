from Object import Shape
import random

# This is used for debugging/testing purposes
def createRectangularPrism(width, length, height):
    x = width / 2
    y = height / 2
    z = length / 2
    front = [(-x, y, z),
            (x, y, z),
            (x, -y, z),
            (-x, -y, z)]
    back = [(-x, y, -z),
            (x, y, -z),
            (x, -y, -z),
            (-x, -y, -z)]
    left = [(-x, y, z),
            (-x, y, -z),
            (-x, -y, -z),
            (-x, -y, z)]
    right = [(x, y, z),
            (x, y, -z),
            (x, -y, -z),
            (x, -y, z)]
    top = [(-x, y, z),
            (-x, y, -z),
            (x, y, -z),
            (x, y, z)]
    bottom = [(-x, -y, z),
            (-x, -y, -z),
            (x, -y, -z),
            (x, -y, z)]
    prism = [(front, 'red'),
             (back, 'yellow'),
             (left, 'green'),
             (right, 'blue'),
             (bottom, 'purple'),
             (top, 'orange')]
    return prism

def createBuilding(width, length, height):
    x = width / 2
    y = height / 2
    z = length / 2
    front = [(-x, y, z),
            (x, y, z),
            (x, -y, z),
            (-x, -y, z)]
    back = [(-x, y, -z),
            (x, y, -z),
            (x, -y, -z),
            (-x, -y, -z)]
    left = [(-x, y, z),
            (-x, y, -z),
            (-x, -y, -z),
            (-x, -y, z)]
    right = [(x, y, z),
            (x, y, -z),
            (x, -y, -z),
            (x, -y, z)]
    top = [(-x, y, z),
            (-x, y, -z),
            (x, y, -z),
            (x, y, z)]
    bottom = [(-x, -y, z),
            (-x, -y, -z),
            (x, -y, -z),
            (x, -y, z)]
    building = [(front, 'darkgray'),
             (back, 'darkgray'),
             (left, 'darkgray'),
             (right, 'darkgray'),
             (bottom, 'darkgray'),
             (top, 'darkgray')]
    return building

def createObstacle(width, length, height):
    x = width / 2
    y = height / 2
    z = length / 2
    front = [(-x, y, z),
            (x, y, z),
            (x, -y, z),
            (-x, -y, z)]
    back = [(-x, y, -z),
            (x, y, -z),
            (x, -y, -z),
            (-x, -y, -z)]
    left = [(-x, y, z),
            (-x, y, -z),
            (-x, -y, -z),
            (-x, -y, z)]
    right = [(x, y, z),
            (x, y, -z),
            (x, -y, -z),
            (x, -y, z)]
    top = [(-x, y, z),
            (-x, y, -z),
            (x, y, -z),
            (x, y, z)]
    bottom = [(-x, -y, z),
            (-x, -y, -z),
            (x, -y, -z),
            (x, -y, z)]
    obstacle = [(front, 'lightgray'),
             (back, 'lightgray'),
             (left, 'lightgray'),
             (right, 'lightgray'),
             (bottom, 'lightgray'),
             (top, 'lightgray')]
    return obstacle

def shipModel(size, flip=False):
    zFlip = -1 if flip else 1

    top = [(-size, size, size),
           (-size, size, -size),
           (size, size, -size),
           (size, size, size)]
    bottom = [(-size, -size, size),
              (-size, -size, -size),
              (size, -size, -size),
              (size, -size, size)]
    left = [(-size, size, size),
            (-size, size, -size),
            (-size, -size, -size),
            (-size, -size, size)]
    right = [(size, size, size),
             (size, size, -size),
             (size, -size, -size),
             (size, -size, size)]
    back = [(-size, size, zFlip * size),
            (-size, -size, zFlip * size),
            (size, -size, zFlip * size),
            (size, size, zFlip * size)]
    frontTop = [(-size, size, -zFlip * size),
                (size, size, -zFlip * size),
                (size, 0, -zFlip * size * 3),
                (-size, 0, -zFlip * size * 3)]
    frontBottom = [(-size, -size, -zFlip * size),
                (size, -size, -zFlip * size),
                (size, 0, -zFlip * size * 3),
                (-size, 0, -zFlip * size * 3)]
    frontLeft = [(-size, size, -zFlip * size),
                 (-size, -size, -zFlip * size),
                 (-size, 0, -zFlip * size * 3)]
    frontRight = [(size, size, -zFlip * size),
                  (size, -size, -zFlip * size),
                  (size, 0, -zFlip * size * 3)]
    leftWingTop = [(-size, 0, -zFlip * size),
                   (-size, 0, zFlip * size),
                   (-(size * 4), -(size * 0.25), zFlip * (size * 2)),
                   (-(size * 4), -(size * 0.25), zFlip * size)]
    leftWingBottom = [(-size, -(size*0.25), -zFlip * size),
                      (-size, -(size*0.25), zFlip * size),
                      (-(size * 4), -(size * 0.25), zFlip * (size * 2)),
                      (-(size * 4), -(size * 0.25), zFlip * size)]
    leftWingBack = [(-size, 0, zFlip * size),
                    (-size, -(size*0.25), zFlip * size),
                    (-(size * 4), -(size * 0.25), zFlip * (size * 2))]
    leftWingFront = [(-size, 0, -zFlip * size),
                     (-size, -(size*0.25), -zFlip * size),
                     (-(size * 4), -(size * 0.25), zFlip * size)]
    rightWingTop = [(size, 0, -zFlip * size),
                   (size, 0, size),
                   ((size * 4), -(size * 0.25), zFlip * (size * 2)),
                   ((size * 4), -(size * 0.25), zFlip * size)]
    rightWingBottom = [(size, -(size*0.25), -zFlip * size),
                      (size, -(size*0.25), zFlip * size),
                      ((size * 4), -(size * 0.25), zFlip * (size * 2)),
                      ((size * 4), -(size * 0.25), zFlip * size)]
    rightWingBack = [(size, 0, zFlip * size),
                    (size, -(size*0.25), zFlip * size),
                    ((size * 4), -(size * 0.25), zFlip * (size * 2))]
    rightWingFront = [(size, 0, -zFlip * size),
                     (size, -(size*0.25), -zFlip * size),
                     ((size * 4), -(size * 0.25), zFlip * size)]
    shipPrism = [(top, 'gray'),
                 (bottom, 'gray'),
                 (back, 'gray'),
                 (left, 'gray'),
                 (right, 'gray'),
                 (frontTop, 'black'),
                 (frontRight, 'gray'),
                 (frontLeft, 'gray'),
                 (frontBottom, 'gray'),
                 (leftWingTop, 'blue'),
                 (leftWingBottom, 'blue'),
                 (leftWingBack, 'red'),
                 (leftWingFront, 'red'),
                 (rightWingTop, 'blue'),
                 (rightWingBottom, 'blue'),
                 (rightWingBack, 'red'),
                 (rightWingFront, 'red')]
    return shipPrism

def projectileModel(size):
    backTop = [(-size, size, 0),
               (size, size, 0),
               (0, 0, -size*4)]
    backBottom = [(-size, -size, 0),
               (size, -size, 0),
               (0, 0, -size*4)]
    backLeft = [(-size, -size, 0),
                (-size, size, 0),
                (0, 0, -size*4)]
    backRight = [(size, size, 0),
                 (size, -size, 0),
                 (0, 0, -size*4)]
    frontTop = [(-size, size, 0),
               (size, size, 0),
               (0, 0, size*2)]
    frontBottom = [(-size, -size, 0),
               (size, -size, 0),
               (0, 0, size*2)]
    frontLeft = [(-size, -size, 0),
                (-size, size, 0),
                (0, 0, size*2)]
    frontRight = [(size, size, 0),
                 (size, -size, 0),
                 (0, 0, size*2)]
    projectilePrism = [(backTop, 'cyan'),
                       (backBottom, 'cyan'),
                       (backLeft, 'cyan'),
                       (backRight, 'cyan'),
                       (frontTop, 'cyan'),
                       (frontBottom, 'cyan'),
                       (frontLeft, 'cyan'),
                       (frontRight, 'cyan')]
    return projectilePrism 
    

class Obstacle(Shape):

    def __init__(self, shape, position, length):
        super().__init__(shape, position)
        self.power = 10 # Arbitrary power value
        self.radius = length // 2
        # Grabs the height data of the first Polygon's coordinate
        # For a rectangularPrism this is the front panel
        self.height = abs(shape[0][0][0][1]) * 2

class Ground(Shape):

    def __init__(self, shape):
        z = abs(shape[0][0][0][2])
        super().__init__(shape, position=(0, 0, z))

    # Moves the location of the ground forward by a litte
    def updateGround(self, z):
        self.movePosition(0, 0, z)

class Projectile(Shape):

    def __init__(self, shape, speed, power, direction, position=(0, 0, 0), orientation=(0, 0, 0)):
        super().__init__(shape, position, orientation)
        self.speed = speed # Can be negative to indicate direction
        self.power = power
        self.direction = direction
        self.distanceTraveled = 0

    # Not the most elegant way, but because position is a tuple not much I can do
    def move(self):
        self.distanceTraveled += abs(self.speed)
        if self.direction == 0:
            dx = self.speed
            self.position = (self.position[0] + dx, self.position[1], self.position[2])
        elif self.direction == 1:
            dy = self.speed
            self.position = (self.position[0], self.position[1] + dy, self.position[2])
        elif self.direction == 2:
            dz = self.speed
            self.position = (self.position[0], self.position[1], self.position[2] + dz)
        self.updateMidPoint()

class Ship(Shape):

    def __init__(self, shape, captain, speed, jerk, health):
        super().__init__(shape) # Assume default parameters
        self.captain = captain
        self.speed = speed
        self.jerk = jerk
        self.health = health
        self.hit = 0
        self.heal = 0
        self.boost = 0
        self.boostCooldown = 40

    def __repr__(self):
        return f"{self.captain} is the captain: Speed({self.speed}) and Jerk({self.jerk}) at ({self.position})"
    
    def __eq__(self, other):
        return (isinstance(other, Ship) and 
            self.captain == other.captain)

    def __hash__(self):
        return hash(str(repr))
    
    def moveShip(self, dx, dy, dz):
        super().movePosition(dx, dy, dz)

    def tiltShip(self, dp, dr, dy):
        super().moveOrientation(dp, dr, dy)

    def startBarrelRoll(self):
        # The roll must be faster so jerk is increased
        self.tiltShip(0, self.jerk * 10, 0)

    def performBarrelRoll(self):
        # The roll must be faster so jerk is increased
        if self.orientation[1] != 0: # adds to the roll
            self.tiltShip(0, self.jerk * 10, 0)
        if self.orientation[1] >= 360: # Resets the roll
            self.tiltShip(0, -self.orientation[1], 0)

    def startBoost(self):
        if self.boost == 0 and self.boostCooldown == 40:
            self.boost += 1
            self.boostCooldown = 0

    def performBoost(self):
        if self.boost != 0:
            self.speed += 1
            self.boost += 1
        if self.boost > 15:
            self.speed -= 15
            self.boost = 0
        self.updateBoostCooldown()

    def updateBoostCooldown(self):
        if self.boostCooldown != 40:
            self.boostCooldown += 1

class Enemy(Ship):

    # shootRate is going to be a value out of 100
    # 0 being impossible and 100 being guaranteed.
    def __init__(self, shape, position, standPosition, health, shootRate):
        super().__init__(shape, 'Enemy', 6, 4, health)
        self.position = position
        self.standPosition = standPosition
        self.shootRate = shootRate
        self.updateMidPoint()

    def __repr__(self):
        return f'Enemy ship with health: {self.health}'
    
    def __eq__(self, other):
        return (isinstance(other, Enemy) and 
                self.health == other.health and
                self.position == other.position)
    
    def __hash__(self):
        return hash(str(self))
    
    def shoot(self):
        shooting = random.randrange(0, 100)
        if self.shootRate > shooting:
            return True
        return False
    
    def moveToStandPosition(self):
        dx, dy, dz = 0, 0, 0
        if abs(self.position[0] - self.standPosition[0]) > self.speed:
            xDirection = -1 if self.position[0] > self.standPosition[0] else 1
            dx = self.speed * xDirection
        if abs(self.position[1] - self.standPosition[1]) > self.speed:
            yDirection = -1 if self.position[1] > self.standPosition[1] else 1
            dy = self.speed * yDirection
        if abs(self.position[2] - self.standPosition[2]) > self.speed:
            zDirection = -1 if self.position[2] > self.standPosition[2] else 1
            dz = self.speed * zDirection
        self.moveShip(dx, dy, dz)

class PowerUp(Shape):

    def __init__(self, shape, position, healthValue):
        self.position = position
        self.healthValue = healthValue
        self.radius = 5
        self.rotateSpeed = 3
        leftPos = (position[0] - self.radius, position[1], position[2])
        rightPos = (position[0] + self.radius, position[1], position[2])
        topPos = (position[0], position[1] + self.radius, position[2])
        bottomPos = (position[0], position[1] - self.radius, position[2])
        self.orbs = [Shape(shape, leftPos),
                    Shape(shape, rightPos),
                    Shape(shape, topPos),
                    Shape(shape, bottomPos)]
        self.midpoint = self.position

    def __repr__(self):
        return f"Power up at {self.position} with {self.healthValue}"
    
    def __eq__(self, other):
        return (isinstance(other, PowerUp) and
                self.position == other.position and
                self.orbs == other.orbs)
    
    def __hash__(self):
        return hash(str(self))

    def movePosition(self, dx, dy, dz):
        for orb in self.orbs:
            orb.movePosition(dx, dy, dz)

    def moveOrientation(self, dp, dr, dy):
        for orb in self.orbs:
            orb.moveOrientation(dp, dr, dy)

    def updateMidPoint(self):
        self.midpoint = self.calculateMidpoint()

    def calculateMidpoint(self, addPosition=True):
        if addPosition:
            return self.position
        else:
            return (0, 0, 0)
        
    def rotateOrbs(self):
        self.moveOrientation(0, self.rotateSpeed, self.rotateSpeed)


