# 
```python
class T:
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        # or
        # self = object.__new__(cls)
        return self


    def __init__(self, arg):
        self.arg = arg

t = T("test")
```
先运行 __new__, 传入类和参数，返回实例
然后调用 __init__, 实例和参数一同传递到 __init__


```python
class T:
    def __call__(self, *args, **kwargs):
        print("__call__: arguments {}, keyword arguments {}".format(args, kwargs))
        
t = T()
t("bar")        
```
__call__ 当实例被调用时触发