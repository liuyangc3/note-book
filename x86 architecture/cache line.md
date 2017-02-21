# Cache Line
最数据小单元 加载/保存 到内存

CPU缓存是一个高效的非链式结构的hash map，每个桶（bucket）通常是64个字节。被称为之为一个“缓存行（cache line）”。
缓存行（cache line）是内存传输的有效单元。


处理器从内存读取操作数(operand)到缓存(L1,L2,L3),每次读取 cache line 大小，这个操作叫做 `cache line fill`.

内存里的操作数位置如果在缓存里，下次处理器访问操作数的时候，会直接从缓存读取，这个操作叫做 `cache hit`.
# 
grep . /sys/devices/system/cpu/cpu0/cache/index*/*

# Memory Type 
Memory Types and Their Properties

Memory Type and Mnemonic | Cacheable | Writeback Cacheable | Allows Speculative Reads | Memory Ordering Model
:--- | :--- | :--- | :--- | :---
Strong Uncacheable(UC)| No | No | No | Strong Ordering.
Uncacheable (UC-) | No | No | No | Strong Ordering. Can only be selected through the PAT. Can be overridden by WC in MTRRs.
Write Combining (WC) | No | No | Yes | Weak Ordering. Available by programming MTRRs or by selecting it through the PAT.
Write Through (WT) | Yes | No  | Yes | Speculative Processor Ordering.
Write Back (WB) | Yes | Yes | Yes | Speculative Processor Ordering.
Write Protected (WP) | Yes for reads; no for writes | No | Yes | Speculative Processor Ordering.







 
# Cache Write
## Write through

## Write back

## coherency protocols
CPU 之间使用 coherency protocols 来同步 cache 的数据。 

只要系统只有一个CPU核在工作，一切都没问题。
如果有多个核，每个核又都有自己的缓存，如果某个CPU缓存段中对应的内存内容被另外一个CPU偷偷改了，会产生一个问题：

数据没有发生变化

那么在其他CPU修改这块内存的时候，我们希望得到通知。

方案一

让多个CPU核共用一组缓存：也就是说只有一块一级缓存，所有处理器都必须共用它。在每一个指令周期，只有一个幸运的CPU能通过一级缓存做内存操作，运行它的指令。
这本身没问题。唯一的问题就是太慢了，因为这下处理器的时间都花在排队等待使用一级缓存了（并且处理器会做大量的这种操作，至少每个读写指令都要做一次）。


方案二
使用多组缓存，但使它们的行为看起来就像只有一组缓存那样。缓存一致性协议就是为了做到这一点而设计的。

窥探（snooping）/基于目录的（directory-based）

snooping 背后的基本思想是，所有内存传输都发生在一条共享的总线上，而所有的处理器都能看到这条总线：缓存本身是独立的，
但是内存是共享资源，所有的内存访问都要经过仲裁（arbitrate）：同一个指令周期中，只有一个缓存可以读写内存。
窥探协议的思想是，缓存不仅仅在做内存传输的时候才和总线打交道，而是不停地在窥探总线上发生的数据交换，跟踪其他缓存在做什么。
所以当一个缓存代表它所属的处理器去读写内存时，其他处理器都会得到通知，它们以此来使自己的缓存保持同步。
只要某个处理器一写内存，其他处理器马上就知道这块内存在它们自己的缓存中对应的段已经失效。

在直写模式下，这是很直接的，因为写操作一旦发生，它的效果马上会被“公布”出去。但是如果混着回写模式，就有问题了。因为有可能在写指令执行过后很久，数据才会被真正回写到物理内存中——在这段时间内，其他处理器的缓存也可能会傻乎乎地去写同一块内存地址，导致冲突。在回写模型中，简单把内存写操作的信息广播给其他处理器是不够的，我们需要做的是，在修改本地缓存之前，就要告知其他处理器。搞懂了细节，就找到了处理回写模式这个问题的最简单方案，我们通常叫做MESI协议（译者注：MESI是Modified、Exclusive、Shared、Invalid的首字母缩写，代表四种缓存状态，下面的译文中可能会以单个字母指代相应的状态）。

###  MESI 以及衍生协议



## Write Combining
当CPU执行存储指令(store)时，它会尝试将数据写到离CPU最近的L1缓存。如果此时出现 Write miss，CPU会访问下一级缓存。
为了减少 Write Miss 带来的性能开销，英特尔以及其它厂商的 CPU 都会使用一种称为"write combining"的技术。

当发生L1 Write Miss时,在owner 对这个cache line 读之前，CPU 会把多个对 cache line 的 Store 操作的数据合并到 buffer 中，


## 耗叔感悟
程序的运行存在时间和空间上的局部性，前者是指只要内存中的值被换入缓存，今后一段时间内会被多次引用，后者是指该内存附近的值也被换入缓存。如果在编程中特别注意运用局部性原理，就会获得性能上的回报。

比如C语言中应该尽量减少静态变量的引用，这是因为静态变量存储在全局数据段，在一个被反复调用的函数体内，引用该变量需要对缓存多次换入换出，而如果是分配在堆栈上的局部变量，函数每次调用CPU只要从缓存中就能找到它了，因为堆栈的重复利用率高。

再比如循环体内的代码要尽量精简，因为代码是放在指令缓存里的，而指令缓存都是一级缓存，只有几K字节大小，如果对某段代码需要多次读取，而这段代码又跨越一个L1缓存大小，那么缓存优势将荡然无存。


# reference
Intel® 64 and IA-32 Architectures Software Developer Manual: Vol 3: Chapter 11 Memory Cache Control

https://mechanical-sympathy.blogspot.com/2011/07/write-combining.html

https://fgiesen.wordpress.com/2013/01/29/write-combining-is-not-your-friend/

[What Every Programmer Should Know About Memory](https://www.akkadia.org/drepper/cpumemory.pdf)