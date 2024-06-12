# Экспериментальные исследования.
# Тест №3.

import matplotlib.pyplot as plt
from coveragePathPlanningAlgorithm import coverage_path_planning_algorithm
import os



distance = 1.5

poligons = []
poligons.append([(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)])
poligons.append([(2, 18), (8, 19), (14, 15), (17, 8), (5, 3)])
poligons.append([(1, 6), (4, 18), (10, 20), (16, 15), (18, 7)])
poligons.append([(3, 12), (7, 18), (14, 19), (18, 11), (12, 6)])
poligons.append([(2, 8), (8, 18), (12, 20), (16, 12), (6, 5)])
poligons.append([(3, 15), (7, 18), (8, 14), (14, 13), (16, 14), (19, 12), (10, 4), (4,2)])

id = 0

for poligon in poligons:

    id += 1

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

    namefileplt = f'photos/finalPLOT/exp3/poligon_5/poligon_cpp_{id}_distance_{distance}.png'
    
    # Получение директории из имени файла
    directory = os.path.dirname(namefileplt)
    
    # Проверка и создание директории, если она не существует
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(namefileplt, dpi=300, bbox_inches='tight')

    # plt.pause(1)
    plt.clf()
    # plt.show()

