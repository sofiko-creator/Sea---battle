import random

class AlgoritmGame:

    def __init__(self):
        self.size = 10
        self.player_field = []
        self.player_field = [['-' for _ in range(12)] for _ in range(12)]
        self.bot_field = []
        self.bot_field = [['-' for _  in range(12)] for _  in range(12)]
        self.fill_the_map(self.player_field)
        self.ships_info_player = []
        self.ships_info_player = self.find_ships_on_field(self.player_field)
        self.fill_the_map(self.bot_field)
        self.ships_info_bot = []
        self.ships_info_bot = self.find_ships_on_field(self.bot_field)
        self.hits = []  # Список координат, по которым были сделаны попадания
        self.misses = []
        self.last_hit_coordinates = None 
        self.bot_direction = None  # Направление бота
        self.last_hit_direction = None
        self.initial_hit_coordinates = {}
        self.direction = (0, 0) 

    def fill_the_map(self, field):
        self.place_ship(field, 4)  # Линкор (4 клетки)
        self.place_ship(field, 3)  # Крейсера (3 клетки)
        self.place_ship(field, 3)  # Крейсера (3 клетки)
        self.place_ship(field, 2)  # Эсминцы (2 клетки)
        self.place_ship(field, 2)  # Эсминцы (2 клетки)
        self.place_ship(field, 2)  # Эсминцы (2 клетки)
        self.place_ship(field, 1)  # Торпедные катера (1 клетка)
        self.place_ship(field, 1)  # Торпедные катера (1 клетка)
        self.place_ship(field, 1)  # Торпедные катера (1 клетка)
        self.place_ship(field, 1)  # Торпедные катера (1 клетка)
            
            
    def place_ship(self, field, size):

        position = random.randint(0, 1) # 0 - Horizontal 1 - Vertical
        is_cell_enable = False
        if (position == 0): # 0 - Horizontal
   
            while (is_cell_enable != True):
                x = random.randint(1, 10 - size + 1)
                y = random.randint(1, 10)
                for i in range(0, size, 1):
                    is_cell_enable = self.are_neighbors_empty(x + i, y, field)
                    if (is_cell_enable == False):
                        break
                if (is_cell_enable == True):
                    for i in range(0, size, 1):
                        field[x + i][y] = '■'           
        else: # 1 - Vertical
            while (is_cell_enable != True):
                x = random.randint(1, 10)
                y = random.randint(1, 10 - size + 1)
                for i in range(0, size, 1):
                    is_cell_enable = self.are_neighbors_empty(x, y + i, field)
                    if (is_cell_enable == False):
                        break
                if (is_cell_enable == True):
                    for i in range(0, size, 1):
                        field[x][y + i] = '■'
            
    def are_neighbors_empty(self, x, y, field):
        if (field[x][y] == '■'):
            return False
        if (field[x][y-1] == '■'):
            return False
        if (field[x][y+1] == '■'):
            return False
        if (field[x-1][y] == '■'):
            return False
        if(field[x+1][y] == '■'): 
            return False
        if (field[x+1][y-1] == '■'):
            return False
        if (field[x+1][y+1] == '■'):
            return False
        if (field[x-1][y-1] == '■'):
            return False 
        if (field[x-1][y+1] == '■'):
            return False
        return True
    

    def find_ships_on_field(self, field):
        ships = []
        visited = set()

        for x in range(1, 11): 
            for y in range(1, 11):
                if field[x][y] == '■' and (x, y) not in visited:
                    # Определение ориентации корабля
                    orientation = 'vertical' if x + 1 < 11 and field[x + 1][y] == '■' else 'horizontal'
                    ship_size = 1  # Корабль как минимум уже 1 клетка
                    visited.add((x, y))

                    if orientation == 'horizontal': 
                        ny = y + 1
                        while ny < 11 and field[x][ny] == '■':
                            ship_size += 1
                            visited.add((x, ny))
                            ny += 1
                    else:  # Вертикальное направление
                        nx = x + 1
                        while nx < 11 and field[nx][y] == '■':
                            ship_size += 1
                            visited.add((nx, y))
                            nx += 1

                    ships.append({'start': (x, y), 'size': ship_size, 'orientation': orientation})

        return ships

    def is_ship_sunk_after_hit(self, hit_x, hit_y):
        # Перебираем все корабли бота, чтобы найти, к какому кораблю принадлежит попадание
        for ship in self.ships_info_bot:
            ship_cells = []
            # Генерируем клетки корабля на основе его начальных координат, размера и ориентации
            if ship['orientation'] == 'vertical':
                ship_cells = [(ship['start'][0] + i, ship['start'][1]) for i in range(ship['size'])]
              
            else:  # 'vertical'
                ship_cells = [(ship['start'][0], ship['start'][1] + i) for i in range(ship['size'])]

            # Если попадание принадлежит этому кораблю, проверяем все его клетки на попадание
            if (hit_x, hit_y) in ship_cells:
                # Проверяем, все ли клетки корабля подбиты
                if all(self.bot_field[x][y] == 'X' for x, y in ship_cells):
                    return True  # Корабль потоплен
        return False  # Корабль не потоплен

    def is_ship_sunk_after_hit_player(self, field, hit_x, hit_y):
        # Перебираем все корабли игрока, чтобы найти, к какому кораблю принадлежит попадание
        for ship in self.ships_info_player:
            ship_cells = []
            # Генерируем клетки корабля на основе его начальных координат, размера и ориентации
            if ship['orientation'] == 'vertical':
                ship_cells = [(ship['start'][0] + i, ship['start'][1]) for i in range(ship['size'])]
              
            else:  # 'vertical'
                ship_cells = [(ship['start'][0], ship['start'][1] + i) for i in range(ship['size'])]

            # Если попадание принадлежит этому кораблю, проверяем все его клетки на попадание
            if (hit_x, hit_y) in ship_cells:
                # Проверяем, все ли клетки корабля подбиты
                if all(field[x][y] == 'X' for x, y in ship_cells):
                    return True  # Корабль потоплен

        return False  # Корабль не потоплен


    def update_board_after_sink(self, field, x, y):
        # Получаем координаты только подбитых клеток
        for ship in self.ships_info_bot:
            ship_cells = []
            if ship['orientation'] == 'vertical':
                ship_cells = [(ship['start'][0] + i, ship['start'][1]) for i in range(ship['size'])]
            else:  # Горизонтальное расположение
                ship_cells = [(ship['start'][0], ship['start'][1] + i) for i in range(ship['size'])]

            if (x, y) in ship_cells:
                if all(field[i][j] == 'X' or field[i][j] == 'S' for i, j in ship_cells):
                    for i, j in ship_cells:
                        if field[i][j] != 'S':
                            field[i][j] = 'S'
                    
                    # Обновляем соседние клетки корабля и их окружение (*)
                    for i, j in ship_cells:
                        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < len(field) and 0 <= nj < len(field[0]):
                                if field[ni][nj] != 'X' and field[ni][nj] != 'S':
                                    field[ni][nj] = '*'
                    return

                
    def update_player_board_after_sink(self, field, x, y):
    # Получаем координаты только подбитых клеток
        for ship in self.ships_info_player:
            ship_cells = []
            if ship['orientation'] == 'vertical':
                ship_cells = [(ship['start'][0] + i, ship['start'][1]) for i in range(ship['size'])]
            else: 
                ship_cells = [(ship['start'][0], ship['start'][1] + i) for i in range(ship['size'])]

            if (x, y) in ship_cells:
                if all(field[i][j] == 'X' or field[i][j] == 'S' for i, j in ship_cells):
                    for i, j in ship_cells:
                        if field[i][j] != 'S':
                            field[i][j] = 'S'
                    
                         # Обновляем соседние клетки корабля и их окружение (*)
                    for i, j in ship_cells:
                        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < len(field) and 0 <= nj < len(field[0]):
                                if field[ni][nj] != 'X' and field[ni][nj] != 'S':
                                    field[ni][nj] = '*'
                                    self.misses.append((ni, nj))
                    return


    def make_move(self, field, x, y):
        if field[x][y] == '■':  # Если на клетке есть корабль
            field[x][y] = 'X'    # Отметить попадание
            self.hits.append((x, y))
            self.last_hit_coordinates = (x, y)

            if self.check_victory(field):
                return "Попадание! Вы выиграли!"
            else:
                if self.is_ship_sunk_after_hit_player(field,x, y) or self.is_ship_sunk_after_hit(x, y):
                        if self.is_ship_sunk_after_hit_player(field, x, y):
                            self.update_player_board_after_sink(field, x, y)
                            return "Попадание и корабль потоплен!"
                        elif self.is_ship_sunk_after_hit(x, y):
                            self.update_board_after_sink(field, x, y)
                            return "Попадание и корабль потоплен!"

                return "Попадание!"
        else:
            if field[x][y] != 'S' and field[x][y] != 'X':
                field[x][y] = '*'    # Отметить промах
            self.misses.append((x, y))
            return "Промах"


    def get_ship_coordinates(self, field, x, y):
        ship_coordinates = []
        queue = [(x, y)]

        while queue:
            current_x, current_y = queue.pop(0)

            if (current_x, current_y) not in ship_coordinates:
                ship_coordinates.append((current_x, current_y))

                for i, j in self.get_neighboring_coordinates(current_x, current_y):
                    if field[i][j] == '■' and (i, j) not in queue:
                        queue.append((i, j))

        print("Ship coordinates:", ship_coordinates)  # Отладочное сообщение
        return ship_coordinates

    def check_victory(self, field):
        for row in field:
            if '■' in row:
                return False
        return True
    
    def display_player_field(self):
        return self.player_field
    
    def display_enemy_field(self):
        return self.bot_field

    def generate_random_move(self):
        move = (random.randint(1, 10), random.randint(1, 10))
        while not self.is_move_valid(move):
            move = (random.randint(1, 10), random.randint(1, 10))
        return move

    def get_neighboring_coordinates(self, x, y):
        neighbors = []
        for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 1 <= i <= 10 and 1 <= j <= 10:
                neighbors.append((i, j))
        return neighbors


    def update_last_hit_coordinates(self, x, y):
        self.last_hit_coordinates = (x, y)

    def get_bot_next_move(self):
        if self.last_hit_coordinates:
            # Проверяем, определено ли направление для продолжения атаки
            if self.bot_direction:
                next_move = (self.last_hit_coordinates[0] + self.bot_direction[0],
                            self.last_hit_coordinates[1] + self.bot_direction[1])

                if self.is_move_valid(next_move):
                    return next_move
                else:
                    # Смена направления на противоположное, если следующий ход невозможен
                    opposite_direction = (-self.bot_direction[0], -self.bot_direction[1])
                    # Пытаемся сделать ход в противоположном направлении от последнего успешного попадания
                    next_move = (self.last_hit_coordinates[0] + opposite_direction[0],
                                self.last_hit_coordinates[1] + opposite_direction[1])
                    if self.is_move_valid(next_move):
                        # Обновляем направление на противоположное
                        self.bot_direction = opposite_direction
                        return next_move
                    else:
                        # Возврат к исходной точке после атаки всего корабля в текущем направлении
                        self.bot_direction = None
                        self.last_hit_coordinates = self.initial_hit_coordinates
                        return self.get_bot_next_move()  # Повторный вызов метода для начала атаки в противоположном направлении

            # Поиск новой соседней клетки для атаки, если направление не было определено или сброшено
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_move = (self.last_hit_coordinates[0] + direction[0], 
                            self.last_hit_coordinates[1] + direction[1])
                if self.is_move_valid(next_move):
                    # Устанавливаем новое направление атаки
                    self.bot_direction = direction
                    return next_move
                
        return self.generate_random_move()

    def is_move_valid(self, move):
        x, y = move
        is_within_bounds = 1 <= x <= self.size and 1 <= y <= self.size
        is_not_previously_attempted = move not in self.hits and move not in self.misses
        return is_within_bounds and is_not_previously_attempted