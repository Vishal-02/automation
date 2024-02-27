import random
from queue import Queue

# checks whether or not the coordinates are out of bounds
def is_valid(i, j, D):
    return (0 <= i < D) and (0 <= j < D)
    
# prints grid
def print_grid(grid):
    for col in grid:
        for block in col:
            print(block, end=" ")
        print("")

# finds the shortest path from the bot to the captain (using bfs)
def find_shortest_path(grid, bot_start, captain, new_alien=[]):
    q = Queue()
    q.put(bot_start)
    prev = {bot_start: bot_start}
    reached_captain = False
    visited = {}

    while not q.empty():
        start_x, start_y = q.get()
        visited[(start_x, start_y)] = 0

        adjacent = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1)]
        for child_x, child_y in adjacent:
            if is_valid(child_x, child_y, len(grid[0])) and (child_x, child_y) not in visited:
                if grid[child_x][child_y] not in ['X', 'A'].append(new_alien):
                    q.put((child_x, child_y))
                    prev[(child_x, child_y)] = (start_x, start_y)
                
                    if (child_x, child_y) == captain:
                        reached_captain = True
                        break
        
        if reached_captain:
            break
    
    # what if there's no path?
    if reached_captain == False:
        return False, {}
    
    path = [captain]
    row, col = prev[captain]
    while (row, col) != bot_start:
        path.append((row, col))
        grid[row][col] = 'Z'
        row, col = prev[(row, col)]

    return True, path[::-1]

# take a guess
def move_alien(grid, alien_pos, i):
    D = len(grid[0])
    adj = [0, -1, 0, 1, 0]
    y, x = alien_pos[i]
    possible_moves = []

    for mod in range(4):
        new_y, new_x = y + adj[mod], x + adj[mod + 1]
        if is_valid(new_y, new_x, D) and grid[new_y][new_x] not in ['X', 'A']:
            possible_moves.append((new_y, new_x))

    new_y, new_x = random.choice(possible_moves)
    grid[y][x] = '.'
    if grid[new_y][new_x] == 'B':
        grid[new_y][new_x] = 'A'
        return True
    alien_pos[i] = (new_y, new_x)

# moves bot 1
def move_bot_1(grid, bot_start, alien_pos, captain):
    t = 0
    ded = False
    exists, path = find_shortest_path(grid, bot_start, captain)
    if not exists:
        print("the path does not exist")
        return t
    
    curr_row, curr_col = bot_start
    row, col = path[0]

    while t < 1000 and (row, col) != captain:
        t += 1
        row, col = path[t]

        if grid[row][col] == 'A':
            print("bot ran into the alien, it ded")
            ded = True
            break
        
        # move the bot
        grid[curr_row][curr_col] = '.'
        grid[row][col] = 'B'
        curr_col, curr_row = col, row

        # move the aliens
        random.shuffle(alien_pos)
        for i in range(len(alien_pos)):
            did_it_kill = move_alien(grid, alien_pos, i)
            if did_it_kill == True:
                print("alien ran into bot and killed it, bot ded")
                ded = True
                break

    if not ded and (row, col) == captain:
        print(f"captain saved!! in {t} steps!!")
    return t

# time for bot 2
def move_bot_2(grid, bot_start, alien_pos, captain):
    exists, path = find_shortest_path(grid, bot_start)
    t = 0
    ded = False
    curr_row, curr_col = bot_start

    while t < 1000 and (row, col) != captain:
        if not exists:
            print("The path does not exist")
            return t
        t += 1
        row, col = path[1]

        # move the bot
        if grid[row][col] == 'A':
            print("bot ran into the alien, it ded")
            ded = True
            break

        grid[curr_row][curr_col] = '.'
        grid[row][col] = 'B'
        curr_col, curr_row = col, row

        # move the aliens
        random.shuffle(alien_pos)
        for i in range(len(alien_pos)):
            did_it_kill = move_alien(grid, alien_pos, i)
            if did_it_kill == True:
                print("alien ran into bot and killed it, bot ded")
                ded = True
                break
        
        exists, path = find_shortest_path(grid, (row, col), captain)

    if not ded and (row, col) == captain:
        print(f"captain saved!! in {t} steps!!")
    return t

