#!/public1/home/sch0149/deepmd-kit/bin/python


import json
import numpy as np


# Load the JSON data from the file
with open("./final_Af_matrix.json", "r") as file:
    data = json.load(file)

# Extract the matrix dimensions from the keys
max_row, max_col = 0, 0
for key in data.keys():
    row, col = map(int, key.strip('()').split(', '))
    max_row = max(max_row, row)
    max_col = max(max_col, col)

# Initialize the matrix with zeros
matrix = [[0] * (max_col + 1) for _ in range(max_row + 1)]

# Populate the matrix with the data
for key, value in data.items():
    row, col = map(int, key.strip('()').split(', '))
    matrix[row][col] = 100*value

for i in range(len(matrix)):
    for j in range(i + 1, len(matrix[i])):
        avg = (matrix[i][j] + matrix[j][i]) / 2
        matrix[i][j] = avg
        matrix[j][i] = avg

np.savetxt('Af_matrix.txt',matrix,fmt='%.3f')

