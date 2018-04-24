# call/cc
call-with-current-continuation，
它可以捕捉当前环境下的 current continuation并利用它做各种各样的事情

# Continuation
延续

https://www.quora.com/What-is-continuation-passing-style-in-functional-programming

CPS
Continuation-passing style 是一种定义和执行函数的方式

正常函数传入参数，经过计算返回结果，这里的返回是语言层面的，并不由程序控制。
而CPS的做法是对 "返回" 做了明确定义，赋予我们对最后的控制流更多的控制力。

写成CPS函数有一个额外的callback参数，它是一个用用于替代return计算结果的函数，
这个callback叫做 Continuation 延续，因为它是将要获得返回值，表示即将要做的事情。

```
function add(a, b) {
  return a + b;
}
```
用cps 改写， 先用参数 callback `done`  替代 return
```
function add_cps(a, b, done) {
  done(a + b);
}
```
因为这个函数并不返回任何值，所以需要把返回值 result 作为 callback 的参数
```
add_cps(a, b, function (result) {
  // use result here
});
```

有什么用