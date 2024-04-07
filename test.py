from cmu_graphics import *
import numpy as np

first = [1, 2, 3]
second = [4, 5, 6]

first = np.transpose(np.array(first))
second = np.transpose(np.array(second))
print(first - second)

first = np.append(first, [[1]])

thing = {1: 2, 3: 4, 0: 6}
print(thing.sort())