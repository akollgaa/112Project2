# Data structure for any physical object that should be displayed
class Object:
    
    # points is a list of tuples, (x, y, z)
    def __init__(self, points):
        
        self.points = points

    def __repr__(self):
        pointDescription = ''
        for point in self.points:
            pointDescription += str(point) + ', '
        pointDescription = pointDescription[:len(pointDescription) - 2]
        return 'Points(' + pointDescription + ')'
    
    def __eq__(self, other):
        return (isinstance(other, Object) and 
                self.points == other.points)

    def addPoint(self, point):
        self.points.append(point)

    def removePoint(self, point):
        self.points.remove(point)