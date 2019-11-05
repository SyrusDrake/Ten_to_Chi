import numpy as np

dims = 3
b = np.fromfile("import_test.txt", sep=' ')
b.shape = b.size//dims, dims
print(b)

point = np.random.uniform(0, 100, dims) # choose random point
print ('point:', point)
