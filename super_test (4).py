import random
from math import log10
from matplotlib import pyplot as plt
from collections import deque
from time import time

random.seed(44)

# checks whether or not the coordinates are out of bounds
def is_valid(i, j, D):
    return (0 <= i < D) and (0 <= j < D)
    
# prints grid
def print_grid(grid):
    for col in grid:
        for block in col:
            print(block, end=" ")
        print("")

# gets neighbors
def get_neighbors(row, col, D, buffer = 1):
    if buffer > 1:
        l = [(row, col)]
        for i in range(buffer):
            l.append([(row - i, col), (row + i, col), (row, col - i), (row, col + i)])
    else:
        l = [(row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    neighbor = [n for n in l if is_valid(n[0], n[1], D)]
    return neighbor

# finds the shortest path from the bot to the captain (using bfs)
def find_shortest_path(grid, bot_start, captain, new_aliens = []):
    q = deque()
    q.append(bot_start)
    prev = {bot_start: bot_start}
    reached_captain = False
    visited = {}

    while q:
        start_x, start_y = q[0]
        q.popleft()
        visited[(start_x, start_y)] = 1

        adjacent = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1)]
        for child_x, child_y in adjacent:
            if is_valid(child_x, child_y, len(grid[0])) and (child_x, child_y) not in visited:
                if grid[child_x][child_y] not in ['X', 'A'] + new_aliens:
                    q.append((child_x, child_y))
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
    path.append(bot_start)
    
    return True, path[::-1]

# take a guess
def move_alien(grid, alien_pos, i, var = True):
    # print(f"i: {i}, alien_pos: {alien_pos}")
    D = len(grid[0])
    adj = [0, -1, 0, 1, 0]
    y, x = alien_pos[i]
    possible_moves = []

    for mod in range(4):
        new_y, new_x = y + adj[mod], x + adj[mod + 1]
        if is_valid(new_y, new_x, D) and grid[new_y][new_x] not in ['X', 'A']:
            possible_moves.append((new_y, new_x))

    new_y, new_x = random.choice(possible_moves) if len(possible_moves) > 0 else alien_pos[i]
    grid[y][x] = '.'
    alien_pos[i] = (new_y, new_x)

    if grid[new_y][new_x] == 'B':
        grid[new_y][new_x] == 'A'
        return True

    if var:
        new_aliens = [(row, col) for x, y in alien_pos for row, col in get_neighbors(x, y, D) if is_valid(row, col, D)]
        for row, col in new_aliens:
            if grid[row][col] == 'B':
                grid[new_y][new_x] == 'A'
                return True
            
    grid[new_y][new_x] == 'A'
    # print(f"i: {i}, alien_pos: {alien_pos}", end="\n\n")

    return False

# moves bot 1
def move_bot_1(grid, bot_start, alien_pos, captain):
    t = 0
    bot_1_path_counter = 0
    ded = False
    exists, path = find_shortest_path(grid, bot_start, captain)
    
    curr_row, curr_col = bot_start

    while t < 1000:
        t += 1
        bot_1_path_counter += 1
        row, col = path[bot_1_path_counter] if len(path) > 0 else bot_start
        
        if exists:
            if grid[row][col] == 'A':
                # print("bot ran into the alien, it ded")
                ded = True
                break
            
            # move the bot
            grid[curr_row][curr_col] = '.'
            grid[row][col] = 'B'
            curr_col, curr_row = col, row
        else:
            bot_1_path_counter = 1
            exists, path = find_shortest_path(grid, bot_start, captain)

        if (curr_row, curr_col) == captain:
            break

        # move the aliens
        random.shuffle(alien_pos)
        for i in range(len(alien_pos)):
            did_it_kill = move_alien(grid, alien_pos, i)
            if did_it_kill == True:
                # print("alien ran into bot and killed it, bot ded")
                ded = True
                break

    # if not ded and (curr_row, curr_col) == captain:
    #     print(f"captain saved!! in {t} steps!!")
    #     pass
    
    return [not ded, t]

# time for bot 2
def move_bot_2(grid, bot_start, alien_pos, captain):
    exists, path = find_shortest_path(grid, bot_start, captain)
    t = 0
    ded = False
    curr_row, curr_col = bot_start
    row, col = bot_start

    while t < 1000 and (row, col) != captain:
        if not exists:
            print("The path does not exist")
            return t
        t += 1
        row, col = path[1] if len(path) > 1 else path[0]

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
    return [not ded, t]

