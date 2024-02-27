def is_valid(i, j, D):
    return (0 <= i < D) and (0 <= j < D)

def get_neighbors(row, col):
    l = [(row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    neighbor = [n for n in l if is_valid(n[0], n[1], 30)]
    return neighbor

print(get_neighbors(3, 4))