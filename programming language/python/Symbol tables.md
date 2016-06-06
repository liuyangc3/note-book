译自

http://eli.thegreenplace.net/2010/09/18/python-internals-symbol-tables-part-1/

http://eli.thegreenplace.net/2010/09/18/python-internals-symbol-tables-part-2/

介绍
------
这篇文章里我将介绍 CPython 是如何实现 symbol tables (符号表)的,并在内部寻找中使用符号表,把源代码编译为字节码.
在这个部分里我将解释什么是符号表,并展示它的概念是如何应用到Python的,第二部分介绍它在CPython中的实现.

什么是符号表?
------
[维基百科](http://en.wikipedia.org/wiki/Symbol_table)上的解释:
>在计算机科学里,符号表是一种编程语言转换器使用数据结构,通常这种转换器是编译器或者解释器,
在符号表内部,每个源码里的标识都关联了它的符声明或出现信息,例如类型,作用域,有时候还有位置.

几乎所有的编译器都使用符号表,尤其是静态类型的语言,因为所有的变量都有类型,类型检查是前段的重要部分.

考虑如下代码:
```c
int main()
{
    int aa, bb;

    bb = *aa;

    {
        int* aa;
        bb = *aa;
    }

    return 0;
}

```

代码中有两处`bb = *aa`,但是只有第二个是正确的,编译器遇到第一个语句会抛出下面的错误信息:
```
error: invalid type argument of ‘unary *’ (have ‘int’)
```
编译器是如何知道`*`操作符的参数是个`int`类型,并且是个非法的类型呢?答案就是:符号表.
当编译器看到`*aa`后会问自己`aa`的类型是什么,问题的答案就在它之前构建的符号表中.
符号表囊括了所有编译器在源码中遇到的变量的类型.

这个简单的例子也演示了另一个重要概念-对于大多数语言,不会仅有单一的符号表保存所有变量的信息.
第二个赋值语句是合法的,是因为在内部花括号的用域内,`aa`被重新定义为指针类型.
因此为了正确编译这样的代码,C编译器需要为每个作用域保持一个符号表.

题外话:Python里的"变量"
----------
目前为止,我很随意的使用"变量"这个术语.为了安全起见,我们来看看"变量"在Python中的定义.
Python并没有C意义上的变量,Python拥有和对象对象的Symbol names(符号名):
```python
aa = [1, 2, 3]
bb = aa
aa[0] = 666
```

在这段代码里,`aa`绑定到一个 list 对象, `bb` 是另一个绑定到这个对象的名字,
第三行通过aa修改了 list 对象的元素,如果我们打印`bb`,我们也会看到这个被修改的对象.

现在理解了这个,我仍然会使用"变量"这个术语，因为它有时很方便，而且每个人都习惯它.

Python代码的符号表
----------
是的,符号表对类型检查非常有用.但是 Python 并没有编译时的类型检查(鸭子类型),那么 CPython 用符号表来干什么?

CPython 编译器仍然需要符号表来解析代码里的变量是那种类型的.Python 中的变量可以是局部的,全局的,甚至是一个语法封闭的作用域,例如:
```python
def outer(aa):
    def inner():
        bb = 1
        return aa + bb + cc
    return inner
```

函数`inner`使用了3个变量,`aa`,`bb`和`cc`.从 Python 的视角来看,他们是不同的:
`aa`是绑定在`outer`上,`bb`是局部的,绑定在内部的`inner`,而`cc`没有任何的绑定,所以被认为是全局的.
生成`inner`的字节码清楚的显示了这些变量的不同的处理方式:
```python
5           0 LOAD_CONST               1 (1)
            3 STORE_FAST               0 (bb)

6           6 LOAD_DEREF               0 (aa)
            9 LOAD_FAST                0 (bb)
           12 BINARY_ADD
           13 LOAD_GLOBAL              0 (cc)
           16 BINARY_ADD
           17 RETURN_VALUE
```

如你所见,加载变量到栈使用了不同的操作码,并按顺序执行`BINARY_ADD`,`LOAD_DEREF`是加载 `aa`,
`LOAD_FAST`是加载`bb`,而 `LOAD_GLOBAL` 是 `cc`.

此刻,为了更进一步地理解 Python,我们有3个不同的方向:

1.  弄明白 Python 中定义变量的精确语义 - 什么时候它们是局部的,什么时候是全局的,
    并且是什么使在它们词法上的绑定.

2.  弄明白 Cpython 编译器是如何知道这些区别的.

3.  学习这3种不同的字节码操作码,它们是如何影响 VM 运行代码的.

我们不会进入(1),因为范围太过宽广,也不是这篇文章的主题.网络上有很多的资源,先从[官方文档](http://docs.python.org/dev/py3k/reference/executionmodel.html)
开始,然后持续地谷歌直到你完全搞明白了.(3)同样超出范围,我目前仅仅关注 CPython 的前端,
如果你感兴趣,有许多的关于Python后端的文章,附带这个问题的一个很好的[处理](https://tech.blog.aknin.name/2010/06/05/pythons-innards-naming/).

为了解答(2),我们需要知道 Cpython 如何使用符号表,这正是这篇文章的意义.

符号表放在哪里
--------

Cpython 的前端高层视图是:

1.  解析源代码为解析树
2.  把解析树转化为抽象语法树(Abstract Syntax Tree, AST)
3.  把AST转化为控制流图(Control Flow Graph, CFG)
4.  根据CFG生成字节码

符号表在第三部生成,编译器从AST构建一个符号表用来代替 Python 源代码.
这个符号表结合AST将会生成CFG,并最终生成字节码.

探索符号表
-------
CPython做了一个很了不起的工作,将一些内部的信息通过标准库曝露出来,通过模块 `symtable`,
符号表也是一个可以从纯Python代码里可以获取的数据结构,根据模块的定义:
> 符号表是编译器在生成字节码前,从AST中生成的.它代表了代码内每个标识符计算的范围.
symtable提供了检查这些符号表的接口.

`symtable`模块提供了标识符的大量信息,除了告诉我们标识符的作用域,还允许我们找出哪个变量在自己的作用域内被重新引用了,
以及定义名称空间(像函数),等等.为了浏览符号表,我写了下面的函数,简单的使用这个模块:
```python
def describe_symbol(sym):
    assert type(sym) == symtable.Symbol
    print("Symbol:", sym.get_name())

    for prop in [
            'referenced', 'imported', 'parameter',
            'global', 'declared_global', 'local',
            'free', 'assigned', 'namespace']:
        if getattr(sym, 'is_' + prop)():
            print('    is', prop)
```
我们来看看它如何解释上面的例子中的`inner`函数
```
Symbol: aa
    is referenced
    is free
Symbol: cc
    is referenced
    is global
Symbol: bb
    is referenced
    is local
    is assigned
```







