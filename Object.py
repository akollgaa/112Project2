# Data structure for any physical object that should be displayed
class Shape:
    
    # shape is a collection of tuples that contain a polygon and color
    # We naturally want to flip the axis because the camera will render everything upsidedown
    def __init__(self, shape, position=(0, 0, 0), orientation=(0, 0, 0), flipAxis=True):
        self.polygons = []
        self.position = position
        self.orientation = orientation
        for points, color in shape:
            self.polygons.append(Polygon(points, color))
        self.midpoint = self.calculateMidpoint()

    def __repr__(self):
        return f'Shape containing {len(self.polygons)} polygons at ({self.position})'
    
    def __eq__(self, other):
        return (isinstance(other, Shape) and 
                self.polygons == other.polygons and 
                self.position == other.position and
                self.orientation == other.orientation)
    
    def __hash__(self):
        return hash(str(self))
    
    def movePosition(self, dx, dy, dz):
        self.position = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
        self.updateMidPoint()

    # Pitch, Roll, Yaw
    def moveOrientation(self, dp, dr, dy):
        self.orientation = (self.orientation[0] + dp, self.orientation[1] + dr, self.orientation[2] + dy)

    def updateMidPoint(self):
        self.midpoint = self.calculateMidpoint()

    # calculates midpoint with respect to its position
    def calculateMidpoint(self, addPosition=True):
        xMid, yMid, zMid = 0, 0, 0
        for polygon in self.polygons:
            xSum, ySum, zSum = 0, 0, 0
            for x, y, z in polygon.points:
                xSum += x
                ySum += y
                zSum -= z
            xMid += xSum / len(polygon.points)
            yMid += ySum / len(polygon.points)
            zMid += zSum / len(polygon.points)
        result = (xMid / len(self.polygons), yMid / len(self.polygons), zMid / len(self.polygons))
        if addPosition:
            return (result[0] + self.position[0], result[1] + self.position[1], result[2] + self.position[2])
        return result

class Polygon:
    # We naturally want to flip the axis because the camera will render everything upsidedown
    def __init__(self, points, color, flipAxis=True):
        self.points = points # list of tuple of points
        self.color = color
        if flipAxis:
            newPoints = []
            for point in self.points:
                newPoints.append((point[0], -point[1], point[2]))
            self.points = newPoints

    def __repr__(self):
        pointDescription = ''
        for point in self.points:
            pointDescription += str(point) + ', '
        pointDescription = pointDescription[:len(pointDescription) - 2]
        return 'Points(' + pointDescription + ')'
    
    def __eq__(self, other):
        return (isinstance(other, Shape) and 
                self.points == other.points and
                self.color == other.color)
    
    def __hash__(self):
        return hash(str(self))
    
    def calculateMidpoint(self):
        xSum, ySum, zSum = 0, 0, 0
        for x, y, z in self.points:
            xSum += x
            ySum += y
            zSum += z
        xMid = xSum / len(self.points)
        yMid = ySum / len(self.points)
        zMid = zSum / len(self.points)
        return (xMid, yMid, zMid)
