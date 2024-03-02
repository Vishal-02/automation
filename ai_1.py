import random
from matplotlib import pyplot as plt
from collections import deque
from time import time
from termcolor import colored, cprint
# import copy

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
        elif self.walked:
            output += colored("#", "green")
        elif self.path:
            output += colored("O", "light_cyan")
        elif self.open:
            output += colored(".", "dark_grey")
        elif self.open == False:
            output += colored("#", "white")
        
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
    
    # resets the grid as it was original
    def reset_grid(self):
        for i in range(self.D):
            for j in range(self.D):
                if self.grid[i][j].open == False or self.grid[i][j].captain:
                    continue

                self.grid[i][j].path = False
                self.grid[i][j].walked = False
                self.grid[i][j].alien = False
                self.grid[i][j].bot = False
                self.grid[i][j].open = True

        self.grid[self.bot_start[0]][self.bot_start[1]].bot = True
        for alien_row, alien_col in self.alien_pos:
            self.grid[alien_row][alien_col].alien = True

    # just prints the grid out
    def print_grid(self):
        for row in self.grid:
            for block in row:
                print(block, end="")
            print()

    # let's see if i use this function at all, does nothing for now
    def move_stuff(self, thing, location):
        pass

    # choose a random opening
    def choose_random_open(self):
        row, col = random.randint(0, self.D - 1), random.randint(0, self.D - 1)

        while self.grid[row][col].open == False or self.grid[row][col].alien \
            or self.grid[row][col].captain or self.grid[row][col].bot:
            row, col = random.randint(0, self.D - 1), random.randint(0, self.D - 1)

        return (row, col)

    # creates the entire grid
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
            self.grid[row][col].open = False
            self.alien_pos.append((row, col))

        # captain position
        row, col = self.choose_random_open()
        self.grid[row][col].captain = True
        self.grid[row][col].open = False
        self.captain = (row, col)

# bots, should I make a class or just do with all the functions?
class Bot:
    def __init__(self, Grid) -> None:
        self.bot_start = Grid.bot_start
        # self.grid = copy.deepcopy(Grid.grid)
        self.grid = Grid.grid
        self.alien_pos = Grid.alien_pos[:]
        self.captain = Grid.captain
        self.D = Grid.D
        self.reached_captain = False
        self.path = []

    # just prints the grid out
    def print_grid(self):
        for col in self.grid:
            for block in col:
                print(block, end="")
            print()

    # checks if the index is valid
    def is_valid(self, row, col):
        return (0 <= row < self.D) and (0 <= col < self.D)

    # get the neighbors of a certain (row, col)
    def get_neighbors(self, row, col, buffer = 1):
        l = []
        for i in range(1, buffer + 1):
            l.extend([(row - i, col), (row + i, col), (row, col - i), (row, col + i)])

        neighbor = [(x, y) for x, y in l if self.is_valid(x, y)]
        return neighbor

    # gets the shortest path using bfs
    def shortest_path_function(self):
        q = deque()
        q.append(self.bot_start)
        prev = {self.bot_start: self.bot_start}
        visited = {}
        reached = False
        # print(f"Bot is at : {self.bot_start}")
        
        while q:
            start_x, start_y = q[0]
            q.popleft()
            visited[(start_x, start_y)] = 1

            # adjacent = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1)]
            adjacent = self.get_neighbors(start_x, start_y)
            for child_x, child_y in adjacent:
                if (child_x, child_y) == self.captain:
                    reached = True
                    prev[(child_x, child_y)] = (start_x, start_y)
                    break

                if (child_x, child_y) not in visited:
                    if self.grid[child_x][child_y].alien == False and self.grid[child_x][child_y].open:
                        q.append((child_x, child_y))
                        # print((child_x, child_y), end=" ")
                        prev[(child_x, child_y)] = (start_x, start_y)
                        visited[(child_x, child_y)] = 1

            if reached:
                break
        
        # what if there's no path?
        if reached == False:
            print("no path...")
            print(f"captain : {self.captain}")
            return
        
        self.path.append(self.captain)
        row, col = prev[self.captain]
        while (row, col) != self.bot_start:
            self.path.append((row, col))
            self.grid[row][col].path = True
            self.grid[row][col].path = True
            row, col = prev[(row, col)]

        self.path.append(self.bot_start)
        self.path = self.path[::-1]
        
    # moves bot 1
    def move_bot_1(self):
        t = 0
        bot_1_path_counter = 1
        ded = False
        
        curr_row, curr_col = self.bot_start

        while t < 1000:
            t += 1
            exists = True if len(self.path) > 0 else False
            row, col = self.path[bot_1_path_counter] if exists else self.bot_start
            
            if exists:
                # i need to move the bot according to the path here
                if self.grid[row][col].alien:
                    return self.reached_captain, t
                elif self.grid[row][col].captain:
                    self.reached_captain = True
                    return self.reached_captain, t

                # the index that the bot moves to
                self.grid[row][col].bot = True
                self.grid[row][col].open = False

                # the index that the bot moved from
                self.grid[curr_row][curr_col].bot = False
                self.grid[curr_row][curr_col].open = True
                self.grid[curr_row][curr_col].walked = True # just for the visuals

                bot_1_path_counter += 1
                curr_col, curr_row = col, row

            else:
                self.shortest_path_function()

            # move the aliens
            random.shuffle(self.alien_pos)
            print(f"aliens former position : {self.alien_pos}")
            for i, shuffled in enumerate(self.alien_pos):
                # we gotta move the aliens now, so we get the open neighbors
                alien_row, alien_col = shuffled
                possible = self.get_neighbors(alien_row, alien_col)
                possible = [(x, y) for x, y in possible \
                            if self.grid[x][y].open or self.grid[x][y].bot or self.grid[x][y].captain]

                if len(possible) == 0:
                    continue

                x, y = random.choice(possible)
                # check if it kills the bot or something
                if self.grid[x][y].bot:
                    return self.reached_captain, t
                
                # it didn't run into a bot
                self.grid[x][y].alien = True
                self.grid[x][y].open = False

                self.grid[alien_row][alien_col].alien = False
                self.grid[alien_row][alien_col].open = True

                self.alien_pos[i] = (x, y)
            
            self.print_grid()
        # the bot simply survived and didn't find the captain
        return self.reached_captain, t

grid = Grid(10)
grid.gen_grid(5)
bot1 = Bot(grid)
bot1.shortest_path_function()
bot1.print_grid()
print("now we start moving...", end="\n\n")
bot1.move_bot_1()
