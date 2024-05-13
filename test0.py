from area import Area
from grid import Grid

vertices1 = [(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)]
vertices2 = [(2, 18), (8, 19), (14, 15), (17, 8), (5, 3)]
vertices3 = [(1, 6), (4, 18), (10, 20), (16, 15), (18, 7)]
vertices4 = [(3, 12), (7, 18), (14, 19), (18, 11), (12, 6)]
vertices5 = [(2, 8), (8, 18), (12, 20), (16, 12), (6, 5)]
gs = 0.9
grid_size = 25

Area(vertices1, gs, grid_size)
Area(vertices2, gs, grid_size)
Area(vertices3, gs, grid_size)
Area(vertices4, gs, grid_size)
Area(vertices5, gs, grid_size)