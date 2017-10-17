## control state/control flow
 
指在程序运行时，个别的指令（或是statement、subroutine）运行或求值的顺序

例如下面的 statement
```
a = 1 + 2 + 3
```
加法从左开始执行

或者 block
```
x = 1
if x > 0:
    print(x)
```
整个程序默认从行号较小的行开始执行，条件控制(if, while ...)以缩进为界，其他语言以 `{}`有自己规则


有些编程语言会提供非区部的控制流程（non-local control flow），会允许流程跳出目前的代码，进入一段事先指定的代码。常用的结构化非区部控制流程可分为条件处理（condition）、异常处理（Exceptions）及延续性（Continuation）三种

* condition  on condition goto  多数语言不支持
* Exceptions try {} catch {}
* Continuation 延续性是 control state 的抽象

## Continuation

http://jlongster.com/Whats-in-a-Continuation

https://www.h5jun.com/post/what%E2%80%99s-in-a-continuation.html

Continuation 实化(如内存地址实化成了指针)了 control state

一个延续性以数据结构的形式表现了程序在运行过程中某一点的计算状态，相应的数据内容可以被编程语言访问

通过延续性，可以实现协程，可以暂停自身的执行，然后通过一个值恢复执行


http://www.mitgai.net/2015/08/programming-language/talk-about-concurrent-programming.html#more-796

延续调用，不采用堆栈来保存上下文，而是把这些信息保存在 continuation record 中。这些 continuation record 和堆栈的 activation record 的不同，并不采用后入先出的堆栈存储方式，而是以节点的形式存放在树或者图中，从一个函数调用另一个函数就等于给当前节点生成一个子节点并系统寄存器移动到这个子节点上。
这样的好处是什么，就是我们不需要按照线性的顺序来完成函数，我们完全可以自由的在不同的节点间进行跳转，不需要像堆栈一样一层一层的 return。这里的 return 更像是一个带参数的 goto。

## continuation-passing style（CSP）变换
CPS 作用是调用函数执行后并不直接返回值, 而是将值传入continuation function, 由continuation function执行获得返回值后的操作

如
```python
def callee(x, y):
    return x + y

callee(1, 3)


# CPS transfer
def callee_cps(x, y, continuation):
    continuation(x + y)

callee_cps(1, 3, lambda x:x)
```

有什么用？

CPS 变换说白了就是把程序内部原本隐式的控制流跳转，用某种方法抽象出来暴露给程序员

CPS 常常用到的地方是实现 call/cc ，用这货能实现诸如协程，yield 之类的特性

## Coroutines
Coroutines are computer program components that generalize subroutines for non-preemptive multitasking, by allowing multiple entry points for suspending and resumingexecution at certain locations.


https://zhuanlan.zhihu.com/p/25513336


同步写RPC调用的例子，可能coroutine模型就是最适合

