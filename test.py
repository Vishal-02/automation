import random
from queue import Queue

def generate_grid_with_bot_aliens_and_captain(D, num_aliens):
    grid = [['blocked' for _ in range(D)] for _ in range(D)]
    
    # Place bot
    start_row, start_col = random.randint(1, D-2), random.randint(1, D-2)
    grid[start_row][start_col] = 'open'
    bot_position = (start_row, start_col)

    # Place aliens
    for _ in range(num_aliens):
        alien_row, alien_col = random.randint(1, D-2), random.randint(1, D-2)
        while grid[alien_row][alien_col] != 'blocked':
            alien_row, alien_col = random.randint(1, D-2), random.randint(1, D-2)
        grid[alien_row][alien_col] = 'alien'

    # Place Captain
    captain_row, captain_col = random.randint(1, D-2), random.randint(1, D-2)
    while grid[captain_row][captain_col] != 'blocked':
        captain_row, captain_col = random.randint(1, D-2), random.randint(1, D-2)
    grid[captain_row][captain_col] = 'captain'

    return grid, bot_position, (captain_row, captain_col)

def move_bot(grid, bot_position, captain_position, strategy):
    if strategy == 1:
        return move_bot_strategy_1(grid, bot_position, captain_position)
    elif strategy == 2:
        return move_bot_strategy_2(grid, bot_position, captain_position)
    elif strategy == 3:
        return move_bot_strategy_3(grid, bot_position, captain_position)

def move_bot_strategy_1(grid, bot_position, captain_position):
    # Bot plans the shortest path to the Captain, ignoring aliens' movement
    path = shortest_path_to_captain(grid, bot_position, captain_position)
    return path[1] if len(path) > 1 else bot_position  # Move to the next cell in the path, or stay in place

def move_bot_strategy_2(grid, bot_position, captain_position):
    # Bot re-plans the shortest path to the Captain at every time step, avoiding current alien positions
    path = shortest_path_to_captain(grid, bot_position, captain_position)
    return path[1] if len(path) > 1 else bot_position  # Move to the next cell in the path, or stay in place

def move_bot_strategy_3(grid, bot_position, captain_position):
    # Bot re-plans the shortest path to the Captain, avoiding current alien positions and adjacent cells
    path = shortest_path_to_captain_avoiding_adjacent(grid, bot_position, captain_position)
    if len(path) > 1:
        return path[1]  # Move to the next cell in the path
    else:
        # Resort to Bot 2 behavior if there is no path avoiding adjacent cells
        path = shortest_path_to_captain(grid, bot_position, captain_position)
        return path[1] if len(path) > 1 else bot_position  # Move to the next cell in the path, or stay in place

def shortest_path_to_captain(grid, start, end):
    # Find the shortest path using BFS
    queue = Queue()
    visited = set()
    parent = {}

    queue.put(start)
    visited.add(start)

    while not queue.empty():
        current = queue.get()

        if current == end:
            path = []
            while current in parent:
                path.insert(0, current)
                current = parent[current]
            path.insert(0, start)
            return path

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []

def shortest_path_to_captain_avoiding_adjacent(grid, start, end):
    # Find the shortest path avoiding adjacent cells
    queue = Queue()
    visited = set()
    parent = {}

    queue.put(start)
    visited.add(start)

    while not queue.empty():
        current = queue.get()

        if current == end:
            path = []
            while current in parent:
                path.insert(0, current)
                current = parent[current]
            path.insert(0, start)
            return path

        for neighbor in get_neighbors_avoiding_adjacent(grid, current):
            if neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []

def get_neighbors(grid, position):
    i, j = position
    possible_moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    return [(x, y) for x, y in possible_moves if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] in {'open', 'captain', 'blocked'}]

def get_neighbors_avoiding_adjacent(grid, position):
    i, j = position
    possible_moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    return [(x, y) for x, y in possible_moves if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] in {'open', 'captain', 'blocked'} and not is_adjacent_to_aliens(grid, (x, y))]

def is_adjacent_to_aliens(grid, position):
    i, j = position
    for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 'alien':
            return True
    return False

def move_aliens(grid, aliens_order):
    random.shuffle(aliens_order)
    for alien_position in aliens_order:
        move_alien(grid, alien_position)

def move_alien(grid, position):
    i, j = position
    possible_moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] in {'open', 'captain'}]
    if valid_moves:
        new_position = random.choice(valid_moves)
        grid[i][j] = 'open'
        grid[new_position[0]][new_position[1]] = 'alien'

# Simulate multiple instances and calculate success rates
def simulate_multiple_instances(num_instances, D, num_aliens, strategy):
    success_save_captain = 0
    success_survival = 0

    for _ in range(num_instances):
        grid, bot_position, captain_position = generate_grid_with_bot_aliens_and_captain(D, num_aliens)
        aliens_order = [(i, j) for i in range(1, D-1) for j in range(1, D-1) if grid[i][j] == 'alien']
        random.shuffle(aliens_order)
        flag = False

        for _ in range(1000):  # Maximum of 1000 time steps
            bot_position = move_bot(grid, bot_position, captain_position, strategy)

            if bot_position == captain_position and grid[bot_position[0]][bot_position[1]] != 'alien':
                success_save_captain += 1
                flag = True
                break

            move_aliens(grid, aliens_order)

        if not flag:  # Executed if the loop completes without a 'break', i.e., bot did not save the Captain
            success_survival += 1

    return success_save_captain / num_instances, success_survival / num_instances

# Example usage
num_instances = 100
D = 30
num_aliens = 5

# Evaluate Bot 1
success_rate_save_captain_1, success_rate_survival_1 = simulate_multiple_instances(num_instances, D, num_aliens, 1)
print("Bot 1:")
print(f"Success rate of saving the Captain: {success_rate_save_captain_1 * 100:.2f}%")
print(f"Success rate of bot survival: {success_rate_survival_1 * 100:.2f}%")

# Evaluate Bot 2
success_rate_save_captain_2, success_rate_survival_2 = simulate_multiple_instances(num_instances, D, num_aliens, 2)
print("\nBot 2:")
print(f"Success rate of saving the Captain: {success_rate_save_captain_2 * 100:.2f}%")
print(f"Success rate of bot survival: {success_rate_survival_2 * 100:.2f}%")

# Evaluate Bot 3
success_rate_save_captain_3, success_rate_survival_3 = simulate_multiple_instances(num_instances, D, num_aliens, 3)
print("\nBot 3:")
print(f"Success rate of saving the Captain: {success_rate_save_captain_3 * 100:.2f}%")
print(f"Success rate of bot survival: {success_rate_survival_3 * 100:.2f}%")
