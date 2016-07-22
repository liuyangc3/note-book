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
















code
----------
netlink use inet_diag for TCP_LISTEN
```
/*
    use inet_diag_rev v1, only support kernel 2.6.32 
    author: web <liuyangc33@gmail.com>

*/

#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <linux/inet_diag.h>
#include <linux/netlink.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {
    int fd;
    fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_INET_DIAG);

    // bind
    struct sockaddr_nl bind_nladdr = {
            .nl_family = AF_NETLINK,
            .nl_pid    = getpid(),
    };

    if(bind(fd, (struct sockaddr *)&bind_nladdr, sizeof(bind_nladdr)) < 0) {
        perror("can't bind socket\n");
        return -1;
    }


    // netlink request
    struct sockaddr_nl nladdr = {
            .nl_family = AF_NETLINK,
            .nl_pid    = 0,         /* kernel */
    };

    struct {
        struct nlmsghdr nlh;
        struct inet_diag_req r;
    } req = {
            .nlh = {
                    // NLMSG_ALIGN(NLMSG_LENGTH(sizeof(req)))
                    .nlmsg_len   = sizeof(req),
                    .nlmsg_type  = TCPDIAG_GETSOCK,
                    .nlmsg_flags = NLM_F_REQUEST | NLM_F_DUMP,
                    .nlmsg_seq   = 1,
            },
            .r = {
                    .idiag_family = AF_INET,
                    .idiag_states = (1 << 10), // TCP_LISTEN
                    .id = {
                            .idiag_cookie[0] = INET_DIAG_NOCOOKIE,
                            .idiag_cookie[1] = INET_DIAG_NOCOOKIE,
                    },
            },
    };

    struct iovec iov_s[1] = {
        [0] = {
                .iov_base = &req,
                .iov_len  = sizeof(req),
        },
    };

    struct msghdr msg_s = {
            .msg_name    = &nladdr,
            .msg_namelen = sizeof(nladdr),
            .msg_iov     = iov_s,
            .msg_iovlen  = 1,
    };


    // send netlink request
    if (sendmsg(fd, &msg_s, 0) < 0) {
        perror("socket send error\n");
        return -1;
    }

    // receive netlink request
    int len;
    char buff[16384];
    char ip[1024];

    struct iovec iov_r[1] = {
                [0] = {
                        .iov_base = buff,
                        .iov_len  = sizeof(buff),
                },
    };

    struct msghdr msg_r = {
            .msg_name    = &nladdr,
            .msg_namelen = sizeof(nladdr),
            .msg_iov     = iov_r,
            .msg_iovlen  = 1,
    };
    
    while (1) {
        if( (len = recvmsg(fd, &msg_r, 0)) < 0) {
            close(fd);
            fprintf(stderr, "recv error\n");
            return -1;
        }

        struct nlmsghdr *h = (struct nlmsghdr *)buff;

        if (h->nlmsg_type == NLMSG_ERROR) {
            struct nlmsgerr *err = NLMSG_DATA(h);
            errno = -err->error;
            fprintf(stderr, "nlmsg error %s\n", strerror(errno));
            close(fd);
            return -1;
        }
        if (h->nlmsg_type == NLMSG_DONE) {
            close(fd);
            return 0;
        }
        
        // parse msg data 
        struct inet_diag_msg *r = NLMSG_DATA(h);

        printf("%s:%d\n",
               inet_ntop(r->idiag_family, &r->id.idiag_src, ip, sizeof(ip)),
               ntohs(r->id.idiag_sport));
        
        h = NLMSG_NEXT(h, len);
    }
        return 0;
}
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
