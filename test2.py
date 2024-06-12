# Экспериментальные исследования.
# Тест №2. Выход в точку из точки [5,0]

from yawControl import YawControl
from go_to import GoToPoint
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

tf_model = YawControl()

speed = 0.1
tolerance = 0.2
debug = 1

waypoints = []
waypoints.append([10, 10])
waypoints.append([10, -10])
waypoints.append([-10, 10])
waypoints.append([-10, -10])

for waypoint in waypoints:
    
    # настройка графика
    plt.figure(figsize=(10, 10))
    plt.grid(True, which='both', linestyle='--', linewidth=1.5)
    plt.xlabel('X', fontsize=14)
    plt.ylabel('Y', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    nameplt = f'Движение в точку {waypoint}'
    plt.title(nameplt, fontsize=16)

    # зону удержания для целевой точки
    circle = Circle((waypoint[0], waypoint[1]), tolerance, color='#7fb5b5', fill=False, linewidth=2)
    plt.gca().add_patch(circle)

    position = [5, 0]
    auv = GoToPoint(position, speed, tolerance, tf_model, plt, debug)
    auv.start_mission(waypoint)
    # plt.show()

    # Сохранить график в файл
    namefileplt = f'photos/finalPLOT/exp2/plotGoTo_{waypoint}.png'
    plt.savefig(namefileplt, dpi=300, bbox_inches='tight')
    plt.clf()
