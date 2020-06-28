# netlink
netlink 是一个用于用户空间和内核通信的程序

netlink 使用socket发送消息，netlink 是面向 datagram (UDP)的. 所以 socket_type 只能是SOCK_RAW 或者 SOCK_DGRAM，
内核并不区分它们。

建立一个 socket 用于 netlink
```
fd = socket(AF_NETLINK, socket_type, netlink_family);
```
其中 netlink_family 表示内核端的处理模块


# netlink_family
内核中已经存在基于 netlink 的具体协议有Linux/include/uapi/linux/netlink.h
```
NETLINK_ROUTE		0	/* Routing/device hook				*/
NETLINK_UNUSED		1	/* Unused number				*/
NETLINK_USERSOCK	2	/* Reserved for user mode socket protocols 	*/
NETLINK_FIREWALL	3	/* Unused number, formerly ip_queue		*/
NETLINK_SOCK_DIAG	4	/* socket monitoring				*/
NETLINK_NFLOG		5	/* netfilter/iptables ULOG */
NETLINK_XFRM		6	/* ipsec */
NETLINK_SELINUX		7	/* SELinux event notifications */
NETLINK_ISCSI		8	/* Open-iSCSI */
NETLINK_AUDIT		9	/* auditing */
NETLINK_FIB_LOOKUP	10	
NETLINK_CONNECTOR	11
NETLINK_NETFILTER	12	/* netfilter subsystem */
NETLINK_IP6_FW		13
NETLINK_DNRTMSG		14	/* DECnet routing messages */
NETLINK_KOBJECT_UEVENT	15	/* Kernel messages to userspace */
NETLINK_GENERIC		16
 room for NETLINK_DM (DM Events) */
NETLINK_SCSITRANSPORT	18	/* SCSI Transports */
NETLINK_ECRYPTFS	19
NETLINK_RDMA		20
NETLINK_CRYPTO		21	/* Crypto layer */
NETLINK_INET_DIAG	NETLINK_SOCK_DIAG /*  4 */
```

* NETLINK_ROUTE   修改路由表，IP地址等

* NETLINK_USERSOCK  用户端socket，处理netlink请求的程序就不是内核了，而是用户空间另外的一个进程。这个就是进程间通信(IPC)的另一种方案。由于是socket，
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
NETLINK_W1 GPIO用来拉高或者拉低某一根线的内核子系统，所以用户如果使用GPIO就可以不用动内核，直接在用户空间操作GPIO了。
```


# netlink 协议格式

每个netlink套接字也需要分配一个地址 sockaddr_nl 
```
struct sockaddr_nl {
    __kernel_sa_family_t	nl_family;	/* AF_NETLINK	*/
    unsigned short	nl_pad;		/* zero		*/
    __u32		nl_pid;		/* port ID	*/
    __u32		nl_groups;	/* multicast groups mask */
};
```
* nl_family netlik 总是 AF_NETLINK
* nl_pad 填充总是0
* nl_pid 0 表示内核处理或者多播消息，否则为处理消息的线程组id，nl_pid 并不是pid，它只是用于区分不同的接收者或发送者的一个标识,用户可以根据自己需要设置该字段。
* nl_groups 指定播组，bind 函数用于把调用进程加入到该字段指定的播组,若是为0表示不加入任何播组

netlink 消息是一个字节流，它包含了一个或者多个消息头部(struct nlmsghdr),
每个头部后是与其相关的载荷
```
<--- nlmsg_total_size(payload)  --->|
<-- nlmsg_msg_size(payload) -->|
nlmsg_data(nlh)->|
+----------+-----+-------------+----+----------+
| nlmsghdr | Pad |   Payload   |Pad | nlmsghdr | ...
+----------+-----+-------------+----+----------+



```

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
```
 0              1              2              3               4
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

nlmsg_len 表示头部和载荷一共的大小

nlmsg_type 表明载荷的类型 SOCK_DIAG_BY_FAMILY for v2

nlmsg_flags 表明数据的状态，linux/include/uapi/linux/netlink.h

```
NLM_F_REQUEST		1	/* It is request message. 	*/
NLM_F_MULTI		2	/* Multipart message, terminated by NLMSG_DONE */
NLM_F_ACK		4	/* Reply with ack, with zero or error code */
NLM_F_ECHO		8	/* Echo this request 		*/
NLM_F_DUMP_INTR		16	/* Dump was inconsistent due to sequence change */
NLM_F_DUMP_FILTERED	32	/* Dump was filtered as requested */
/* Modifiers to GET request */
NLM_F_ROOT      0x100   /* specify tree root    */
NLM_F_MATCH     0x200   /* return all matching  */
NLM_F_ATOMIC    0x400   /* atomic GET           */
NLM_F_DUMP      (NLM_F_ROOT|NLM_F_MATCH)
/* Modifiers to NEW request */
NLM_F_REPLACE   0x100   /* Override existing            */
NLM_F_EXCL      0x200   /* Do not touch, if it exists   */
NLM_F_CREATE    0x400   /* Create, if it does not exist */
NLM_F_APPEND    0x800   /* Add to end of list           */
```

* NLM_F_REQUEST 用于表示消息是一个请求，所有应用首先发起的消息都应设置该标志。
* NLM_F_MULTI 用于指示该消息是一个多部分消息的一部分，后续的消息可以通过宏NLMSG_NEXT来获得。
* NLM_F_ACK 表示该消息是前一个请求消息的响应，顺序号与进程ID可以把请求与响应关联起来。
* NLM_F_ECHO 表示该消息是相关的一个包的回传。
* NLM_F_ROOT 被许多 netlink 协议的各种数据获取操作使用，该标志指示被请求的数据表应当整体返回用户应用，而不是一个条目一个条目地返回。有该标志的请求通常导致响应消息设置NLM_F_MULTI标志。注意，当设置了该标志时，请求是协议特定的，因此，需要在字段 nlmsg_type 中指定协议类型。
* NLM_F_MATCH 表示该协议特定的请求只需要一个数据子集，数据子集由指定的协议特定的过滤器来匹配。
* NLM_F_ATOMIC 指示请求返回的数据应当原子地收集，这预防数据在获取期间被修改。
* NLM_F_DUMP NLM_F_ROOT 和 NLM_F_MATCH 缩写
* NLM_F_REPLACE 用于取代在数据表中的现有条目。
* NLM_F_EXCL_ 用于和 CREATE 和 APPEND 配合使用，如果条目已经存在，将失败。
* NLM_F_CREATE 指示应当在指定的表中创建一个条目。
* NLM_F_APPEND 指示在表末尾添加新的条目。


结构 struct iovec 用于把多个消息通过一次系统调用来发送，需要使用sendmsg
```c
struct iovec iov;
iov.iov_base = (void *)nlhdr;
iov.iov_len = nlh->nlmsg_len;
msg.msg_iov = &iov;
msg.msg_iovlen = 1;
sendmsg(fd, &msg, 0);
```




参考
------

https://www.ibm.com/developerworks/cn/linux/l-kerns-usrs/

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
