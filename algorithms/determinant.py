# -*- coding:utf-8 -*-

import numpy as np

A = np.array([
    [3, 6, 4],
    [2, 4, 8],
    [1, 6, 9]
])

print np.linalg.det(A)

array = [[3, 6, 4], [2, 4, 8], [1, 6, 9]]
print map(list, zip(*array))


