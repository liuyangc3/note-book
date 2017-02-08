#

处理器从内存读取操作数(operand)到缓存(L1,L2,L3),每次读取 cache line 大小，这个操作叫做 `cache line fill`.

内存里的操作数位置如果在缓存里，下次处理器访问操作数的时候，会直接从缓存读取，这个操作叫做 `cache hit`.


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



 
# Write Combining

## coherency
CPU 之间使用 coherency 协议来同步 cache 的数据。

## Write Combining
当CPU执行存储指令(store)时，它会尝试将数据写到离CPU最近的L1缓存。如果此时出现 Write miss，CPU会访问下一级缓存。
为了减少 Write Miss 带来的性能开销，英特尔以及其它厂商的 CPU 都会使用一种称为"write combining"的技术。





# reference
Intel® 64 and IA-32 Architectures Software Developer Manual: Vol 3: Chapter 11 Memory Cache Control
