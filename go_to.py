import math
from yawControl import YawControl
import numpy as np
import matplotlib.pyplot as plt
from coveragePathPlanningAlgorithm import coverage_path_planning_algorithm



class   GoToPoint:
    def __init__(self, position, speed, tolerance, transfer_function_model, plt):
        self.position = position  # Текущая позиция [x, y]
        self.speed = speed  # Текущая скорость
        self.flagExecute = 0 # флаг работы АНПА
        self.tolerance = tolerance
        self.transfer_function_model = transfer_function_model
        self.current_yaw = -2  # Текущий курс
        self.point = 0
        self.plt = plt



    def move_to_waypoint(self, waypoint):
        # Определение вектора направления
        direction_vector = [waypoint[i] - self.position[i] for i in range(2)]

        # Определение дистанции        
        distance = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)
        
        # Нормализация вектора направления
        if distance > self.tolerance:
            direction_vector = [direction_vector[i] / distance for i in range(2)]
        else:
            direction_vector = [0,0]

        # Вычисление необходимого курса и скорости
        desired_yaw = self.calculate_yaw(direction_vector)
        desired_speed = self.calculate_speed(distance)
        
        # Отправка команд в модель курса
        self.update_course(desired_yaw)
        dx = desired_speed * math.cos(self.current_yaw)
        dy = desired_speed * math.sin(self.current_yaw)
        self.position[0] += dx
        self.position[1] += dy
        self.plot_current_position(self.position[0],self.position[1], 'g+')

    def calculate_yaw(self, direction_vector):
        yaw = math.atan2(direction_vector[1], direction_vector[0])
        return yaw
    

    def calculate_speed(self, distance):
        return min(self.speed, distance)
    
    def update_course(self, desired_yaw):
        # Определение ошибки курса
        yaw_error = desired_yaw - self.current_yaw

        # Используем передаточную функцию для вычисления корректировки курса
        time_span = np.linspace(0, 1, 100)  # Временной интервал для моделирования
        yaw_response = self.transfer_function_model.get_response(yaw_error, time_span)

        # Обновляем текущий курс на основе отклика передаточной функции
        self.current_yaw += yaw_response  # Используем последний элемент отклика 

    def plot_current_position(self, x, y, type = 'bo'):
        self.plt.plot(x, y, type)
        self.plt.pause(0.001)  # Пауза для обновления графика

    
    def at_point(self, point):
        return sum((self.position[i] - point[i])**2 for i in range(2))**0.5 < self.tolerance

    def get_position(self):
        # метод создания запроса к БСО
        self.position
        return 

    def start_mission(self, point):
        self.flagExecute = 1
        self.point = point
        self.plot_current_position(point[0], point[1])
        self.move_to_waypoint(point)
        # цикл: пока АНПА не достигнет точки назначения
        while not self.at_point(point): 
            # Обновление позиции
            # self.get_position()
            # Поддержание курса
            self.move_to_waypoint(point)
        self.flagExecute = 0

tf_model = YawControl()

# vertices1 = [(5, 10), (10, 15), (20,  20), (15, 5), (1, 1)]
# vertices2 = [(2, 18), (8, 19), (14, 15), (17, 8), (5, 3)]
# vertices3 = [(1, 6), (4, 18), (10, 20), (16, 15), (18, 7)]
# vertices4 = [(3, 12), (7, 18), (14, 19), (18, 11), (12, 6)]
# vertices5 = [(2, 8), (8, 18), (12, 20), (16, 12), (6, 5)]
vertices6 = [(3, 15), (7, 18), (8, 12), (14, 13), (16, 14), (19, 12), (10, 4), (4,2)]

gs = 1
path, points, plt = coverage_path_planning_algorithm(vertices6, gs)
auv = GoToPoint([2, 14], 0.5, 0.1, tf_model, plt)

for waypoint in points:
    auv.start_mission([waypoint[0],waypoint[1]])
