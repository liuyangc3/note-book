new

内建函数 new(T) 为类型 T 的每项分配零值，并且返回 T 的地址，即一个指针类型 *T 


基本类型的声明和 new 行为类似  
```go
var i int
println(&i, i)

p := new(int)
println(p, *p)

------ out
0xc042023f38 0
0xc042023f48 0
```

struct 声明、构造表达式 和 new 行为类似
```go
type S struct {}

var s S
fmt.Printf("%v %p\n", s, &s)
s1 := &S{}
fmt.Printf("%v %p\n", *s1, s1)
ps := new(S)
fmt.Printf("%v %p\n", *ps, ps)

------ out
{} 0x634d58
{} 0x634d58
{} 0x634d58
```

对于 slice map chan 类型，使用 make 初始化, 原型
```go
func make(Type, size IntegerType) Type
```
和new 不同，maka 不返回指针，返回类型

slice 类型的构造表达式 和 make 行为一致
```go
var s1 []int            // s1 == nil
s2 := []int{}
s3 := make([]int, 0, 0)
fmt.Printf("%#v\n", (*reflect.SliceHeader)(unsafe.Pointer(&s1)))
fmt.Printf("%#v\n", (*reflect.SliceHeader)(unsafe.Pointer(&s2)))
fmt.Printf("%#v\n", (*reflect.SliceHeader)(unsafe.Pointer(&s3)))

---- out
&reflect.SliceHeader{Data:0x0, Len:0, Cap:0}
&reflect.SliceHeader{Data:0x634d58, Len:0, Cap:0}
&reflect.SliceHeader{Data:0x634d58, Len:0, Cap:0}
```
s2/s3 内部数组指针指向 runtime.zerobase