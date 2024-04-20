from Object import Shape

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

class Building(Shape):

    def __init__(self, shape, position):
        super().__init__(shape, position)

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

class Ship(Shape):

    def __init__(self, shape, captain, speed, jerk):
        super().__init__(shape) # Assume default parameters
        self.captain = captain
        self.speed = speed
        self.jerk = jerk
        
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