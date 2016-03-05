```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
     0
    / \
   1   2
  / \ / \
 3  4 5  6
+---------+
|  | |  | |   4 bytes
+---------+
"""


def is_power_of_2(n):
    """
    n 是否为2的幂
    """
    return not n & n - 1


def roundup_power_of_2(n):
    """
    n 最接近的2的指数次幂，上边界
    """
    if is_power_of_2(n):
        return n
    index = 0
    while n > 0:
        n >>= 1
        index += 1
    return 1 << index


class BinaryTree(object):
    def __init__(self, size):
        self.array = [0] * (2 * size - 1)

    def left(self, i):
        return self.array[i * 2 + 1]

    def set_left(self, i, v):
        self.array[i * 2 + 1] = v

    def right(self, i):
        return self.array[i * 2 + 1]

    def set_right(self, i, v):
        self.array[i * 2 + 1] = v

    def parent_i(self, index):
        return (index + 1) / 2 - 1


class Buddy(object):
    def __init__(self, size):
        # 大小必须是2的n次方
        if is_power_of_2(size):
            self.size = size
        else:
            raise ValueError("must be power of 2")

        self.tree = BinaryTree(size)

    def malloc(self, size):
        nodes_of_layer = self.size / roundup_power_of_2(size)

    def free(self, size):
```
