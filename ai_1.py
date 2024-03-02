import random
from matplotlib import pyplot as plt
from collections import deque
from time import time
from termcolor import colored

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

    # resets the grid as it was original
    def reset_grid(self):
        for i in range(self.D):
            for j in range(self.D):
                # if it's a captain, it doesn't need changing so we continue
                if self.grid[i][j].captain:
                    continue

                # i need to check if it's a wall
                # alien, bot, wall and captain have the 'open' property set to False
                if all([not self.grid[i][j].open, not self.grid[i][j].alien, not self.grid[i][j].bot]):
                    continue

                self.grid[i][j].path = False
                self.grid[i][j].walked = False
                self.grid[i][j].alien = False
                self.grid[i][j].bot = False
                self.grid[i][j].open = True

        self.grid[self.bot_start[0]][self.bot_start[1]].bot = True
        for alien_row, alien_col in self.alien_pos:
            self.grid[alien_row][alien_col].alien = True

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
    def shortest_path_function(self, bot_start = None, captain = None):
        if bot_start == None:
            bot_start = self.bot_start
        if captain == None:
            captain = self.captain

        self.path = []
        q = deque()
        q.append(bot_start)
        prev = {bot_start: bot_start}
        visited = {}
        reached = False
        
        while q:
            start_x, start_y = q[0]
            q.popleft()
            visited[(start_x, start_y)] = 1

            # adjacent = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1)]
            adjacent = self.get_neighbors(start_x, start_y)
            for child_x, child_y in adjacent:
                if (child_x, child_y) == captain:
                    reached = True
                    prev[(child_x, child_y)] = (start_x, start_y)
                    break

                if (child_x, child_y) not in visited:
                    if self.grid[child_x][child_y].alien == False and self.grid[child_x][child_y].open:
                        q.append((child_x, child_y))
                        prev[(child_x, child_y)] = (start_x, start_y)
                        visited[(child_x, child_y)] = 1

            if reached:
                break
        
        # what if there's no path?
        if reached == False:
            print("no path...")
            print(f"captain : {captain}")
            return
        
        self.path.append(captain)
        row, col = prev[captain]
        while (row, col) != bot_start:
            self.path.append((row, col))
            self.grid[row][col].path = True
            self.grid[row][col].open = True
            row, col = prev[(row, col)]

        self.path.append(self.bot_start)
        self.path = self.path[::-1]
        
    # moves the bot
    def move_bot(self, row, col, curr_row, curr_col):       
        self.grid[row][col].bot = True
        self.grid[row][col].open = False

        # the index that the bot moved from
        self.grid[curr_row][curr_col].bot = False
        self.grid[curr_row][curr_col].open = True
        self.grid[curr_row][curr_col].walked = True # just for the visuals
    
    # moves the aliens
    def move_aliens(self, put_buffer = False, alien_pos = None):
        if alien_pos == None:
            alien_pos = self.alien_pos

        random.shuffle(alien_pos)
        for i, shuffled in enumerate(alien_pos):
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
                return True

            # it didn't run into a bot
            self.grid[x][y].alien = True
            self.grid[x][y].open = False

            self.grid[alien_row][alien_col].alien = False
            self.grid[alien_row][alien_col].open = True

            alien_pos[i] = (x, y)

        if put_buffer == True:
            neighbor_cells = []
            neighbor_cells.append((row, col) for x, y in self.alien_pos for row, col in self.get_neighbors(x, y))

            for neighbor_row, neighbor_col in neighbor_cells:
                self.grid[neighbor_row][neighbor_col].alien = True
            
    # clears the path drawn by the shortest path function
    def clear_path(self):
        for i in range(self.D):
            for j in range(self.D):
                self.grid[i][j].path = False

    # moves bot 1
    def move_bot_1(self):
        t = 0
        bot_1_path_counter = 1
        ded = False
        self.shortest_path_function()
        
        curr_row, curr_col = self.bot_start

        while t < 1000:
            t += 1
            # exists = True if len(self.path) > 0 else False
            exists = len(self.path) > 0
            row, col = self.path[bot_1_path_counter] if exists else self.bot_start
            
            if exists:
                # i need to move the bot according to the path here
                if self.grid[row][col].alien:
                    return self.reached_captain, t
                elif self.grid[row][col].captain:
                    self.reached_captain = True
                    return self.reached_captain, t

                # the index that the bot moves to
                self.move_bot(row, col, curr_row, curr_col)

                bot_1_path_counter += 1
                curr_col, curr_row = col, row

            else:
                self.shortest_path_function()

            # move the aliens
            random.shuffle(self.alien_pos)
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
            
        # the bot simply survived and didn't find the captain
        return self.reached_captain, t

    # moves bot 2
    def move_bot_2(self):
        self.reached_captain = False
        t = 0
        curr_row, curr_col = self.bot_start
        row, col = self.bot_start

        while t < 1000 and (row, col) != self.captain:
            t += 1
            self.clear_path()
            self.shortest_path_function((curr_row, curr_col))
            row, col = self.path[1] if len(self.path) > 1 else (curr_row, curr_col)
            exists = len(self.path) > 0

            # move the bot
            if exists:
                if self.grid[row][col].alien:
                    return self.reached_captain, t
                elif self.grid[row][col].captain:
                    self.reached_captain = True
                    return self.reached_captain, t
                self.move_bot(row, col, curr_row, curr_col)
                
                curr_col, curr_row = col, row
            
            # move the aliens
            if self.move_aliens():
                return self.reached_captain, t
            
            self.print_grid()
            print("\n\n")

        return self.reached_captain, t

    # move bot 3
    def move_bot_3(self):
        t = 0
        curr_row, curr_col = self.bot_start
        row, col = self.bot_start
        
        # since the alien_pos list is going to be changing and we don't know if we're going to be successful with this strat,
        # let's put the original alien_pos in another list in case we want to run the bot 2 strat instead
        alien_pos = self.alien_pos[:]

        while t < 1000 and (row, col) != self.captain:
            # a list containing positions of aliens and their neighboring cells (nsew)
            # neighbor_cells = self.alien_pos[:]
            neighbor_cells = []
            neighbor_cells.append((row, col) for x, y in alien_pos for row, col in self.get_neighbors(x, y))

            # set the neighboring cells as aliens as well, cause you might as well
            # makes the shortest path function handling a bit better
            for neighbor_row, neighbor_col in neighbor_cells:
                self.grid[neighbor_row][neighbor_col].alien = True

            self.find_shortest_path()
            t += 1
            exists = len(self.path) > 0
            row, col = self.path[1] if exists else (curr_row, curr_col)

            # move the bot
            if exists:
                if self.grid[row][col].alien:
                    return self.reached_captain, t
                elif self.grid[row][col].captain:
                    self.reached_captain = True
                    return self.reached_captain, t
                self.move_bot(row, col, curr_row, curr_col)

                curr_col, curr_row = col, row

            # undo the neighbors, move the aliens, do the neighbors, check for death
            for neighbor_row, neighbor_col in neighbor_cells:
                self.grid[neighbor_row][neighbor_col].alien = False

            if self.move_aliens(True, alien_pos):
                return self.reached_captain, t

        # if we're here, it either means that t > 1000 or we died
        # so we just do what bot 2 did
        self.reset_grid()
        
        return self.move_bot_2()

    # moves bot 4
    def move_bot_4(self):
        min_dist = 3 # D // 6
        buffer = 1 # int((D // 10) * (log10(D) / log10(1000)))

        # neighbor_cells = [(x, y) for row, col in self.alien_pos for x, y in self.get_neighbors(row, col, buffer)]
        # bot 4 still follows a bfs kinda path, so we use the same code over here as the other bots
        t = 0
        lookout = len(self.alien_pos) // 3 # 3 is an arbitrary number we choose here
        curr_row, curr_col = self.bot_start
        row, col = self.bot_start

        alien_pos = self.alien_pos[:]

        def evasion_strategy(some_closest_aliens):
            mean_x, mean_y = 0, 0
            for _, x, y in some_closest_aliens:
                mean_x += x
                mean_y += y
            
            mean_x /= len(some_closest_aliens)
            mean_y /= len(some_closest_aliens)

            # now go in the opposite direction while using the captains position to modify it,
            # so that we don't move too far away from the dude
            # also offset it by the captains direction
            final_x, final_y = ((-mean_x + self.captain[0]) // 2, (-mean_y + self.captain[1]) // 2)
            if not self.is_valid(final_x, final_y):
                final_x = 0 if final_x < 0 else (self.D if final_x > self.D else final_x)
                final_y = 0 if final_y < 0 else (self.D if final_y > self.D else final_y)
            return (final_x, final_y)

        while t < 1000 and (row, col) != self.captain:
            t += 1
            destination = self.captain
            some_closest_aliens = []

            # now let's find the manhattan distance and we only look at it if its 'close enough'
            bot_x, bot_y = self.bot_start
            temp = [(abs(bot_x - x) + abs(bot_y - y), x, y) for x, y in alien_pos]
            if len(temp) > 0:
                temp.sort()
                some_closest_aliens = [(dist, x, y) for dist, x, y in temp if dist <= min_dist][:lookout]
            
            # so the bot moves one step towards its new direction until the aliens are far away from it
            if len(some_closest_aliens) == lookout:
                # find the general "direction" of these bots and move away from them
                # that's kind of just the average of their positions in the opposite direction
                destination = evasion_strategy(some_closest_aliens)

            # get neighbor cells for the aliens
            # i added this bit after getting the man.dist because the alien buffer might give us too many values
            # and i didn't want that, i just need the alien to avoid the buffer which the shortest path can do
            neighbor_cells = []
            neighbor_cells.append((row, col) for x, y in alien_pos for row, col in self.get_neighbors(x, y))

            for neighbor_row, neighbor_col in neighbor_cells:
                self.grid[neighbor_row][neighbor_col].alien = True
            
            self.shortest_path_function((curr_row, curr_col), destination)
            exists = len(self.path) > 0

            if exists:
                if self.grid[row][col].alien:
                    return self.reached_captain, t
                elif self.grid[row][col].captain:
                    self.reached_captain = True
                    return self.reached_captain, t
                self.move_bot(row, col, curr_row, curr_col)
                
                curr_col, curr_row = col, row

            # remove the alien buffers to move them
            for neighbor_row, neighbor_col in neighbor_cells:
                self.grid[neighbor_row][neighbor_col].alien = False
            # the killing of the bot is taken care of by the function
            if self.move_aliens(True, alien_pos):
                return self.reached_captain, t
        
        return self.reached_captain, t

grid = Grid(10)
grid.gen_grid(5)
bot1 = Bot(grid)

bot1.shortest_path_function()
bot1.print_grid()
print("\n\n")
bot1.reset_grid()
bot1.print_grid()

# print("now we start moving...", end="\n\n")
# bot1.move_bot_2()
# print("resetting the grid...", end="\n\n")
# grid.reset_grid()
# bot1.print_grid()
