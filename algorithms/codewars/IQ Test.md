> find out which one of the given numbers differs from the others.
Bob observed that one number usually differs from the others in evenness. 
Help Bob — to check his answers, he needs a program that among the given numbers finds one that is different in evenness, and return a position of this number.
! Keep in mind that your task is to help Bob solve a real IQ test, which means indexes of the elements start from 1 (not 0)

##Examples :
```js
q_test("2 4 7 8 10") => 3 // Third number is odd, while the rest of the numbers are even

iq_test("1 2 1 1") => 2 // Second number is even, while the rest of the numbers are odd
```

6 kyu



先看前2个数, 如果相同, 说明后面只要出现不同的数,那个就是我们要找的数

如果不同, 第三个数决定了 前面两个是哪个不同. 注意 index 是从 1 开始

```
def iq_test(numbers):
    nums = [int(i) for i in numbers.split()]

    left = nums[0] % 2
    right = nums[1] % 2
    
    for i, n in enumerate(nums[2:]):
        if left != right:
            if n % 2 == left:
                return 2
            else:
                return 1
                
        else: # left == right:
            if n % 2 != left:
                return i +1 + 2  # +2 is first tow number
```
