import math

class   GoToPoint:
    def __init__(self, position, speed, tolerance):
        self.position = position  # Текущая позиция [x, y]
        self.speed = speed  # Текущая скорость
        self.flagExecute = 0 # флаг работы АНПА
        self.tolerance = tolerance

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
        self.model.update_course(desired_yaw)
        self.model.update_speed(desired_speed)

    def calculate_yaw(self, direction_vector):
        # Пример расчета курса на основе вектора направления
        yaw = math.atan2(direction_vector[1], direction_vector[0])
        return yaw

    def calculate_speed(self, distance):
        # Пример расчета скорости на основе дистанции до точки
        return min(self.speed, distance)
    
    def at_point(self, point):
        return sum((self.position[i] - point[i])**2 for i in range(2))**0.5 < self.tolerance

    def get_position(self):
        # метод создания запроса к БСО
        self.position
        return 

    def start_mission(self, point):
        self.flagExecute = 1
        self.move_to_waypoint(point)
        # цикл: пока АНПА не достигнет точки назначения
        while not self.at_point(point): 
            # Обновление позиции
            self.get_position()
            # Поддержание курса
            self.move_to_waypoint(point)
        self.flagExecute = 0