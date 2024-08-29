# Example flat list representing a 3D matrix with dimensions 2x3x4
matrix_3d = [
    1, 2, 3, 4,   # layer 1, row 1
    5, 6, 7, 8,   # layer 1, row 2
    9, 10, 11, 12, # layer 1, row 3
    13, 14, 15, 16, # layer 2, row 1
    17, 18, 19, 20, # layer 2, row 2
    21, 22, 23, 24  # layer 2, row 3
]

# Dimensions of the 3D matrix
X = 2  # number of layers
Y = 3  # number of rows per layer
Z = 4  # number of elements per row

# Iterate through the 3D matrix
for i in range(X):
    for j in range(Y):
        for k in range(Z):
            # Calculate the index in the flat list
            index = i * Y * Z + j * Z + k
            value = matrix_3d[index]
            print(f"matrix_3d[{i}][{j}][{k}] = {value}")
