https://www.codewars.com/kata/539a0e4d85e3425cb0000a88/train/python

We want to create a function that will add numbers together when called in succession.
```
add(1)(2); // returns 3
```
We also want to be able to continue to add numbers to our chain.
```
add(1)(2)(3); // 6
add(1)(2)(3)(4); // 10
add(1)(2)(3)(4)(5); // 15
and so on.
```
A single call should return the number passed in.
```
add(1); // 1
```
We should be able to store the returned values and reuse them.
```
var addTwo = add(2);
addTwo; // 2
addTwo + 5; // 7
addTwo(3); // 5
addTwo(3)(5); // 10
```

一开始以为返回个闭包就行了, 但是要求 `addTwo(3)` 多次调用 都返回 5. 说明是创建了新对象,不是在原有基础上+5

定义一个类, 重写一下 eq add sub  三个运算符即可

```python
def add(n):
    class Int:
        def __init__(self, n):
            self.value = n

        def __add__(self, b):
            return self.value + b
        
        def __sub__(self, b):
            return self.value - b
        
        def __eq__(self, b):
            return self.value == b

        def __call__(self, b):
            return Int(self.value + b)

    return Int(n)
```

还研究了一下如何拿到 caller 的代码
```python
def callme():
    import inspect
    traceback_of_caller = inspect.getframeinfo(inspect.currentframe().f_back)
    # caller_code is the code that call `add` of caller
    caller_code = traceback_of_caller.code_context[0]
    print(caller_code)

if True: callme() # test

output:
if True: callme() # test
```
