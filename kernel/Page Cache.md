在2.2x时期,page cache和buffer cache是两套cache系统，之间有同步.
到了2.4.x事情已经变得不是这样了,dd if=/dev/hda1 从buffer cache中获取数据,
open打开的普通文件缓冲到page cache,
两者没有任何同步机制(meta data还是一致的). 合适的次序下,得到的结果不能保证正确性.

到了2.5,文件的meta data移到了page cache.

在2.6的内核中page cache和buffer cache进一步结合,buffer cache 消失,只有page cache了.
 
 buffer cache退化为一个纯粹的io entry.随了linus的心愿.


# page descriptors
物理页框的状态信息保存在 page descriptor 里, 内核用 struct page(linux/mm.h)结构表示系统中的每个物理页
```c
struct page {
    ...
    _count;  // 被引用次数
    struct address_space *mapping; // 当页被插入 page cache，或者隶属于 anonymous region 时才被使用
    pgoff_t index;                 // page cache 里 owner 数据在页框内的偏移量
    ...
}
```
_count -1 表示页是自由的，可以分配给进程和内核，


# page cache
传统上 read() write() 文件操作依赖于 page cache，除非设置了 O_DIRECT，



根据 给定 owner(文件，块设备，swap等) 快速定为到相关的页数据，



跟踪记录缓存中的每个页如何被读写，因为文件数据页，块设备数据页，swap页的读写方式都是不同的

page cache 的核心数据结构是 address_space，它被嵌入在 struct page 里，



