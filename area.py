import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from grid import Grid
from pathPlanning_easy import PathPlanning_easy

class Area:
    def __init__(self, vertices, gs, grid_size):
        self.vertices = vertices
        self.gs = gs
        self.grid_size = grid_size
        
        self.create_area()

    def create_area(self):
        """
        Построение многоугольника и сетки на одном графике.
    
        Параметры:
        vertices (list of tuples): Массив вершин многоугольника в формате [(x1, y1), (x2, y2), ..., (xn, yn)]
        grid_size (int): Размер сетки
        
        Возвращает:
        None
        """
        # Создаем экземпляр фигуры и оси
        fig, ax = plt.subplots()
        
        # Настройка пределов осей
        ax.set_xlim(min(x for x, y in self.vertices) - 1, max(x for x, y in self.vertices) + 1)
        ax.set_ylim(min(y for x, y in self.vertices) - 1, max(y for x, y in self.vertices) + 1)
        
        # Рисуем сетку
        for i in range(self.grid_size+1):
            ax.axhline(y = i * self.gs, color='k', linestyle='-')
            ax.axvline(x = i * self.gs, color='k', linestyle='-')
        ax.grid(True)

        gridPoint = []
        for y in range(self.grid_size + 1):
            row = []
            for x in range(self.grid_size + 1):
                row.append(Grid(plt, self.vertices, x * self.gs, y * self.gs))
                # plt.plot(x * self.gs, y * self.gs, 'ro')
            gridPoint.append(row)

        PathPlanning_easy(gridPoint, plt, self.grid_size)            
            
        
        # Создаем многоугольник с помощью массива вершин
        polygon = Polygon(self.vertices, closed=True, fill=None, edgecolor='b')
        
        # Добавляем многоугольник на оси
        ax.add_patch(polygon)

        from datetime import datetime
        import os
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"my_plot_{current_time}.png"
        file_path = os.path.join(".", file_name)  # Замените "путь_к_папке_с_файлами" на путь к вашей папке

        # Сохранение графика в файл
        plt.savefig(file_path)


        # Показываем график
        plt.show()
        