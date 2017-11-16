# λ-calculus 
also called lambda calculus
```
f(x, y) = x * x + y * y

如果函数的参数是个函数，这个函数就是"高阶函数" (High-Order Function)
f(x, y) 可以改写成 f(x) = f(y) + x * x , f(y) = y * y

f(x, y) -> f(x)(y) 

function(arg1,arg2,…,argn) - > function(arg1)(arg2)…(argn)
```
这种把多参数函数都转换成单参数高阶函数的方法，叫做柯里化（Currying），
它以数学家 Haskell Brooks Curry 命名的。

Currying 的重要意义在于可以把函数完全变成「接受一个参数；返回一个值」的固定形式，这样对于讨论和优化会更加方便。

偏函数应用(Partial Application)， 把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
## 和计算机程序有什么关系
1965 年，英国计算机科学家 Peter Landin 发现可以通过把复杂的程序语言转化成简单的 𝜆 演算，来理解程序语言
的行为。这个洞见可以让我们把 𝜆 演算本身看成一种程序设计语言。

可以用 lambda calculus 表示布尔值，加减乘除，控制流

## Y Combinator

递归
```python
# 阶乘函数
def fact(n):
    return n * (lambda x:  x if x > 0 else 1)(n - 1)
```

不动点 Fixed-point Combinator
一般的，函数f(x)f(x)的不动点，指的是这样的x，使得x=f(x)x=f(x)。

Y不动点组合子， 在正统的 Lambda 演算里函数全部是没有名字的，
因此直接调用函数名来实现递归函数，在Lambda 演算里无法实现,
用一种特殊的构造可以实现递归， 这部分构造叫 Y Combinator 





# ref

https://github.com/txyyss/Lambda-Calculus/releases/download/v1.0/lambda.pdf

http://pds14.egloos.com/pds/200901/16/93/Lambda-Calculus_and_Combinators.pdf

https://www.zhihu.com/question/21099081