# A number spiral is an infinite grid whose upper-left square has number 1. 
# Here are the first five layers of the spiral:

# +---+---+---+---+---+
# | 1 | 2 | 9 |10 | 25|
# +---+---+---+---+---+
# | 4 | 3 | 8 |11 | 24|
# +---+---+---+---+---+
# | 5 | 6 | 7 |12 | 23|
# +---+---+---+---+---+
# |16 |15 |14 |13 | 22|
# +---+---+---+---+---+
# |17 |18 |19 |20 | 21|
# +---+---+---+---+---+

# Ypur task is to find out the number in row y and column x.

# Input
# The first input line contains an integer t: the number of tests.
# After this, there are t lines, each containing integers y and x.

# Output
# For each test, print the number in row y and column x.

# Constraints
# 1≤ t ≤ 10^5
# 1 ≤ y, x ≤ 10^9

# Example
# Input:
# 3
# 2 3
# 1 1
# 4 2

# Output:
# 8
# 1
# 15

# L1 L2 L3 L4
# L2 L2 L3
# L3 L3 L3
# L4 ...

# you can see total numbers of layer n = L1 + L2 + L3 + L4 ... + Ln
#  equals square n area, so sum(Ln) = n^2

def main(y, x):
    # return munber of row[y] col[x]
    n = max(x, y)
    i = min(x, y)

    if n == x: # layer first value is square(n-1)  + 1, index start at column
        start = n * n - 2 * n + 2
        return start + i -1
    # n == y, layer first value is square(n), index start at row
    start = n * n
    return start - i + 1
