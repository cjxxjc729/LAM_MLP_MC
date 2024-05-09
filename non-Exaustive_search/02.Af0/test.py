#!/public1/home/sch0149/deepmd-kit/bin/python


matrix_dict = {(i, j): 0 for i in range(5) for j in range(5)}

# To access or modify the value at a specific location, for example, at row 2, column 3:
matrix_dict[(2, 3)] = 1  # Set the value at row 2, column 3 to 1

# To print the entire dictionary:
print(matrix_dict)

# If you want to display it in a more matrix-like format:
for i in range(5):
    for j in range(5):
        print(matrix_dict[(i, j)], end=' ')
    print()  # Move to the next line after printing each row

