import random
from matplotlib import pyplot as plt
from collections import deque
from time import time
from termcolor import colored, cprint

class Grid_Status:
    def __init__(self) -> None:
        self.open = False
        self.alien = False
        self.captain = False
        self.bot = False
        self.path = False
        self.walked = False

    def __str__(self):
        output = ""
        if self.alien:
            output += colored("A", "red")
        elif self.captain:
            output += colored("C", "blue")
        elif self.bot:
            output += colored("B", "yellow")
        elif self.open:
            output += colored(".", "dark_grey")
        elif self.open == False:
            output += colored("#", "white")
        elif self.path:
            output += colored("#", "light_cyan")
        elif self.walked:
            output += colored("#", "green")
        
        return output

class Grid:
    def __init__(self, D) -> None:
        self.D = D
        self.grid = [[Grid_Status() for row in range(self.D)] for col in range(self.D)]
        self.alien_pos = []
        self.captain = None
        self.bot_start = None

    # checks if the index is valid
    def is_valid(self, row, col):
        return (0 <= row < self.D) and (0 <= col < self.D)
    
    # gets all the adjacent cells (not including the given position)
    def get_neighbors(self, row, col, buffer = 1):
        l = []
        for i in range(1, buffer + 1):
            l.extend([(row - i, col), (row + i, col), (row, col - i), (row, col + i)])

        neighbor = [(x, y) for x, y in l if self.is_valid(x, y)]
        return neighbor
    
    # just prints the grid out
    def print_grid(self):
        for col in self.grid:
            for block in col:
                print(block, end="")
            print()

    def move_stuff(self, thing, location):
        pass

    # choose a random opening
    def choose_random_open(self):
        row, col = random.randint(0, self.D - 1), random.randint(0, self.D - 1)

        while self.grid[row][col].open == False or self.grid[row][col].alien \
            or self.grid[row][col].captain or self.grid[row][col].bot:
            row, col = random.randint(0, self.D - 1), random.randint(0, self.D - 1)

        return (row, col)

    def gen_grid(self, k):
        # generate the iterative part of the grid
        self.grid[random.randint(0, self.D - 1)][random.randint(0, self.D - 1)].open = True
        while True:
            one_neighbor = []
            for i in range(len(self.grid)):
                for j in range(len(self.grid)):
                    if self.grid[i][j].open:
                        continue

                    count = 0
                    neighbors = self.get_neighbors(i, j)
                    for x, y in neighbors:
                        if self.grid[x][y].open:
                            count += 1

                    # exactly one open neighbor
                    if count == 1:
                        one_neighbor.append((i, j))

            if len(one_neighbor) == 0:
                break

            row, col = random.choice(one_neighbor)
            self.grid[row][col].open = True


        # now for the dead ends
        dead_end = []
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if self.grid[i][j].open == False:
                    continue

                count = 0
                neighbors = self.get_neighbors(i, j)
                for row, col in neighbors:
                    if self.grid[row][col].open:
                        count += 1
                
                if count == 1:
                    dead_end.append((i, j))

        # remove half of the dead ends
        random.shuffle(dead_end)
        dead_end = dead_end[len(dead_end) // 2 :]

        for row, col in dead_end:
            neighbors = self.get_neighbors(row, col)
            closed_walls = []

            for x, y in neighbors:
                if self.grid[x][y].open == False:
                    closed_walls.append((x, y))

            if len(closed_walls) == 0:
                continue

            closed_x, closed_y = random.choice(closed_walls)
            self.grid[closed_x][closed_y].open = True

        bot_start = self.choose_random_open()
        self.grid[bot_start[0]][bot_start[1]].bot = True
        self.grid[bot_start[0]][bot_start[1]].open = False
        self.bot_start = bot_start

        # alien positions now
        for i in range(k):
            row, col = self.choose_random_open()
            self.grid[row][col].alien = True
            self.alien_pos.append((row, col))

        # captain position
        row, col = self.choose_random_open()
        self.grid[row][col].captain = True
        self.grid[row][col].open = False
        self.captain = (row, col)

        self.print_grid()


grid = Grid(10)

grid.gen_grid(5)
print("called gen_grid")
        
