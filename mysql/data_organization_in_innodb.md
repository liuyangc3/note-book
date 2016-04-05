source : https://blogs.oracle.com/mysqlinnodb/entry/data_organization_in_innodb

数据在InnoDB的组织结构
==============

介绍
---
这篇文章主要介绍数据是如何在 InnoDB 存储引擎内组织的。

首先我们看一下InnoDB创建的文件，然后了解一下逻辑数据(如表空间，页，段和扩展)的组织结构。

然后分别解释它们的细节与之间的关系。最后，得到一个关于InnoDB存储引擎的层次结构鸟瞰图。


文件
---
MySQL 将所有的文件都保存在data目录，这个路径可以使用命令行参数-data-dir，或者指定在配置文件。默认情况下，当InnoDB舒适化时，会在data目录创建3个重要的文件 – ibdata1, ib_logfile0 and ib_logfile1。ibdata1 是系统和用户数据保存的文件，ib_logfile0 和 ib_logfile1 是 redo 日志文件.

数据文件 ibdata1 属于系统表空间(表空间id为0，space_id)。系统表空间可以拥有多个数据文件，从MySQL5.6起，只有系统表空间可以拥有多于1个的数据文件。其他的表空间只能有1ge数据文件，并且只有系统表空间可以拥有多个表，其他表空间只能有一个表。

数据文件和redo日志文件代表了内存中的 C 语言structure  `fil_node_t`。


表空间(tablespace)
---------------
默认情况下，InnoDB 仅使用一个表空间，叫做系统表空间，表空间id为0. 不过通过指定innodb_file_per_table 参数也可以使用多个表空间，MySQL5.6中这个参数默认是开启的，就是说每个表都有一个自己的表空间

表空间和数据文件的关系在源码(storage/innobase/fil/fil0fil.cc)的注释里有阐述:

```
A tablespace consists of a chain of files. The size of the files does not
have to be divisible by the database block size, because we may just leave
the last incomplete block unused. When a new file is appended to the
tablespace, the maximum size of the file is also specified. At the moment,
we think that it is best to extend the file to its maximum size already at
the creation of the file, because then we can avoid dynamically extending
the file when more space is needed for the tablespace.
```

其中最后一句话里的动态扩展仅针对redo 日志而不是数据文件。数据文件是动态扩展的，而redo日志是预分配的

尽管表空间可以有多个数据文件，这些文件被认为是链接在一起的一个大文件，所以表空间内文件的顺序是很重要的

页(pages)
--------
一个物理文件逻辑上被分为多个页，第一个数据文件的第一个页被标记为页号0，下一个页的页号为1，如此反复。一个表空间内的页有一个全局唯一标记,页号(page_number)，而每个表空间也有唯一编号(space_id)。
所以InnoDB内的页可以使用(space_id, page_no)来唯一标记，那么InnoDB内任意的位置就可以使用(space_id, page_no, page_offset)来表示，
page_offset 表示指定页的偏移字节数。

来自不同数据文件的页之间的关联，在源码的注释里写道：
```
A block's position in the tablespace is specified with a 32-bit unsigned integer.
The files in the chain are thought to be catenated, and the block corresponding
to an address n is the nth block in the catenated file (where the first block
is named the 0th block,and the incomplete block fragments at the end of files
are not taken into account).A tablespace can be extended by appending a
new file at the end of the chain.
```
这表明，所有数据文件的第一个页页号不是0，只有表空间内第一个数据文件的第一个页的页号才是0。

注释也提到page_no 是32位无符号整数,这是page_no保存在磁盘上的大小。

每个页都有一个头部(page_header_t)，细节请看Jeremy Cole's 的博客[The basics of InnoDB space file layout.](http://blog.jcole.us/2013/01/03/the-basics-of-innodb-space-file-layout/)

扩展(extents)
-----------
一个扩展是大小1M的连续页，定义如下
```
# define FSP_EXTENT_SIZE (1048576U / UNIV_PAGE_SIZE)
```
宏UNIV_PAGE_SIZE是一个编译时间常数，MySQL5.6起它是一个全局变量。扩展内页的数量取决于页的大小，默认情况下页大小16KB，那么一个扩展包含64个页。

页类型
---
一个页可以有多种用途，页的类型表明了页被使用的目的，每个页的类型被保存在页的头文件里，头文件的定义在`storage/innobase/include/fil0fil.h`
下面的表格描述了页类型的用途：
| Page Type | Description |
| ------------- | ------------- |
| FIL_PAGE_INDEX | The page is a B-tree node |
| FIL_PAGE_UNDO_LOG | The page stores undo logs |
|FIL_PAGE_INODE|contains an array of fseg_inode_t objects.|
|FIL_PAGE_IBUF_FREE_LIST|The page is in the free list of insert buffer or change buffer.|
|FIL_PAGE_TYPE_ALLOCATED|Freshly allocated page.|
|FIL_PAGE_IBUF_BITMAP|Insert buffer or change buffer bitmap|
|FIL_PAGE_TYPE_SYS|System page|
|FIL_PAGE_TYPE_TRX_SYS|Transaction system data|
|FIL_PAGE_TYPE_FSP_HDR|File space header|
|FIL_PAGE_TYPE_XDES||Extent Descriptor Page|
|FIL_PAGE_TYPE_BLOBUncompressed BLOB page|
|FIL_PAGE_TYPE_ZBLOB|First compressed BLOB page|
|FIL_PAGE_TYPE_ZBLOB2|Subsequent compressed BLOB page|


