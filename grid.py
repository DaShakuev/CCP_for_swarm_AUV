from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as ShapelyPolygon

class Grid:
    def __init__(self, plt, vertices, coord_x, coord_y, state = -1):
        self.plt = plt
        self.vertices = vertices
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.state = self.point_inside_polygon()
        


    def point_inside_polygon(self):
        """
        Проверка, находится ли точка внутри многоугольника.
        
        Параметры:
        point (tuple): Координаты точки в формате (x, y)
        vertices (list of tuples): Массив вершин многоугольника в формате [(x1, y1), (x2, y2), ..., (xn, yn)]
        
        Возвращает:
        bool: True, если точка находится внутри многоугольника, False в противном случае
        """
        polygon = ShapelyPolygon(self.vertices)
        point = Point((self.coord_x, self.coord_y))
        self.state = int(polygon.contains(point))

        if self.state: self.plt.plot(self.coord_x, self.coord_y, 'go')
        else : self.plt.plot(self.coord_x, self.coord_y, 'ro')
        
        return self.state
    
