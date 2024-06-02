import math
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

class TransferFunctionModel:
    def __init__(self, K1, K_omega, Kc, T, xi):
        self.K_Omega = K1 * K_omega * Kc
        self.T = T
        self.xi = xi
        self.transfer_function = self.create_transfer_function()
        
    def create_transfer_function(self):
        numerator = [self.K_Omega]
        denominator = [self.T**2, 2*self.T*self.xi, 1, 0]
        Wp = ctrl.TransferFunction(numerator, denominator)
        Wcl = ctrl.feedback(Wp, 1)
        return Wcl
    
    def get_response(self, error, time_span):
        _, response = ctrl.forced_response(self.transfer_function, T=time_span, U=error)
        return response[-1]  # Возвращаем последнее значение отклика

class GoToPoint:
    def __init__(self, position, speed, tolerance, transfer_function_model):
        self.position = np.array(position, dtype=float)  # Убедитесь, что элементы позиции являются числами с плавающей запятой
        self.speed = speed  # Текущая скорость
        self.flagExecute = 0  # Флаг работы АНПА
        self.tolerance = tolerance
        self.transfer_function_model = transfer_function_model
        self.current_yaw = 0  # Текущий курс
        self.positions = [self.position.copy()]  # Сохранение траектории

    def move_to_waypoint(self, waypoint):
        # Определение вектора направления
        direction_vector = np.array(waypoint) - self.position

        # Определение дистанции        
        distance = np.linalg.norm(direction_vector)

        # Нормализация вектора направления
        if distance > self.tolerance:
            direction_vector /= distance
        else:
            direction_vector = np.zeros_like(direction_vector)

        # Вычисление необходимого курса и скорости
        desired_yaw = self.calculate_yaw(direction_vector)
        desired_speed = self.calculate_speed(distance)

        # Обновление курса с учетом передаточной функции
        self.update_course(desired_yaw)

        # Обновление позиции
        self.position += desired_speed * np.array([math.cos(self.current_yaw), math.sin(self.current_yaw)])
        self.positions.append(self.position.copy())

        # plt.plot(self.position[0], self.position[1], 'bo')
        self.plot_trajectory(self.position)


    def calculate_yaw(self, direction_vector):
        # Пример расчета курса на основе вектора направления
        yaw = math.atan2(direction_vector[1], direction_vector[0])
        return yaw

    def calculate_speed(self, distance):
        # Пример расчета скорости на основе дистанции до точки
        return min(self.speed, distance)
    
    def at_point(self, point):
        return np.linalg.norm(self.position - np.array(point)) < self.tolerance

    def get_position(self):
        return self.position

    def start_mission(self, point):
        self.flagExecute = 1
        self.move_to_waypoint(point)
        # Цикл: пока АНПА не достигнет точки назначения
        while not self.at_point(point): 
            # Обновление позиции
            self.move_to_waypoint(point)
        self.flagExecute = 0
        self.plot_trajectory(point)

    def update_course(self, desired_yaw):
        # Определение ошибки курса
        yaw_error = desired_yaw - self.current_yaw

        # Используем передаточную функцию для вычисления корректировки курса
        time_span = np.linspace(0, 1, 100)  # Временной интервал для моделирования
        yaw_response = self.transfer_function_model.get_response(yaw_error, time_span)

        # Обновляем текущий курс на основе отклика передаточной функции
        self.current_yaw += yaw_response  # Используем последний элемент отклика как новый курс

    def plot_trajectory(self, target_point):
        plt.figure()
        plt.plot(target_point[0], target_point[1], 'ro', label='Целевая точка')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Траектория движения АНПА')
        plt.legend()
        plt.grid()
        plt.show()

# Пример создания экземпляра класса TransferFunctionModel
K1 = 1
K_omega = 1
Kc = 1
T = 1
xi = 0.5
tf_model = TransferFunctionModel(K1, K_omega, Kc, T, xi)

# Создание экземпляра класса GoToPoint и запуск миссии
anpa = GoToPoint([0, 0], 1, 0.1, tf_model)
anpa.start_mission([10, 10])