# let's create bot 3
def move_bot_3(grid, bot_start, alien_pos, captain):
    # we're going to be adding the buffer to the aliens by simply adding their adjacent cells to the alien_pos list
    D = len(grid[0])

    # a list containing positions of aliens and their neighboring cells (nsew)
    neighbor_cells = [(row, col) for x, y in alien_pos for row, col in get_neighbors(x, y, D)]

    # now we need to get the shortest path with these new 'aliens'
    exists, path = find_shortest_path(grid, bot_start, captain)
    as_we_move = [bot_start] # tracks the path as we keep moving and recalculating across the grid
    t = 0
    ded = False
    curr_row, curr_col = bot_start
    row, col = bot_start

    # since the alien_pos list is going to be changing and we don't know if we're going to be successful with this strat,
    # let's put the original alien_pos in another list in case we want to run the bot 2 strat instead
    org_alien_pos = [element for element in alien_pos]

    # since the grid also changes,
    org_grid = [element[:] for element in grid]

    while t < 1000 and (row, col) != captain:
        if not exists:
            print("The path does not exist")
            return t
        t += 1
        row, col = path[1] if len(path) > 1 else path[0]

        # move the bot
        if grid[row][col] == 'A' or (row, col) in neighbor_cells:
            print("bot ran into the alien, it ded")
            ded = True
            break

        grid[curr_row][curr_col] = '.'
        grid[row][col] = 'B'
        curr_col, curr_row = col, row
        as_we_move.append((row, col))

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
        exists, path = find_shortest_path(grid, (row, col), captain, neighbor_cells)

    if (row, col) == captain:
        print("we found the cap with the alien buffer")
        return [not ded, t]

    # if we're here, it either means that t > 1000 or we died
    # so we just do what bot 2 did
    second_t = move_bot_2(org_grid, bot_start, org_alien_pos, captain)
    return second_t

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

