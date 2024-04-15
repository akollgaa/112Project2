# Data structure for any physical object that should be displayed
class Shape:
    
    # shape is a collection of tuples that contain a polygon and color
    def __init__(self, shape, position=(0, 0, 0), flipAxis=True):
        self.polygons = []
        self.position = position
        for points, color in shape:
            self.polygons.append(Polygon(points, color))
        
        if flipAxis:
            self.position = (position[0], -position[1], position[2])

    def __repr__(self):
        return f'Shape containing {len(self.polygons)} polygons'
    
    def __eq__(self, other):
        return (isinstance(other, Shape) and 
                self.polygons == other.polygons)
    
    def __hash__(self):
        return hash(str(self))
    
class Polygon:
    def __init__(self, points, color, flipAxis=True):
        self.points = points # list of tuple of points
        self.color = color
        if flipAxis:
            newPoints = []
            for point in self.points:
                newPoints.append((point[0], -point[1], point[2]))
            self.points = newPoints
            print(self.points)

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