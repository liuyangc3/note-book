Go 的内存分配器把内存分为 Mheap，MCache 和 MCentral 三个部分

MHeap 就是 Go 程序的堆，MCache 是为小对象分配的内存池，MCentral 是负责从 MHeap 分配和归还 MCache 的内容（newstack，morestack 和 lesstack 的操作）

每个线程对应一个MCache, Heap Central 所有线程共享

Goroutine 在初始化的时候是将 g.stack 和 g.stackGuard0 上下界指向从 MCache.stackcache 链表 分配来的小内存空间。只有大对象才会从 MHeap 分配。
Goroutine 的初始栈内存很小，一般都是从 MCache 分配来的。

Goroutine 需要栈扩容的时候，也是先从 MCache 中获取更大的内存对象，拷贝旧栈过去，修改 g.stack 的指向。

当 Goroutine 结束的时候他指向的内存对象就被放回 MCache.stackcache 的链表中，等待被别的操作使用。