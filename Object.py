# Data structure for any physical object that should be displayed
class Shape:
    
    # points is a list of tuples, (x, y, z)
    def __init__(self, points, color):
        self.points = points
        self.color = color

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

    def addPoint(self, point):
        self.points.append(point)

    def removePoint(self, point):
        self.points.remove(point)