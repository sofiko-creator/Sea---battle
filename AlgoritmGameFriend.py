import random

class AlgoritmGameFriend:

    def __init__(self):
        self.player1_field = [['-' for _ in range(12)] for _ in range(12)]
        self.player2_field = [['-' for _  in range(12)] for _  in range(12)]
        self.fill_the_map(self.player1_field)
        self.fill_the_map(self.player2_field)
       

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
 
    
    def make_move(self, field, x, y):
        if field[x][y] == '■':  # Если на клетке есть корабль
            field[x][y] = 'X'    # Отметить попадание
            if self.check_victory(field):
                return "Попадание! Вы выиграли!"
            else:
                return "Попадание!"
        else:
            field[x][y] = '*'    # Отметить промах
            return "Промах"

    def check_victory(self, field):
        for row in field:
            if '■' in row:
                return False
        return True
    
    def display_player1_field(self):
        return self.player1_field
    
    def display_player2_field(self):
        return self.player2_field
         