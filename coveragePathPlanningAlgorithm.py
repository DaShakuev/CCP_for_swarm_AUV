import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from shapely.geometry import LineString, Point
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry import MultiPolygon
from shapely import distance as getDistance
from shapely.ops import unary_union
from tack import Tack

def get_angle(edge):
    """Вычислить угол наклона ребра в радианах."""
    p1, p2 = edge
    return np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

def get_shift(angle, distance):
    """Вычислить координаты смещённой точки на заданный угол и расстояние."""
    return np.array([distance * np.cos(angle), distance * np.sin(angle)])

def get_straight_line(point, angle):
    """Получить прямую линию, заданную точкой и углом."""
    end_point = point + get_shift(angle, 100) 
    start_point = point + get_shift(angle-np.pi, 100) 
    return LineString([start_point, end_point])

def get_cross_points(line, edge):
    """Получить точки пересечения линии с ребром."""
    intersection = line.intersection(edge)
    if intersection.is_empty:
        return []
    elif isinstance(intersection, Point):
        return [intersection]
    else:
        return list(intersection)
    
def get_segments_inside_region(cross_points, region):
    """Создать отрезки линий из точек пересечения и отфильтровать те, что внутри региона."""
    if len(cross_points) < 2:
        return []
    segments = []
    for i in range(len(cross_points) - 1):
        segment = LineString([cross_points[i], cross_points[i+1]])
        # if region.contains(segment):
        segments.append(segment)
    return segments

def get_subtraction(region, cover_rect):
    """Вычесть покрывающий прямоугольник из региона."""
    return region.difference(cover_rect)

def get_cover_rectangle(tack):
    """Создать покрывающий прямоугольник вокруг такта (заглушка реализации)."""
    return tack.buffer(0.5)

def find_maximum(vector_criterion):
    """Найти такт с максимальным значением критерия."""
    return max(vector_criterion, key=vector_criterion.get)

def remove_micro_polygons(region):
    """Удалить очень маленькие полигоны из региона."""
    min_area = 2

    if isinstance(region, ShapelyPolygon):
        if region.area > min_area:
            return region
        else:
            return ShapelyPolygon()
    else:
        large_polygons = []
        for p in region.geoms:
            if p.area > min_area:
                large_polygons.append(p)
        return unary_union(large_polygons)
    
def plot_polygon(polygon):
    """Функция для рисования многоугольника или мультиполигона."""
    if isinstance(polygon, ShapelyPolygon):
        x, y = polygon.exterior.xy
        plt.plot(x, y)
    elif isinstance(polygon, MultiPolygon):
        for poly in polygon.geoms:
            x, y = poly.exterior.xy
            plt.plot(x, y)
    plt.show()

def plot_paths(paths,plt,ax):
    """
    Функция для отображения массива объектов LineString.

    :param paths: Список объектов LineString.
    """
    # Проходим по каждому LineString в массиве paths
    for path in paths:
        x, y = path.xy  # Извлекаем координаты x и y
        ax.plot(x, y,'r')  # Рисуем линии на графике
    plt.show()

def nearest_end_point(point_coords, linestring):
    """
    Функция для нахождения ближайшей конечной точки на LineString к заданной точке.

    :param point_coords: Координаты точки в формате (x, y).
    :param linestring: Объект LineString.
    :return: Ближайшая конечная точка на LineString к исходной точке.
    """
    # Преобразуем координаты точки в объект Point
    point = Point(point_coords)
    
    # Получаем начальную и конечную точки LineString
    start_point = Point(linestring.coords[0])
    end_point = Point(linestring.coords[-1])
    
    # Вычисляем расстояние от заданной точки до начальной и конечной точки LineString
    distance_to_start = point.distance(start_point)
    distance_to_end = point.distance(end_point)
    
    # Возвращаем ближайшую точку
    if distance_to_start < distance_to_end:
        return start_point
    else:
        return end_point
    
def highest_vertex(line):
    """
    Функция для определения вершины отрезка с наибольшей координатой y.

    :param segment: Объект LineString, представляющий отрезок.
    :return: Вершина отрезка с наибольшей координатой y.
    """
    # Извлекаем координаты вершин отрезка
    start_point = line.coords[0]
    end_point = line.coords[-1]

    # Сравниваем координаты y вершин и возвращаем вершину с бОльшим y
    if start_point[1] > end_point[1]:
        return start_point
    else:
        return end_point
    
def low_vertex(line):
    """
    Функция для определения вершины отрезка с наименьшей координатой y.

    :param segment: Объект LineString, представляющий отрезок.
    :return: Вершина отрезка с наибольшей координатой y.
    """
    # Извлекаем координаты вершин отрезка
    start_point = line.coords[0]
    end_point = line.coords[-1]

    # Сравниваем координаты y вершин и возвращаем вершину с low y
    if start_point[1] < end_point[1]:
        return start_point
    else:
        return end_point
    
