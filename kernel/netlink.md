# netlink
netlink 是一个用于用户空间和内核通信的程序

netlink 使用socket发送消息，netlink 是面向 datagram (UDP)的. 所以 socket_type 只能是SOCK_RAW 或者 SOCK_DGRAM，
内核并不区分它们。

建立一个 socket 用于 netlink
```
fd = socket(AF_NETLINK, socket_type, netlink_family);
```
其中 netlink_family 表示内核端的处理模块


netlink_family
-------------------
* NETLINK_ROUTE 修改路由表，IP地址等。
* NETLINK_W1 GPIO用来拉高或者拉低某一根线的内核子系统，所以用户如果使用GPIO就可以不用动内核，直接在用户空间操作GPIO了。
* NETLINK_USERSOCK 用户端socket，处理netlink请求的程序就不是内核了，而是用户空间另外的一个进程。这个就是进程间通信(IPC)的另一种方案。由于是socket，
  一端可以监听，另一端发送的只要将发送的目标地址填充为目标进程的pid就好（netlink的发送地址不是ip编码的，而是pid等编码的）。
  这种IPC最牛逼的地方在于可以支持multicast，多播的通信。一个消息同时发送给多个接受者，但是普通的回环地址lo的socket通信也可以做到这一点。
* NETLINK_FIREWALL 和内核的 netfilter 的 ip_queue 模块沟通，ip_queue是netfilter提供的将网络数据包从内核传递到用户空间的方法，内核中要提供ip_q
  ueue支持，在用户层空间打开一个netlink的socket后就可以接受内核通过ip_queue所传递来的网络数据包，具体数据包类型可由iptables命令来确定，只要将规则动作设置为“-j QUEUE”即可。 
  之所以要命名为ip_queue，是因为这是一个队列处理过程，iptables规则把指定的包发给QUEUE是一个数据进入队列的过程，而用户空间程序通过netlink socket获取数据包进行裁定，结果返回内核，进行出队列的操作。 
  在iptables代码中，提供了libipq库，封装了对ipq的一些操作，用户层程序可以直接使用libipq库函数处理数据。 
* NETLINK_IP6_FW 与NETLINK_FIREWALL的功能一样，只是是专门针对ipv6的。
* NETLINK_INET_DIAG 就是同网络诊断模块通信使用的，最常用的是tcp_diag模块，可以获得tcp连接的最详细信息。
* NETLINK_NFLOG 将内核 netfilter 的日志发送到用户空间的方法。
* NETLINK_XFRM  与内核的ipsec子模块通信的机制。
* NETLINK_SELINUX 与内核 selinux 通信。
* NETLINK_ISCSI  open iscsi 的内核部分，通过iscsi可以组成iscsi网络，让你的网路存储系统high起来。
* NETLINK_AUDIT 与内核的audit模块通信。记录了一大堆事件。
* NETLINK_FIB_LOOKUP 用户可以自由的查询fib路由表了。fib是快速转发表，里面量很大，刷新比较快，服务于快速查找和快速转发，而不是服务于用户空间设置，用户空间设置使用的路由表是rib，在内核中rib会转化为fib。
* NETLINK_CONNECTOR 是内核端的模块如果想要使用netlink接口对用户提供服务，这个模块可以去注册一个netlink回调，用户空间使用这个子系统就可以连接到特定的内核模块。
* NETLINK_NETFILTER 用于控制netfilter的。
* NETLINK_DNRTMSG  DECnet的，大部分人用不到
* NETLINK_KOBJECT_UEVENT：sys子系统使用的uevent事件。内核内所有设备的uevent事件都会通过这个接口发送到用户空间
* NETLINK_GENERIC 这个也是内核模块用来提供netlink接口的方式。通过这种方式提供的接口都可以复用这一个子系统。
* NETLINK_CRYPTO 可以使用内核的加密系统或者修改查询内核的加密系统参数。

netlink 协议格式
----------
netlink 消息是一个字节流，它包含了一个或者多个消息头部(struct nlmsghdr),每个头部后是与其相关的载荷

消息头部 linux/netlink.h
```c
struct nlmsghdr
{
	__u32		nlmsg_len;	/* Length of message including header */
	__u16		nlmsg_type;	/* Message content */
	__u16		nlmsg_flags;	/* Additional flags */
	__u32		nlmsg_seq;	/* Sequence number */
	__u32		nlmsg_pid;	/* Sending process port ID */
};
```
nlmsg_len 表示头部和载荷一共的大小

nlmsg_type 表明载荷的类型

nlmsg_flags 表明数据的状态，netlink 有3种状态 request, reply, notify

```
0              1              2              3
  +--------------+--------------+--------------+--------------+ \
  |                    Total Message Length                   |  \
  +--------------+--------------+--------------+--------------+   \
  |             Type            |            Flags            |    \
  +--------------+--------------+--------------+--------------+     nlmsghdr
  |                      Sequence Number                      |    /
  +--------------+--------------+--------------+--------------+   /
  |                            PID                            |  /
  +--------------+--------------+--------------+--------------+ /
  |                            PAD                            |
  +--------------+--------------+--------------+--------------+
  |                          PayLoad                          |
  +--------------+--------------+--------------+--------------+
  |                            PAD                            |
  +--------------+--------------+--------------+--------------+
  |                            nlmsghdr                       |
  +--------------+--------------+--------------+--------------+
  |                            ...                            |
  +--------------+--------------+--------------+--------------+
 
```
















go test
```
package main

import (
    "github.com/vishvananda/netlink"
    "github.com/vishvananda/netlink/nl"
    "syscall"
)

const (
	TCPDIAG_GETSOCK = 18
	TCP_LISTEM = 1 << 10
	INET_DIAG_NOCOOKIE = ^uint(0)  // ~0U in C
)
```




参考
------
kernel Manual: http://stuff.onse.fi/man?program=netlink&section=7

libnl: http://www.infradead.org/~tgr/libnl/doc/core.html#core_msg_attr

ss source code: https://git.kernel.org/cgit/linux/kernel/git/shemminger/iproute2.git/tree/misc/ss.c

http://people.redhat.com/nhorman/papers/netlink.pdf

http://blog.csdn.net/ljy1988123/article/details/51025298


http://kristrev.github.io/2013/07/26/passive-monitoring-of-sockets-on-linux/

https://github.com/kristrev/inet-diag-example/blob/master/inet_monitor.c

go-lang version:

http://dtucker.co.uk/hack/taming-netlink.html

http://containerops.org/2014/07/30/tenus-golang-powered-linux-networking/
