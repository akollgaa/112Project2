from cmu_graphics import *
import numpy as np

first = np.array([1, 2, 3, 4])

modelMatrix = np.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

print(first)

print(np.dot(modelMatrix, first))

print(np.dot(modelMatrix, np.transpose(first)))

