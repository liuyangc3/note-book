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

socket结构里成员sk指向sock
`include\linux\net.h`
```c
struct socket {
	struct file		*file;
	struct sock		*sk;
}
```
而 scok 的 sk_socket 同时指向 socket`include\net\sock.h`
```c
/*	@sk_socket: Identd and reporting IO signals */
struct sock {
...
  struct socket		*sk_socket;
...
}
```
什么不把两个数据结构合并成一个?

因为socket是inode结构中的一部分,而很多scok的信息在inode接口中是用不到的,如果全部放入socket,union就会变得很大，从而inode结构也会变得很大.

其他文件系统是不需要使用socket的,而系统中使用inode结构的数量要远远超过使用socket的数量,socket过大会造成巨大浪费.

所以 与 socket 相关内容分成两部分，把与文件系 统关系密切的放在socket结构中，把与通信关系密切的放在另一个单独结构sock中.


socket创建
----
```c
sockfd = socket(AF_INET, SOCKET_DGRM, 0);
```
这行代码大家都再熟悉不过了

总入口 进入 sys_socket
```
SYSCALL_DEFINE2(socketcall, int, call, unsigned long __user *, args)
{
...
  	case SYS_SOCKET:
		err = sys_socket(a0, a1, a[2]);
		break;
...
}
```
sys_socket 里 调用 sock_create 并返回一个fd
```c

SYSCALL_DEFINE3(socket, int, family, int, type, int, protocol)
{
	int retval;
	struct socket *sock;
	int flags;

	/* Check the SOCK_* constants for consistency.  */
	BUILD_BUG_ON(SOCK_CLOEXEC != O_CLOEXEC);
	BUILD_BUG_ON((SOCK_MAX | SOCK_TYPE_MASK) != SOCK_TYPE_MASK);
	BUILD_BUG_ON(SOCK_CLOEXEC & SOCK_TYPE_MASK);
	BUILD_BUG_ON(SOCK_NONBLOCK & SOCK_TYPE_MASK);

	flags = type & ~SOCK_TYPE_MASK;
	if (flags & ~(SOCK_CLOEXEC | SOCK_NONBLOCK))
		return -EINVAL;
	type &= SOCK_TYPE_MASK;

	if (SOCK_NONBLOCK != O_NONBLOCK && (flags & SOCK_NONBLOCK))
		flags = (flags & ~SOCK_NONBLOCK) | O_NONBLOCK;

	retval = sock_create(family, type, protocol, &sock);
	if (retval < 0)
		goto out;
    // 把创建的socket和文件描述符相关联
	retval = sock_map_fd(sock, flags & (O_CLOEXEC | O_NONBLOCK));
	if (retval < 0)
		goto out_release;

out:
	/* It may be already another descriptor 8) Not kernel problem. */
	return retval;

out_release:
	sock_release(sock);
	return retval;
}
```

sock_create 是 `__sock_create`的包装, struct socket
```c
static int __sock_create(int family, int type, int protocol,
			struct socket **res, int kern)
{
...
  sock_alloc(); // 完成了socket和inode节点的创建
...
// 根据协议族family得到struct net_proto_family结构，这个net_families数组在inet_init函数中初始化
  pf = rcu_dereference(net_families[family]);  
      err = -EAFNOSUPPORT;
      if (!pf)
          goto out_release;

      /*
       * We will call the ->create function, that possibly is in a loadable
       * module, so we have to bump that loadable module refcnt first.
       */
      if (!try_module_get(pf->owner))
          goto out_release;

      /* Now protected by module ref count */
      rcu_read_unlock();
      //  这里调用inet_create函数对INET协议族进行创建了庞大的struct sock 结构  
      err = pf->create(sock, protocol);
}
```
通过 sock_create 创建了socket和inode 然后根据协议族 调用inet_create 创建了sock

一些结构体的大致关系
```c
struct inode --> struct socket
                    ^     |
                    |     v
                  struct sock

struct raw_sock  对struct sock的扩展，ICMP协议就使用这种套接字
struct inet_sock 对sock的扩展, 添加了INET协议族层,第一个属性就是struct sock结构
struct udp_sock 是UDP协议套接字表示，其是对struct inet_sock套接字的扩展
struct inet_connetction_sock 可以认为是inet_sock的扩展,用于所有面向连接的协议
struct tcp_sock TCP协议,inet_connetction_sock的扩展,第一个属性就是struct inet_connection_sock inet_conn
```

其空间是不断增加的.所以，程序中给struct sock指针分配的不是该结构体的实际大小，而是大于其实际大小，以便其扩展套接字的属性占用。

所以tcp_sock是可以从sock强制转换而来.