# creates the grid
def grid_creator(grid, num_aliens, D):
    alien_pos = []

    while True:
        one_neighbor = []
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                if (grid[i][j] == '.'):
                    continue

                count = 0
                neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                for x, y in neighbors:
                    if is_valid(x, y, D) and grid[x][y] == '.':
                        count += 1

                # exactly one open neighbor
                if count == 1:
                    one_neighbor.append((i, j))

        if len(one_neighbor) == 0:
            break

        x, y = random.choice(one_neighbor)
        grid[x][y] = '.'

    dead_end = []
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if grid[i][j] == 'X':
                continue

            count = 0
            neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            for x, y in neighbors:
                if is_valid(x, y, D) and grid[x][y] == '.':
                    count += 1
            
            if count == 1:
                dead_end.append((i, j))
    
    # now we randomly eliminate half of these
    org_len = len(dead_end)
    while len(dead_end) > (org_len / 2):
        choice = random.choice(dead_end)
        dead_end.remove(choice)

    for row, col in dead_end:
        neighbors = []
        neigh_val = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]

        for new_row, new_col in neigh_val:
            if is_valid(new_row, new_col, D) and grid[new_row][new_col] == 'X':
                neighbors.append((new_row, new_col))
        
        if not neighbors:
            continue

        try:
            i, j = random.choice(neighbors)
            grid[i][j] = '.'
        except Exception as e:
            print(e)
            print(f"i: {i}, j: {j}")
            print(neighbors)

    # chooses a random open spot
    def choose_random_open(var = False):
        include = []
        if not var:
            include = ['.']
        else: include = ['.', 'A']

        row, col = random.randint(0, D - 1), random.randint(0, D - 1)
        while grid[row][col] not in include:
            # print(f"row: {row}, col: {col}, grid: {grid[row][col]}")
            row, col = random.randint(0, D - 1), random.randint(0, D - 1)
        return (row, col)
    
    # get the starting position of the bot
    bot_start = choose_random_open()
    grid[bot_start[0]][bot_start[1]] = 'B'

    # randomly insert the aliens
    for i in range(num_aliens):
        row, col = choose_random_open()
        grid[row][col] = 'A'
        alien_pos.append((row, col))

    # insert the captain in any spot that's not the bot
    captain_row, captain_col = choose_random_open(True)
    grid[captain_row][captain_col] = 'C'

    return bot_start, alien_pos, (captain_row, captain_col)

# let's do bot 3
def move_bot_3(grid, bot_start, alien_pos, captain):
    # we're going to be adding the buffer to the aliens by simply adding their adjacent cells to the alien_pos list
    buff_aliens = [] # these are the cells adj to the aliens that we'll give to the shortest path algo

    def get_neighbors(row, col):
        l = [(row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        neighbor = [n for n in l if is_valid(n[0], n[1], len(grid[0]))]
        return neighbor
    
    # a list containing positions of aliens and their neighboring cells (nsew)
    neighbor_cells = [(row, col) for x, y in alien_pos for row, col in get_neighbors(x, y) if is_valid(row, col, len(grid[0]))]

    # now we need to get the shortest path with these new 'aliens'
    exists, path = find_shortest_path(grid, bot_start, captain)
    t = 0
    ded = False
    curr_row, curr_col = bot_start

    while t < 1000 and (row, col) != captain:
        if not exists:
            print("The path does not exist")
            return t
        t += 1
        row, col = path[1]

        # move the bot
        if grid[row][col] == 'A':
            print("bot ran into the alien, it ded")
            ded = True
            break

        grid[curr_row][curr_col] = '.'
        grid[row][col] = 'B'
        curr_col, curr_row = col, row

        # move the aliens
        random.shuffle(alien_pos)
        for i in range(len(alien_pos)):
            did_it_kill = move_alien(grid, alien_pos, i)
            if did_it_kill == True:
                print("alien ran into bot and killed it, bot ded")
                ded = True
                break
        
        # since the aliens moved, there's new alien positions and hence new adjacent cells as well. so we recalculate
        neighbor_cells = [(row, col) for x, y in alien_pos for row, col in get_neighbors(x, y) if is_valid(row, col, len(grid[0]))]
        path = find_shortest_path(grid, (row, col), captain, neighbor_cells)


    

def main():
    D = 30 # dimension of the grid
    k = 4 # number of aliens
    grid = [['X' for _ in range(D)] for _ in range(D)]

    start_row, start_col = random.randint(0, D - 1), random.randint(0, D - 1)
    print(f"origin x: {start_row}, origin y: {start_col}")
    grid[start_col][start_row] = '.'

    bot_start, alien_pos, captain = grid_creator(grid, k, D)
    print_grid(grid)
    print()
    find_shortest_path(grid, bot_start, captain)
    print_grid(grid)
    # t = move_bot_1(grid, bot_start, captain)
    # print(t)

if __name__ is '__main__':
    main()