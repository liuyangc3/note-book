original https://blog.packagecloud.io/eng/2016/04/05/the-definitive-guide-to-linux-system-calls/

# The Definitive guide to Linux System Calls

[TL;DR](##TL;DR)

[What is a system call?](##What is a system call?)

[Prerequisite information](##Prerequisite information)

[Hardware and software](### Hardware and software)
## TL;DR

这篇文章描述了 Linux 程序如何调用 Linux 内核函数.


## What is a system call?
当你的程序调用 `open`, `fork`, `read`, `write` (以及其他很多) 函数时,正在发生一个系统调用.


系统调用就是程序如何进入内核执行任务。程序使用系统调用执行一系列的操作诸如：创建进程，网络和文件IO等等。

你可以在 [man page for syscalls(2)](http://man7.org/linux/man-pages/man2/syscalls.2.html) 里面看到系统调用的列表。 用户程序做系统调用有不同的方法，CPU架构不同做系统调用的底层指令也不同。

作为应用开发者，你不需要经常思考系统调用如何正确执行。你只需要把头文件引入，然后像普通功能一样调用。

`glibc` 提供了包装代码，提供抽象接口,原离底层代码, 整理你传递的参数, 然后进入内核。

在我们详细研究系统调用如何实现之前，需要定义一些后面将会出现的条款和核心概念。

## Prerequisite information

### Hardware and software