# Memory Segmentation

## why segmentation
设计师们想要1MB或者64KB的16倍，由于设计原因，它们不希望使用大于16bit的寻址系统。
所以它们通过发明了一个复合寻址系统克服了这个限制。每个复合地址包含了2个16bit数字，
由一个特殊的方法来解释，这就是最初的"地址分段"。与此相配合的是，新的CPU芯片设计有新的寄存器以促进这种新的寻址方法。

内存保护，例如 Linux 内核检查到引发缺页的线性地址不在进程的线性地址范围内，会发出SIGSEGV信号，进程结束，
我们看到 Segmentation fault。


# 分段
逻辑地址 ->线性地址

segment register (cs) store 16-bit segment selectors
stack segment register (ss)




在x86保护模式下，段的信息（段基线性地址、长度、权限等）即段描述符占8个字节
，段信息无法直接存放在段寄存器中（段寄存器只有2字节）。
Intel的设计是段描述符集中存放在GDT或LDT中，而段寄存器存放的是段描述符在GDT或LDT内的索引值(index)。

怎样防止进程访问不属于自己的线性地址（如内核空间）或无效的地址呢？内核里记录着每个进程能访问的线性地址范围
（进程的vm_area_struct 线性区链表和红黑树里存放着），
在引发缺页异常的时候，





#
Linux中逻辑地址等于线性地址。为什么这么说呢？
因为Linux所有的段（用户代码段、用户数据段、内核代码段、内核数据段）的线性地址都是从 0x00000000 开始，
长度4G，这样 线性地址=逻辑地址+ 0x00000000，也就是说逻辑地址等于线性地址了。


# R
http://homepage.smc.edu/morgan_david/cs40/segmentation.htm

http://duartes.org/gustavo/blog/post/memory-translation-and-segmentation/