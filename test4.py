# Экспериментальные исследования.
# Тест №4.

from yawControl import YawControl
from go_to import GoToPoint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from coveragePathPlanningAlgorithm import coverage_path_planning_algorithm
import os


tf_model = YawControl()

speed = 0.02
tolerance = 0.5
debug = 0

distance = 1

poligons = []
poligons.append([(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)])
poligons.append([(2, 18), (8, 19), (14, 15), (17, 8), (5, 3)])
poligons.append([(1, 6), (4, 18), (10, 20), (16, 15), (18, 7)])
poligons.append([(3, 12), (7, 18), (14, 19), (18, 11), (12, 6)])
poligons.append([(2, 8), (8, 18), (12, 20), (16, 12), (6, 5)])
poligons.append([(3, 15), (7, 18), (8, 14), (14, 13), (16, 14), (19, 12), (10, 4), (4,2)])

positions = []
positions.append([20, 24])
positions.append([2, 20])
positions.append([0, 5])
positions.append([2, 14])
positions.append([18, 14])
positions.append([3, 18])
id = 0

for poligon, position in zip(poligons, positions):

    id = id + 1

    points, ax = coverage_path_planning_algorithm(poligon, distance)

    # настройка графика 
    fig = ax.get_figure()
    fig.set_size_inches(10, 10)

    ax.grid(True, which='both', linestyle='--', linewidth=1.5)
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)
    nameplt = f'Покрытие области {id}'
    ax.set_title(nameplt, fontsize=16)

    id_pol = 0
    auv = GoToPoint(position, speed, tolerance, tf_model, plt, debug)
    for waypoint in points:
        id_pol += 1
        # зону удержания для целевой точки
        circle = Circle((waypoint[0], waypoint[1]), tolerance, color='#b00000', fill=False, linewidth=1)
        plt.gca().add_patch(circle)
        auv.start_mission([waypoint[0],waypoint[1]])

        namefileplt = f'photos/finalPLOT/exp3/poligon_4_{id}/poligon_cpp_{id}_id_{id_pol}_{waypoint}.png'
        
        # Получение директории из имени файла
        directory = os.path.dirname(namefileplt)
        
        # Проверка и создание директории, если она не существует
        if not os.path.exists(directory):
            os.makedirs(directory)

        plt.savefig(namefileplt, dpi=300, bbox_inches='tight')

    # plt.pause(1)
    plt.clf()
plt.show()

