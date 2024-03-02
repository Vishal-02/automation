dead_end = [1, 2, 3, 4, 5, 6, 7]
test = dead_end[:]
dead_end[-1] = 1000
test[0] = -200

print(test)
print(dead_end)