每个打开的文件 socket都有一个file的数据结构表示,普通文件和socket用inode->u(union)中的各个成员来区别：
```c
struct inode {
	.....................
	union {
		struct ext2_inode_info ext2_i;
		struct ext3_inode_info ext3_i;
		struct socket socket_i;
		.....................
	} u;
};
```

而socket结构里成员sk指向sock
```c

```