import math
import numpy as np



class   GoToPoint:
    def __init__(self, position, speed, tolerance, transfer_function_model, plt, debug):
        self.position = position  # Текущая позиция [x, y]
        self.speed = speed  # Текущая скорость
        self.flagExecute = 0 # флаг работы АНПА
        self.tolerance = tolerance
        self.transfer_function_model = transfer_function_model
        self.current_yaw = -math.pi/2  # Текущий курс
        self.desired_yaw = self.current_yaw
        self.point = 0
        self.plt = plt
        self.rotates = 0
        self.debug = debug

    def move_to_waypoint(self, waypoint):
        # Определение вектора направления
        direction_vector = [waypoint[i] - self.position[i] for i in range(2)]
        print("start")
        print("direction_vector =", direction_vector)

        # Определение дистанции        
        distance = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)
        print("distance =", distance)


        # Нормализация вектора направления
        if distance > self.tolerance:
            direction_vector = [direction_vector[i] / distance for i in range(2)]
        else:
            direction_vector = [0,0]

        # Вычисление необходимого курса и скорости
        
        self.desired_yaw = self.calculate_yaw(direction_vector, self.desired_yaw)
        desired_speed = self.calculate_speed(distance)
        print("desired_yaw =", self.desired_yaw)

        # Отправка команд в модель курса
        self.update_course(self.desired_yaw)
        dx = desired_speed * math.cos(self.current_yaw)
        dy = desired_speed * math.sin(self.current_yaw)
        self.position[0] += dx
        self.position[1] += dy
        self.plot_current_position(self.position[0], self.position[1], color = '#ffb28b', marker = '.', markersize=1)
        print("current_yaw =", self.current_yaw)
        print("finish")



    def calculate_yaw(self, direction_vector, prev_yaw):
        yaw = math.atan2(direction_vector[1], direction_vector[0])
        print("yaw =", yaw)
        print("prevyaw =", prev_yaw)


        quadrant = self.find_quadrant(self.position, self.point)
        print("quadrant =", quadrant)

        c = 0
        if prev_yaw - self.rotates *2*math.pi > 0.1*math.pi and yaw < -0.1*math.pi:
            self.rotates+=1;
        elif prev_yaw - self.rotates *2*math.pi < -0.1*math.pi and yaw > 0.1*math.pi:
            self.rotates-=1; 
        
        print("self.rotates =", self.rotates)
        c= self.rotates *2*math.pi
        yaw = yaw + c
        return yaw
    
    def find_quadrant(self, point1, point2):
        dx, dy = point2[0] - point1[0], point2[1] - point1[1]
        
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 3
        elif dx > 0 and dy < 0:
            return 4
        else:
            return None  # Точка лежит на одной из осей или совпадает с начальной точкой
    

    def calculate_speed(self, distance):
        yaw_error = self.desired_yaw - self.current_yaw
        speed = self.speed - (self.speed / math.pi) * abs(yaw_error)
        # b = (-self.speed -abs(math.pi)**2)/math.pi
        # speed = abs(yaw_error)**2 + b*abs(yaw_error) + self.speed
        print("speed =", speed)
        print("         yaw_error =", yaw_error)

        if speed < 0 : speed = 0.001

        return speed
    
    def update_course(self, desired_yaw):
        # Определение ошибки курса
        yaw_error = desired_yaw - self.current_yaw

        # Используем передаточную функцию для вычисления корректировки курса
        time_span = np.linspace(0, 1, 100)  # Временной интервал для моделирования
        yaw_response = self.transfer_function_model.get_response(yaw_error, time_span)

        # Обновляем текущий курс на основе отклика передаточной функции
        self.current_yaw += yaw_response  # Используем последний элемент отклика 

    def plot_current_position(self, x, y, color, marker = 'o', markersize = 1):
        self.plt.plot(x, y, color, marker = marker, markersize = markersize)
        if self.debug:
            self.plt.pause(0.01)  # Пауза для обновления графика

    
    def at_point(self, point):
        return sum((self.position[i] - point[i])**2 for i in range(2))**0.5 < self.tolerance

    def get_position(self):
        # метод создания запроса к БСО
        self.position
        return 

    def start_mission(self, point):
        self.flagExecute = 1
        self.point = point
        self.plot_current_position(point[0], point[1], color = '#b00000')
        self.move_to_waypoint(point)
        # цикл: пока АНПА не достигнет точки назначения
        while not self.at_point(point): 
            # Обновление позиции
            # self.get_position()
            # Поддержание курса
            self.move_to_waypoint(point)
        self.flagExecute = 0
