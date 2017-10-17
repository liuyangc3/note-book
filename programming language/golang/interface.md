
# interface
 understanding golang interface(Gopher China) — 
 [youtube](https://www.youtube.com/watch?v=F4wUrj6pmSI&t=2319s), [slide](https://github.com/gopherchina/conference/blob/master/2017/1.4%20interface.presented.pdf)

在 Golang 中，interface 是一组 method 的集合，是 duck-type。

这种非侵入式设计好处是，我们可以先实现类型，然后再抽象出所需接口，项目前期就设计好合理接口并不容易。

# 设计
>Be conservative in what you send, be liberal in what you accept. — Robustness Principle

对应到 Golang：

>Return concrete types, receive interfaces as parameter. — Robustness Principle applied to Go

接收接口返回类型

有时候也要返回接口，例如 context 库
```go
// all return a Context interface
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)    //retrun cancelCtx struct
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc) //retrun timerCtx struct
func WithValue(parent Context, key, val interface{}) Context    //retrun valueCtx struct
```


# interface detail
http://legendtkl.com/2017/07/01/golang-interface-implement/

https://github.com/golang/go/issues/20505


[src/runtime/runtime2.go](https://github.com/golang/go/blob/master/src/runtime/runtime2.go)
```go
// interface with methods
type iface struct {
	tab  *itab
	data unsafe.Pointer
}

// emtpy interface : interface{}
type eface struct {
	_type *_type
	data  unsafe.Pointer
}

type itab struct {
	inter *interfacetype
	_type *_type
	hash  uint32 // copy of _type.hash. Used for type switches.
	_     [4]byte
	fun   [1]uintptr // variable sized. fun[0]==0 means _type does not implement inter.
}

// src/runtime/type.go
type interfacetype struct {
	typ     _type
	pkgpath name
	mhdr    []imethod
}

type _type struct {
	size       uintptr
	ptrdata    uintptr // size of memory prefix holding all pointers
	hash       uint32
	tflag      tflag
	align      uint8
	fieldalign uint8
	kind       uint8
	alg        *typeAlg
	// gcdata stores the GC type data for the garbage collector.
	// If the KindGCProg bit is set in kind, gcdata is a GC program.
	// Otherwise it is a ptrmask bitmap. See mbitmap.go for details.
	gcdata    *byte
	str       nameOff
	ptrToThis typeOff
}
```

```
package main

type Interface interface {
	Say()
}

type N int

func (n N) Say() {}

func main() {
	var n N
	var inter Interface = &n
	inter.Say()
}

// go build -gcflags "-N -l" interface.go
// gdb interface

(gdb) l main.main
6
7       type N int
8
9       func (n N) Say() {}
10
11      func main() {
12          var n N
13          var inter Interface = &n
14          inter.Say()
15      }
(gdb) b 14
Breakpoint 1 at 0x44d6b9: file interface.go, line 14.
(gdb) run
(gdb) info locals
&n = 0xc42005c000
inter = {tab = 0x49a0a0, data = 0xc42005c000}
(gdb) p inter.tab.inter.mhdr 
$10 = {array = 0x45c440, len = 1, cap = 1}
(gdb) p inter.tab.inter.mhdr.array[0]
```




# type assign to interface
```go
type I interface {
    String()
}
var a int = 5
var i I = a
```