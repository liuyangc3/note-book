import sys

x = int(sys.stdin.read())

while x > 1:
    sys.stdout.write('%d ' % x)
    if x & 1:  # odd
        x = x * 3 + 1
    else:  # even
        x = x // 2

sys.stdout.write('1\n')
