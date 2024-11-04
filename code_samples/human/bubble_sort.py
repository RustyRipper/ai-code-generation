def bubble(values):
    length = len(values) - 1
    sorted = False
    while not sorted:
        sorted = True
        for element in range(0,length):
            if values[element] > values[element + 1]:
                 hold = values[element + 1]
                 values[element + 1] = values[element]
                 values[element] = hold
                 sorted = False
    return values
