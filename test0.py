import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

vertices = [(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)]
gs = 0.9

# Создаем экземпляр фигуры и оси
fig, ax = plt.subplots()

# Настройка пределов осей
ax.set_xlim(min(x for x, y in vertices) - 1, max(x for x, y in vertices) + 1)
ax.set_ylim(min(y for x, y in vertices) - 1, max(y for x, y in vertices) + 1)

ax.grid(True)

# Создаем многоугольник с помощью массива вершин
polygon = Polygon(vertices, closed=True, fill=None, edgecolor='b')

# Добавляем многоугольник на оси
ax.add_patch(polygon)