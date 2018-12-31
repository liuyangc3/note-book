# free

经常会碰见这样的一个问题

free 命令展示
```
$ free -m
             total       used       free     shared    buffers     cached
Mem:          3832       2364       1467          0        173        672
-/+ buffers/cache:       1518       2314
Swap:            0          0          0
```
最后两列分别是 buffers 和 cached, 它们是代表什么意思呢？

free 命令来自 procps, 展示的数据来自 `/proc/meminfo`.

对于 `/proc/meminfo` redhat 文档中给出的了解释(详见https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Deployment_Guide/s2-proc-meminfo.html)

* Buffers — The amount, in kibibytes, of temporary storage for raw disk blocks.
* Cached — The amount of physical RAM, in kibibytes, used as cache memory.

从字面意思很难理解它们的区别.


# /proc/meminfo
`/proc/meminfo` 输出来自 `fs/proc/meminfo.c` 下的 `meminfo_proc_show()`

```c
/* https://github.com/torvalds/linux/blob/v4.20/fs/proc/meminfo.c#L48 */
...
// Cached
cached = global_node_page_state(NR_FILE_PAGES) -
			total_swapcache_pages() - i.bufferram;
...
//Buffers
show_val_kb(m, "Buffers:        ", i.bufferram);
```

`global_page_state(NR_FILE_PAGES)` 表示所有的缓存页(page cache)的总和, 即 Cached + Buffers + 交换区缓存(swap cache)

NR_FILE_PAGES 来自 vmstat[NR_FILE_PAGES]
```shell
# cat /proc/vmstat
...
nr_file_pages 774671
```

计算一下, 结果相等
```
# cat /proc/meminfo |grep -P 'Cache|Buffer'
Buffers:          246612 kB
Cached:          2849484 kB
SwapCached:         2588 kB

# Cached = total - SwapCached - Buffers 
774671 * 4 kB - 2588 - 246612 = 2849484 kB
```

# buffers
函数 si_meminfo `mm/page_alloc.c`

```c
/* https://github.com/torvalds/linux/blob/v4.20/mm/page_alloc.c#L4747 */
void si_meminfo(struct sysinfo *val)
{
	val->totalram = totalram_pages;
	val->sharedram = global_node_page_state(NR_SHMEM);
	val->freeram = global_zone_page_state(NR_FREE_PAGES);
-->	val->bufferram = nr_blockdev_pages(); <---------------
	val->totalhigh = totalhigh_pages;
	val->freehigh = nr_free_highpages();
	val->mem_unit = PAGE_SIZE;
}
```
可以看到 bufferram 的值是函数 nr_blockdev_pages() 得到的 `fs/block_dev.c`
```c
/* https://github.com/torvalds/linux/blob/v4.20/fs/block_dev.c#L912 */
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

# bdev
关于 `bdev->bd_inode->i_mapping->nrpages`, bdev 是 block_device, 即块设备,何理解?

首先它是对磁盘等存储设备的抽象, 在请求设备驱动前, kernel 收集,排序 I/O 请求,排序方式是通过IO调度算法来控制.

其次它以文件形式展示在文件系统, 如 /dev/sda1, 所以它会关联 inode, 可以看到结构体有 bd_inode 字段关联 inode
```c
https://github.com/torvalds/linux/blob/v4.20/include/linux/fs.h#L451
struct block_device {
	dev_t			bd_dev;  /* not a kdev_t - it's a search key */
	int			bd_openers;
	struct inode *		bd_inode;	/* will die */
```

块设备如何关联文件系统的inode?

块设备驱动调用 add_disk 函数注册磁盘, 内核用 gen_disk 来表示.

add_disk的职责之一是为块设备关联inode, 调用栈是 add_disk -> register_disk -> bdget_disk(disk, 0) -> bdget(dev_t dev)

在 bdget 里首先 通过 BDEV_I 从vfs inode 里得到 block_device, 然后创建 inode时,把 i_bdev 加入 inode

```c
/* https://github.com/torvalds/linux/blob/v4.20/fs/block_dev.c#L866 */
struct block_device *bdget(dev_t dev)
{
	struct block_device *bdev;
	struct inode *inode;

    // 分配一个新的 inode, 把 dev 写入 block_device->bd_dev, 
	inode = iget5_locked(blockdev_superblock, hash(dev),
			bdev_test, bdev_set, &dev);

    // 从 inode 获取 block_device
	bdev = &BDEV_I(inode)->bdev;

    // inode是新建的话，把 block_device 加入 inode
	if (inode->i_state & I_NEW) {
		...
		inode->i_bdev = bdev;
		...
```

fs/inode.c 中 `iget5_locked` 如果是新建inode,返回的 i_state 是 I_NEW  `inode->i_state = I_NEW`


BDEV_I 返回的是结构体 bdev_inode,它相当于一个粘合剂，把某个块设备描述符block_device和对应的inode结合起来.
这里 BDEV_I 是 container_of 的包装, container_of 含义见 文章结尾 Refs 4,

```
/* https://github.com/torvalds/linux/blob/v4.20/fs/block_dev.c#L39 */
struct bdev_inode {
	struct block_device bdev;
	struct inode vfs_inode;
};

static inline struct bdev_inode *BDEV_I(struct inode *inode)
{
	return container_of(inode, struct bdev_inode, vfs_inode);
}
```


如何增加 buffers ?


```
cat /dev/sda1 > /dev/null 
```

所以可以确定的是直接访问 block 设备产生的 page cache是保存到 block device的 bd_inode 里面的。


# Refs
1 http://link.zhihu.com/?target=http%3A//blog.csdn.net/lux_veritas/article/details/19231993

2 http://linuxperf.com/?p=32

3 https://yannik520.github.io/blkdevarch.html

4 https://stackoverflow.com/questions/15832301/understanding-container-of-macro-in-the-linux-kernel

https://www.kernel.org/doc/htmldocs/filesystems/API-iget5-locked.html