test = [1, 2, 3, 4, 5]

another = [element for element in test]

test[1] = 100

print(another, test)