import random
from matplotlib import pyplot as plt
from collections import deque
from time import time

class Grid:
    def __init__(self, D) -> None:
        self.D = D
        self.grid = []

    # checks if the index is valid
    def is_valid(self, row, col):
        return (0 <= row < self.D) and (0 <= col < self.D)
    
    # gets all the adjacent cells (not including the given position)
    def get_neighbors(self, row, col, buffer = 1):
        l = []
        for i in range(buffer):
            l.append([(row - i, col), (row + i, col), (row, col - i), (row, col + i)])

        neighbor = [n for n in l if self.is_valid(n[0], n[1], self.D)]
        return neighbor
    
    def print_grid(self):
        for col in self.grid:
            for block in col:
                print(block)
            print()

    
