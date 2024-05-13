

class PathPlanning_easy:
    def __init__(self, gridPoint, plt, grid_size):
        self.gridPoint = gridPoint
        self.plt = plt
        self.grid_size = grid_size
        
        self.searchNextPoint()

    def searchNextPoint(self):
        lastPoint = 0
        
        for x in range(self.grid_size + 1):

            if x % 2 == 0:  # если x чётное
                print("start for")
                for y in range(self.grid_size + 1):
                    print("y =", y)
                    if self.gridPoint[y][x].state == 1:
                        if lastPoint:
                            self.plt.plot([self.gridPoint[y][x].coord_x, lastPoint.coord_x], 
                                [self.gridPoint[y][x].coord_y, lastPoint.coord_y], 
                                color='green', linewidth=5)
                            print("lastPoint=", lastPoint)
                            lastPoint = 0

                        if self.gridPoint[y-1][x].state == 1:
                            self.plt.plot([self.gridPoint[y][x].coord_x, self.gridPoint[y][x].coord_x], 
                                [self.gridPoint[y][x].coord_y, self.gridPoint[y - 1][x].coord_y], 
                                color='green', linewidth=5)
                            if self.gridPoint[y+1][x].state == 0 and lastPoint == 0:
                                lastPoint = self.gridPoint[y][x]
                print("finish for")

            else:  # если x нечётное
                print("start reverse for")
                for y in reversed(range(self.grid_size + 1)):
                    print("y=", y)

                    if self.gridPoint[y][x].state == 1:
                        if lastPoint:
                            self.plt.plot([self.gridPoint[y][x].coord_x, lastPoint.coord_x], 
                                [self.gridPoint[y][x].coord_y, lastPoint.coord_y], 
                                color='green', linewidth=5)
                            print("lastPoint=", lastPoint)
                            lastPoint = 0

                        if self.gridPoint[y+1][x].state == 1:
                            self.plt.plot([self.gridPoint[y][x].coord_x, self.gridPoint[y][x].coord_x], 
                                [self.gridPoint[y][x].coord_y, self.gridPoint[y + 1][x].coord_y], 
                                color='green', linewidth=5)
                            if self.gridPoint[y-1][x].state == 0:
                                lastPoint = self.gridPoint[y][x]
                print("finish reverse for")



            # for y in range(self.grid_size + 1):
            #     if self.gridPoint[y][x].state == 1 and self.gridPoint[y-1][x].state == 1:
            #         self.plt.plot([self.gridPoint[y][x].coord_x, self.gridPoint[y][x].coord_x], 
            #              [self.gridPoint[y][x].coord_y, self.gridPoint[y - 1][x].coord_y], 
            #              color='blue', linewidth=2)
            # for y in reversed(range(self.grid_size + 1)):
            #     if self.gridPoint[y][x].state == 1 and self.gridPoint[y+1][x].state == 1:
            #         self.plt.plot([self.gridPoint[y][x].coord_x, self.gridPoint[y][x].coord_x], 
            #              [self.gridPoint[y][x].coord_y, self.gridPoint[y + 1][x].coord_y], 
            #              color='blue', linewidth=2) 
                    

                    # # Рисуем линию между точками
                    # # Например, соединяем точку с предыдущей точкой по x и y
                    # if x > 0 and self.gridPoint[y][x - 1].state == 1:  # Соединяем с левой точкой, если она тоже имеет состояние 1
                    #     self.plt.plot([self.gridPoint[y][x - 1].coord_x, self.gridPoint[y][x - 1].coord_x - 1],
                    #                   [self.gridPoint[y][x - 1].coord_y, self.gridPoint[y][x - 1].coord_y], color='green',linewidth=2)
                    # if y > 0 and self.gridPoint[y - 1][x].state == 1:  # Соединяем с верхней точкой, если она тоже имеет состояние 1
                    #     self.plt.plot([self.gridPoint[y - 1][x].coord_x, self.gridPoint[y - 1][x].coord_x],
                    #                   [self.gridPoint[y - 1][x].coord_y, self.gridPoint[y - 1][x].coord_y - 1], color='green',linewidth=2)