def get_nearest_point(point, linestrings):
    """
    Найти ближайшую точку на любом linestring к заданной точке.

    :param point: исходная точка (shapely.geometry.Point)
    :param linestrings: список линий (список shapely.geometry.LineString)
    :return: ближайшая точка (shapely.geometry.Point) и расстояние до неё
    """
    min_distance = float('inf')
    nearest_point = None

    for linestring in linestrings:
        distance1 = getDistance(point, Point(linestring.coords[0]))
        distance2 = getDistance(point, Point(linestring.coords[-1]))
        if distance1 > distance2:
            current_distance = distance1
            current_nearest_point = linestring.coords[0]
        else:
            current_distance = distance2
            current_nearest_point = linestring.coords[-1]
        if current_distance < min_distance:
            min_distance = current_distance
            nearest_point = current_nearest_point

    return nearest_point, min_distance

def link_tacks_sequentially(TackList):
    """Связать галсы для формирования последовательного пути."""
    path = []

    countTack = TackList.get_lastTack().id + 1

    for i in range(countTack, 0, -1):
        if countTack == i:
            currentTack = TackList.get_tackId(0)
            path.append(currentTack.line)
        if currentTack.connectFlag == 0:
            currentPoint = Point(currentTack.line.coords[-1])
        elif currentTack.connectFlag == 1:
            currentPoint = Point(currentTack.line.coords[0])
        elif currentTack.connectFlag == -1:
            currentPoint = Point(currentTack.line.coords[-1])
            currentTack.connectFlag = 0

        min_id, min_distance, nearest_point = currentTack.get_id_mostNear(currentPoint)

        if min_id == -1: continue
        
        mostNearTack = currentTack.get_tackId(min_id)
        mostNearTack.connectFlag = nearest_point

        if nearest_point: nextPoint = Point(mostNearTack.line.coords[-1])
        else: nextPoint = Point(mostNearTack.line.coords[0])
        connectLine = LineString([currentPoint, nextPoint])

        path.append(connectLine)
        path.append(currentTack.line)

        currentTack = mostNearTack
    path.append(currentTack.line)
    return path


def coverage_path_planning_algorithm(zona_research, distance):
    # Создаем экземпляр фигуры и оси
    fig, ax = plt.subplots()

    # Настройка пределов осей
    ax.set_xlim(min(x for x, y in zona_research) - 1, max(x for x, y in zona_research) + 1)
    ax.set_ylim(min(y for x, y in zona_research) - 1, max(y for x, y in zona_research) + 1)
    ax.grid(True)

    # Создаем многоугольник с помощью массива вершин
    polygon = Polygon(zona_research, closed=True, fill=None, edgecolor='b')

    # Добавляем многоугольник на оси
    ax.add_patch(polygon)

    optimal_tack_set = []
    zona_research_polygon = ShapelyPolygon(zona_research)

    while zona_research_polygon.area > 0:
        tack_set = []
        coords = list(zona_research_polygon.exterior.coords)
        for edge in zip(coords, coords[1:]):
            line_segment = LineString(edge)
            if line_segment.length < 1:
                continue  # Пропускаем короткие edge

            angle = get_angle(edge) - np.pi / 2
            point = np.array(edge[0]) + get_shift(angle, distance / 2)
            line = get_straight_line(point, angle - np.pi / 2)
            cross_point_set = []

            for otherEdge in zip(coords, coords[1:]):
                otherEdge_segment = LineString(otherEdge)
                if otherEdge_segment.length < 1:
                    continue  # Пропускаем короткие edge
                cross_points = get_cross_points(line, LineString(otherEdge))
                cross_point_set.extend(cross_points)

            segments = get_segments_inside_region(cross_point_set, zona_research_polygon)
            tack_set.extend(segments)

        vector_criterion = {}
        for tack in tack_set:
            remain_region = get_subtraction(zona_research_polygon, get_cover_rectangle(tack))
            greed_criterion = zona_research_polygon.area - remain_region.area
            remain_region = remove_micro_polygons(remain_region)
            econom_criterion = zona_research_polygon.length / remain_region.length if remain_region.length != 0 else 1
            vector_criterion[tack] = greed_criterion * econom_criterion

        if vector_criterion:
            optimal_tack = find_maximum(vector_criterion)
            x, y = optimal_tack.xy
            ax.plot(x, y, 'k')
            zona_research_polygon = get_subtraction(zona_research_polygon, get_cover_rectangle(optimal_tack))
            zona_research_polygon = remove_micro_polygons(zona_research_polygon)

            if optimal_tack_set == []: TackList = Tack(optimal_tack)
            else: TackList.append(optimal_tack)
        
            optimal_tack_set.append(optimal_tack)
        else:
            zona_research_polygon = ShapelyPolygon()
    
    path = link_tacks_sequentially(TackList)
    plot_paths(path,plt,ax)
    return path


# vertices1 = [(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)]
vertices2 = [(2, 18), (8, 19), (14, 15), (17, 8), (5, 3)]
# vertices3 = [(1, 6), (4, 18), (10, 20), (16, 15), (18, 7)]
# vertices4 = [(3, 12), (7, 18), (14, 19), (18, 11), (12, 6)]
# vertices5 = [(2, 8), (8, 18), (12, 20), (16, 12), (6, 5)]

gs = 1

# path = coverage_path_planning_algorithm(vertices1, gs)
path = coverage_path_planning_algorithm(vertices2, gs)
# path = coverage_path_planning_algorithm(vertices3, gs)
# path = coverage_path_planning_algorithm(vertices4, gs)
# path = coverage_path_planning_algorithm(vertices5, gs)
