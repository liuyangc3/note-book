original https://blog.packagecloud.io/eng/2016/04/05/the-definitive-guide-to-linux-system-calls/

# The Definitive guide to Linux System Calls
Table of contents

- [TL;DR](#tl-dr)
- [What is a system call?](#what-is-a-system-call-)
- [Prerequisite information](#prerequisite-information)
  * [Hardware and software](#hardware-and-software)

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

本文做如下假设：

- 你使用的是Intel或者AMD的32位或者64位CPU。本文讨论的方法可能对其他系统也有用，但是例子中的代码包含一些CPU专用代码。

- 你对3.13.0版本的Linux内核感兴趣。其他版本内核是相似的，但是代码准确的行数，代码的组织和文件路径是不一样的。建议从GitHub上链接3.13.0版本内核源码树。

- 你对`glibc`或者由`glibc`衍生的libc实现感兴趣。 本文所指的x86-64是基于x86架构的64位 Intel 和 AMD CPU。

### User programs, the kernel, and CPU privilege levels
用户程序（比如编辑器，终端，ssh守护程序等等）需要和linux内核交互，所以有些用户程序无法自己执行的行为可以调用内核执行。

比如，如果用户程序需要做IO操作(`open`, `read`, `write` 等)或者修改自己地址空间(`mmap`, `sbrk`等)，必须触发内核运行来完成这些操作行为。

是什么阻止用户程序自己执行这些操作？

是x86-64的CPU有一个[privilege levels](https://en.wikipedia.org/wiki/Protection_ring#Privilege_level)概念。权限等级是个复杂的题目适合单独一片博客来阐述。在这片博客中，我们简单地把权限等级概念解释为：

1. 权限等级意味着访问控制。当前权限等级决定了那些CPU指令和IO操作可以执行。

2. 内核运行在最高权限等级，叫做 "Ring 0"。用户程序运行在较低等级，叫做"Ring 3"。

用户程序为了要执行某些高权限操作，必须修改权限等级（从 Ring 3到 Ring 0），所以由内核执行。

这就是我们常说的用户态和内核态.

有很多方法可以改变权限等级，触发内核执行操作。

我们先从最普遍的导致内核操作的方法开始: interrupts 中断

### interrupts

你可以把一个中断事件理解成由硬件或者软件产生(或者引起)的事件。这样的信号称为进行中断请求（interrupt request，IRQ）

硬件中断是由硬件设备产生的中断, 它通知内核有特殊事件发生了。这种中断较常见的例子是网卡收到包产生的中断。

一个软件中断是执行某条代码的时候产生的。在x86-64系统中，执行 `int` 指令可以 raise 一个软件中断。

X86 CPU 提供了一个外接引脚 INTR, 用来接受外部设备中断信号, 通常设备的中断信号由 PIC（Programmable Interrupt Controller）传入 CPU


Intel 又把 同步中断和异步中断
- 同步中断是CPU自己产生的,  intel 叫 exceptions 异常
- 异步中断由外部设备产生的, intel 叫 interrupts 中断

然后每个下面又分几种类型

- exception
  * fault
  * trap
  * abort
 
- interrupt
  * Maskable 
  * Nomaskable 
 
传统的系统调用(exception)是通过指令 `int 128` 实现的
