# 函数类型

https://golang.org/ref/spec#Function_types

一个函数类型是具有相同参数类型和返回值类型的函数集合

也就是说下面三个函数都是一个函数类型
```go
func f1(x int) int {
    return x
}

func f2(y int) int {
    return y + 1
}

var f3 = func(z int) int {
    return z -1
}

func main() {
	set := []func(int) int{
		f1, f2, f3,
	}

	for _, f := range set {
		println(f(1))
	}
}
```

也可以给函数类型起个名字
```go
type FuncType func(arg int) int
```

这样上面的函数可以改写成
```go
set := []FuncType{
	f1, f2, f3,
}
```

参数类型或者返回值类型必须严格相同，所以下面的写法是不可以的
```go
tpye Int int

// Int 不是 int，所以 f4 不是 FuncType
func f4(y Int) Int {
    return y + 1
}
```

利用函数类型,给一个函数加上一个方法
```golang
type FuncType func(name string) string

func (f FuncType) say() {
    fmt.Println(f() + "say()")
}

func test(name string) string {
    return "Hello," 
}

func main() {
	f := FuncType(test)
	fmt.Println(f())
	f.say()
}

// out
Hello,
Hello,say()
```

实现了函数类型，自动获得类型下的方法
```golang
type FuncType func(name string) string

func (f FuncType) say() {
    fmt.Println(f() + "say()")
}

func main() {
	f := func(name string) string {
	    println(name)
	}
	
	
}

// out
Hello,
Hello,say()
```


典型的例子 http.HandlerFunc
```go
type HandlerFunc func(ResponseWriter, *Request)

func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
	f(w, r)
}
```