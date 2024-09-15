import math

def calculate_optimal_node_size(size_of_node):
    return math.ceil(4 * size_of_node / 64) + 1

#print(calculate_optimal_node_size(int(input())))
