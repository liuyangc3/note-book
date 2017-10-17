





## 伪寄存器
4 个 预先声明的符号作为伪寄存器，他们不是真的寄存器，是工具链在中间过程使用的虚拟寄存器，
这些伪寄存器在所有架构是通用的：
* FP: Frame pointer: arguments and locals.
* PC: Program counter: jumps and branches.
* SB: Static base pointer: global symbols.
* SP: Stack pointer: top of stack.

所有用户定义的符号，写成相对伪寄存器的偏移量，  FP (arguments and locals) 和 SB (globals).

SB 伪寄存器可以想象成内存的地址，所以符号 `foo(SB)` 是一个由foo这个名字代表的内存地址。这种形式一般用来命名全局函数和数据。给名字增加一个`<>`符号，就像`foo<>(SB)`，会让这个名字只有在当前文件可见，类似在C文件中预定义的static。

FP伪寄存器是一个虚拟的帧指针，用来指向函数的参数。编译器维护了一个虚拟的栈指针，使用对伪寄存器的offsets操作的形式，指向栈上的函数参数。 于是，0(FP)就是第一个参数，8(FP)就是第二个(64位机器)，以此类推。 当用这种方式引用函数参数时，可以很方便的在符号前面加上一个名称，就像first_arg+0(FP)和second_arg+8(FP)。有些汇编程序强制使用这种约定，禁止单一的0(FP)和8(FP)。在使用Go标准定义的汇编函数中，go vet会检查参数的名字和它们的匹配范围。 在32位系统上，一个64位值的高32和低32位表示为增加_lo和_hi这个两个后缀到一个名称，就像arg_lo+0(FP)或者arg_hi+4(FP)。如果一个Go原型函数没有命名它的结果，期待的名字将会被返回。

SP伪寄存器是一个虚拟的栈指针，用来指向栈帧本地的变量和为函数调用准备参数。它指向本地栈帧的顶部，所以一个对栈帧的引用必须是一个负值且范围在[-framesize:0]之间，例如: x-8(SP)，y-4(SP)，以此类推。在CPU架构中，存在一个真实的寄存器SP，虚拟的栈寄存器和真实的SP寄存器的区别在于名字的前缀上。就是说，x-8(SP)和-8(SP)是不同的内存地址：前者是引用伪栈指针寄存器，但后者是硬件中真实存在的SP寄存器。


# 汇编指令
MOVQ，ADDQ 和 RET 是指令

MOVQ 赋值
LEAQ 取地址

标准的DATA指令形式为：
```
DATA    symbol+offset(SB)/width, value
```
例如
```
DATA divtab<>+0x00(SB)/4, $0xf4f8fcff
DATA divtab<>+0x04(SB)/4, $0xe6eaedf0
...
DATA divtab<>+0x3c(SB)/4, $0x81828384
```
GLOBAL指令将一个symbol声明为全局的,LOBAL指令必须跟在对应的DATA指令之后。
```
GLOBL divtab<>(SB), RODATA, $64
GLOBL runtime·tlsoffset(SB), NOPTR, $4
```
NOSPLIT = 4 (TEXT项使用.) 不插入预先检测是否将栈空间分裂的代码。程序的栈帧中，如果调用任何其他代码都会增加栈帧的大小，必须在栈顶留出可用空间。用来保护处理栈空间分裂的代码本身。
RODATA = 8 (DATA和GLOBAL项使用.) 将这个数据放在只读的块中
NOPTR = 16 这个数据不包含指针所以就不需要垃圾收集器来扫描。


# example
https://www.davidwong.fr/goasm

go tool objdump -s main.add
```go
package main

func add(a, b int) int {
    return a + b
}
func main() {add(1,2)}  
```

# 编译
```
go build -gcflags '-N -l' main.go
```
查看入口起始地址 -f 打印 file-headers
```
objdump -f main

main:     file format elf64-x86-64
architecture: i386:x86-64, flags 0x00000112:
EXEC_P, HAS_SYMS, D_PAGED
start address 0x0000000000448fc0
```
需要查找地址 0x448fc0
```
objdump -d main|grep 448fc0 -A 10
0000000000448fc0 <_rt0_amd64_linux>:
  448fc0:       48 8d 74 24 08          lea    0x8(%rsp),%rsi
  448fc5:       48 8b 3c 24             mov    (%rsp),%rdi
  448fc9:       48 8d 05 10 00 00 00    lea    0x10(%rip),%rax        # 448fe0 <main>
  448fd0:       ff e0                   jmpq   *%rax
```
可以看到在 x86_64 Linux 上函数的入口叫做 `_rt0_amd64_linux`

