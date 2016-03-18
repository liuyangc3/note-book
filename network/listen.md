listen函数
====
定义
>int listen(int sockfd, int backlog);
>
>Accept incoming connections and a queue limit for incoming connections. 
 
 这里backlog是完成三次握手,等待`accept`的队列
 
 listen()是由glibc提供，声明位于include/sys/socket.h中，实现位于sysdeps/mach/hurd/listen.c中
 
 用户空间实际上调用的是 sys_socketcall(),再由它调用相应的系统调用,sys_socketcall()实际上是所
有socket函数进入内核空间的共同入口。
 ```c
SYSCALL_DEFINE2(socketcall, int, call, unsigned long __user *, args)  
{  
   ...  
   switch(call) {  
        ...  
        case SYS_LISTEN:  
            err = sys_listen(a0, a1);  
            break;  
        ...  
    }  
    return err;  
}  
```
 
 
 sys_listen() `net/socket.c` 
```c
/*
 *	Perform a listen. Basically, we allow the protocol to do anything
 *	necessary for a listen, and if that works, we mark the socket as
 *	ready for listening.
 */

SYSCALL_DEFINE2(listen, int, fd, int, backlog)
{
	struct socket *sock;
	int err, fput_needed;
	int somaxconn;

	sock = sockfd_lookup_light(fd, &err, &fput_needed);
	if (sock) {
		somaxconn = sock_net(sock->sk)->core.sysctl_somaxconn;
        // 这里可以看到 会先将backlog参数和系统内核参数somaxconn做比较
		if ((unsigned)backlog > somaxconn做比较)
			backlog = somaxconn;

		err = security_socket_listen(sock, backlog);
		if (!err)
			err = sock->ops->listen(sock, backlog);

		fput_light(sock->file, fput_needed);
	}
	return err;
}
```