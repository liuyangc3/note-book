free 命令展示
```
$ free -m
             total       used       free     shared    buffers     cached
Mem:          3832       2364       1467          0        173        672
-/+ buffers/cache:       1518       2314
Swap:            0          0          0
```
最后两列分别是 buffers 和 cached

他们是代表什么意思呢？

https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Deployment_Guide/s2-proc-meminfo.html
/proc/meminfo

* Buffers — The amount, in kibibytes, of temporary storage for raw disk blocks.
* Cached — The amount of physical RAM, in kibibytes, used as cache memory.

翻译过来就是
* Buffers — 一段裸设备块的临时存储空间
* Cached — 一段物理内存作为内存的缓存

解释得不够详细，


Unix 设计里有块设备缓存和文件缓存
文件缓存在Linux 的实现就是 VFS层的 page cache。

论文 https://www.usenix.org/legacy/event/usenix2000/freenix/full_papers/silvers/silvers_html/

buffer_head 结构保证了需要把 page 写入 disk 时，I/O 请求直接发给驱动，不用去找哪个 page

page cache 就不说了，下面主要讲讲 buffer

# buffer
从 free 命令的代码里(项目地址 http://procps.sourceforge.net) 可以得知命令的数值实际上是
从 /proc/meminfo 来的，而 meminfo 的数值是从系统调用 sysinfo 来的。

具体详情 http://blog.csdn.net/lux_veritas/article/details/19231993

文章里提到了一个函数 si_meminfo `mm/page_alloc.c`

```c
void si_meminfo(struct sysinfo *val)  
{  
        val->totalram = totalram_pages;  
        val->sharedram = 0;  
        val->freeram = global_page_state(NR_FREE_PAGES);  
        val->bufferram = nr_blockdev_pages();  
        val->totalhigh = totalhigh_pages;  
        val->freehigh = nr_free_highpages();  
        val->mem_unit = PAGE_SIZE;  
} 
```
可以看到 bufferram 的值是函数 nr_blockdev_pages() 得到的 `fs/block_dev.c`
```c
long nr_blockdev_pages(void)
{
	struct block_device *bdev;
	long ret = 0;
	spin_lock(&bdev_lock);
	list_for_each_entry(bdev, &all_bdevs, bd_list) {
		ret += bdev->bd_inode->i_mapping->nrpages;
	}
	spin_unlock(&bdev_lock);
	return ret;
}
```
可以看到这个函数其实就是，遍历了所有的块设备，然后把这些设备 bd_inode 上的 pages 数目加起来。

这些 page 由内核通过一颗 radix tree 来维护，而 nrpages 记录了tree pages 的数量。

buffer 统计的是所有block device 对应的inode的 address_space的 page的数量。

如何增加 buffers ?
```
cat /dev/sda1 > /dev/null 
```

所以可以确定的是直接访问 block 设备产生的 page cache是保存到 block device的 bd_inode 里面的。


