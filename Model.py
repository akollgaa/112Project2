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