[src/runtime/rt0_linux_amd64.s](https://github.com/golang/go/blob/release-branch.go1.8/src/runtime/rt0_linux_amd64.s)
```
TEXT _rt0_amd64_linux(SB),NOSPLIT,$-8
	LEAQ	8(SP), SI // argv
	MOVQ	0(SP), DI // argc
	MOVQ	$main(SB), AX
	JMP	AX
...

TEXT main(SB),NOSPLIT,$-8
	MOVQ	$runtime·rt0_go(SB), AX
	JMP	AX
```
`_rt0_amd64_linux` 调用了main，保存参数 (argc and argv) 到寄存器 (DI and SI)，
main 里调用了 rt0_go

(src/runtime/asm_amd64.s)[https://github.com/golang/go/blob/release-branch.go1.8/src/runtime/asm_amd64.s]
具体设是 Resizable stack 的内容

# add 函数

查看 add 函数
```
go tool compile -N -l -S main.go 
"".add t=1 size=28 args=0x18 locals=0x0
        0x0000 00000 (main.go:3)        TEXT    "".add(SB), $0-24
        0x0000 00000 (main.go:3)        FUNCDATA        $0, gclocals·54241e171da8af6ae173d69da0236748(SB)
        0x0000 00000 (main.go:3)        FUNCDATA        $1, gclocals·33cdeccccebe80329f1fdbee7f5874cb(SB)
        0x0000 00000 (main.go:3)        MOVQ    $0, "".~r2+24(FP)
        0x0009 00009 (main.go:4)        MOVQ    "".a+8(FP), AX
        0x000e 00014 (main.go:4)        MOVQ    "".b+16(FP), CX
        0x0013 00019 (main.go:4)        ADDQ    CX, AX
        0x0016 00022 (main.go:4)        MOVQ    AX, "".~r2+24(FP)
        0x001b 00027 (main.go:4)        RET
        0x0000 48 c7 44 24 18 00 00 00 00 48 8b 44 24 08 48 8b  H.D$.....H.D$.H.
        0x0010 4c 24 10 48 01 c8 48 89 44 24 18 c3              L$.H..H.D$..
// or
go tool objdump -s main.add main
TEXT main.add(SB) /root/gotest/main.go
        main.go:3       0x44d650        48c744241800000000      MOVQ $0x0, 0x18(SP)
        main.go:4       0x44d659        488b442408              MOVQ 0x8(SP), AX
        main.go:4       0x44d65e        488b4c2410              MOVQ 0x10(SP), CX
        main.go:4       0x44d663        4801c8                  ADDQ CX, AX
        main.go:4       0x44d666        4889442418              MOVQ AX, 0x18(SP)
        main.go:4       0x44d66b        c3                      RET
```       

objdump 输出 包括4 个部分：
* 源码行号
* 目标文件中的偏移量
* 机器码
* 汇编代码


`$0-24` 指定了栈空间所需的 frame size（0代表我们只使用寄存器)
frame size 之后是一个减号(不是真的做减法，而是一个助记符)， 后面跟的数字代表参数和返回值 (argument) 的大小。 本例中参数和返回值占用 3*8 个字节 (它们存在于调用者 caller 的栈内)

stack frame layout
```
+--------+  0x18
| return |
+--------+  0x10
|  arg1  |
+--------+  0x8
|  arg2  |
+--------+ <--- FP/SP
```

```
MOVQ    $0, "".~r2+24(FP)
```
<<<<<<< HEAD
MOVQ 指令用来移动64位的值 (Q代表 QUADWORD)，FP+24 存入0
=======
MOVQ 指令用来移动64位的值 (Q代表 QUADWORD)，FP 存入0
>>>>>>> 70f77497e70b9dc93524e8b6f19ddfc77498b666

```
FUNCDATA        $0, gclocals·54241e171da8af6ae173d69da0236748(SB)
FUNCDATA        $1, gclocals·33cdeccccebe80329f1fdbee7f5874cb(SB)
```
这里的FUNCDATA是golang编译器自带的指令，plan9和x86的指令集都是没有的。它用来给gc收集进行提示。
第一个参数表示函数数据是参数还是局部变量，第二个参数与一个隐藏变量相关，它里面包含了 gc mask
提示和0和1是用于局部函数调用参数，需要进行回收。

```
MOVQ    "".b+16(FP), AX
MOVQ    "".a+8(FP), CX
// or
MOVQ 0x8(SP), AX
MOVQ 0x10(SP), CX
```
这里是将基于栈指针 FP (指向函数参数)的一个偏移中的数据移动到寄存器 AX 和 CX 中.

FP是frame pointer，是指向栈底，SP是指向栈顶, AX,CX 是伪寄存器，那么上面的句子是代表把FP+6这个位置的数据（参数b），保存到AX中；同理 FP+8(参数a) 保存到CX 

```
ADDQ    CX, AX
```
ADDQ 指令对两个64位的寄存器中的值做加法， 结果存储到 AX 中。

```
MOVQ    AX, "".~r2+24(FP)
// or
MOVQ    AX, 0x18(SP)
```
return AX









# ref
[A Quick Guide to Go's Assembler](https://golang.org/doc/asm)
<<<<<<< HEAD

=======
>>>>>>> 70f77497e70b9dc93524e8b6f19ddfc77498b666
[Golang Internals, Part 5: the Runtime Bootstrap Process](https://blog.altoros.com/golang-internals-part-5-runtime-bootstrap-process.html)