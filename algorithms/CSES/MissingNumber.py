# You are given all numbers between 1,2,…,n except one.
# Your task is to find the missing number.
#
# Input
#
# The first input line contains an integer n. The second line contains n−1
# numbers. Each number is distinct and between 1 and n (inclusive).
#
# Output
#
# Print the missing number.
#
# Constraints
# 2 ≤ n ≤ 2*10^5
# Example
#
# Input:
# 5
# 2 3 1 5
#
# Output:
# 4

import sys

n = int(sys.stdin.readline())
seq = sys.stdin.readline()

sum = 0
for i in seq.split():
    sum += int(i)

sum_n = n * (n + 1) // 2

print(sum_n - sum)
