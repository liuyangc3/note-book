> you are asked to square every digit of a number.
For example, if we run 9119 through the function, 811181 will come out, because 9^2 is 81 and 1^2 is 1.

类似反转数字, 如果不使用字符串转数字, 从右往左记录每一位, 反转 累加的时候注意,大于10的值要进2位(即乘以100)

```python
def square_digits(num):
    digits = []
    while num > 0:
        digits.append(num % 10)
        num = num // 10
    digits.reverse()
    
    result = 0
    for digit in digits:
        if digit * digit < 10:
            result = result * 10 + digit * digit
        else:
            result = result * 100 + digit * digit
    return result
```