# let's think of something for bot 4
def move_bot_4(grid, bot_start, alien_pos, captain):
    '''
    you can increase alien buffer by a factor of grid size (D) : (a // 10) * (log10(a) / log10(1000))
    check out evasion in case of no path
    final possible addition, danger detection
    '''
    D = len(grid[0])
    min_dist = D // 6
    buffer = int((D // 10) * (log10(D) / log10(1000)))
    print("before get_neighbor")
    neighbor_cells = [(x, y) for row, col in alien_pos for x, y in get_neighbors(row, col, D, buffer)]
    print("after get_neighbor")
    # bot 4 still follows a bfs kinda path, so we use the same code over here as the other bots
    exists, path = find_shortest_path(grid, bot_start, captain)
    t = 0
    ded = False
    lookout = len(alien_pos) // 3 # 3 is an arbitrary number we choose here
    curr_row, curr_col = bot_start
    row, col = bot_start

    alien_pos_copy = [element for element in alien_pos]
    grid_copy = [element[:] for element in grid]

    def evasion_strategy(some_closest_aliens):
        mean_x, mean_y = 0, 0
        for _, x, y in some_closest_aliens:
            mean_x += x
            mean_y += y
        
        mean_x /= len(some_closest_aliens)
        mean_y /= len(some_closest_aliens)

        # now go in the opposite direction while using the captains position to modify it,
        # so that we don't move too far away from the dude

        final_x, final_y = (-mean_x, -mean_y)
        # now we offset it by the captains direction
        final_direction = (final_x + captain[0] / 2, final_y + captain[1] / 2)

        return final_direction

    def move_bot(row, col, curr_row, curr_col):
        if grid[row][col] == 'A' or (row, col) in neighbor_cells:
            print("bot ran into the alien, it ded")
            return True

        grid[curr_row][curr_col] = '.'
        grid[row][col] = 'B'
        curr_col, curr_row = col, row

    while t < 1000 and (row, col) != captain:
        print(f"t : {t}")
        if not exists:
            print("The path does not exist")
            
        t += 1
        row, col = path[1] if len(path) > 1 else (path[0] if len(path) > 0 else curr_row, curr_col)

        # now let's find the manhattan distance and we only look at it if its 'close enough'
        bot_x, bot_y = bot_start
        temp = [(abs(bot_x - x) + abs(bot_y - y), x, y) for x, y in alien_pos]
        some_closest_aliens = []

        if len(temp) > 0:
            temp.sort()
            some_closest_aliens = [(dist, x, y) for dist, x, y in temp if dist <= min_dist][:lookout]
        
        # so the bot moves one step towards its new direction until the aliens are far away from it
        if len(some_closest_aliens) == lookout:
            # find the general "direction" of these bots and move away from them
            # that's kind of just the average of their positions in the opposite direction
            final_direction = evasion_strategy(some_closest_aliens)
            if not is_valid(final_direction):
                x, y = final_direction[0], final_direction[1]
                final_direction[0] = 0 if x < 0 else (D if x > D else x)
                final_direction[1] = 0 if y < 0 else (D if y > D else y)

            # we got the direction we're supposed to be heading in for now
            print("avoiding aliens path")
            exists, path = find_shortest_path(grid, (curr_row, curr_col), final_direction, neighbor_cells)
            if not exists:
                # the bot stays still and does nothing
                pass
            else:
                move_bot(row, col, curr_row, curr_col)
        else:
            # move the bot
            ded = move_bot(row, col, curr_row, curr_col)
            if ded:
                break

        if (row, col) == captain:
            break

        # move the aliens
        random.shuffle(alien_pos)
        for i in range(len(alien_pos)):
            did_it_kill = move_alien(grid, alien_pos, i)
            if did_it_kill == True:
                print("alien ran into bot and killed it, bot ded")
                ded = True
                break
        
        if ded:
            break

        # since the aliens moved, there's new alien positions and hence new adjacent cells as well. so we recalculate
        neighbor_cells = [(row, col) for x, y in alien_pos for row, col in get_neighbors(x, y, D, buffer)]
        exists, path = find_shortest_path(grid, (row, col), captain, neighbor_cells)

    if (row, col) == captain:
        print("we found the cap with the extra alien buffer")
        return [not ded, t]
    else: 
        print("survived...")
        return [ded, t]


# the main function
def main():
    D = 30 # dimension of the grid

    runs = 50
    k_val = range(5, 31, 5)  
    val = 0
    
    #success_counts_bot1 = []
    #success_counts_bot2 = []
    #success_counts_bot3 = []
    success_counts_bot4 = []

    start_time = time()
    for k in k_val:
       # success_count_bot1 = 0
       # success_count_bot2 = 0
        #success_count_bot3 = 0
        success_count_bot4 = 0
        
        for _ in range(runs):
            val += 1
            print(f"val : {val}")
            grid = [['X' for _ in range(D)] for _ in range(D)]
            start_row, start_col = random.randint(0, D - 1), random.randint(0, D - 1)
            grid[start_col][start_row] = '.'
            bot_start, alien_pos, captain = grid_creator(grid, k, D)
            
            #success_bot1, _ = move_bot_1(grid, bot_start, alien_pos, captain)
            #success_bot2, _ = move_bot_2(grid, bot_start, alien_pos, captain)
            #success_bot3 = move_bot_3(grid, bot_start, alien_pos, captain)
            success_bot4, _ = move_bot_4(grid, bot_start, alien_pos, captain)

            #if success_bot1:
             #   success_count_bot1 += 1
            #if success_bot2:
             #   success_count_bot2 += 1
            #if success_bot3:
              #  success_count_bot3 += 1
            if success_bot4:
                success_count_bot4 += 1

        #success_counts_bot1.append(success_count_bot1 / runs)
        #success_counts_bot2.append(success_count_bot2 / runs)
        #success_counts_bot3.append(success_count_bot3 / runs)
        success_counts_bot4.append(success_count_bot4 / runs)
    end_time = time()

    print(f"time taken : {end_time - start_time}, val : {val}")
    
    plt.figure(figsize=(10, 6))

    #plt.plot(k_val, success_counts_bot1, label = 'Bot 1', color = 'blue')
    #plt.plot(k_val, success_counts_bot2, label = 'Bot 2', color = 'red')
    #plt.plot(k_val, success_counts_bot3, label = 'Bot 3', color = 'yellow')
    plt.plot(k_val, success_counts_bot4, label = 'Bot 4', color = 'pink')
    
    plt.xlabel('Number of Aliens')
    plt.ylabel('Success Rate')
    plt.title(f"Bots : {runs} runs")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()