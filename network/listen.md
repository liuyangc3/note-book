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
 
 
 sys_listen()
 ----
 `net/socket.c` 
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
    
    /* 通过文件描述符fd，找到对应的socket。 
     * 以fd为索引从当前进程的文件描述符表files_struct中找到对应的file实例， 
     * 然后从file实例的private_data成员中获取socket实例。 
     */
	sock = sockfd_lookup_light(fd, &err, &fput_needed);
	if (sock) {
		somaxconn = sock_net(sock->sk)->core.sysctl_somaxconn;
        // 这里可以看到 会先将backlog参数和系统内核参数somaxconn做比较
		if ((unsigned)backlog > somaxconn做比较)
			backlog = somaxconn;

		err = security_socket_listen(sock, backlog);
		if (!err)
            /* 
			 * 如果是TCP套接字SOCK_STREAM，sock->ops指向的是inet_stream_ops， 
			 * sock->ops是在inet_create()函数中初始化，所以listen接口 
			 * 调用的是inet_listen()函数。 
			 */  
			err = sock->ops->listen(sock, backlog);

		fput_light(sock->file, fput_needed);
	}
	return err;
}
```
sys_listen() 的逻辑如下:

1 先调用sockfd_lookup_light()通过文件描述符获取对应的socket实例

2 调整 backlog 值

3 根据socket的协议调用不同的listen

inet_listen()
----
先看看sock 的两个字段
```
/* 
 * @sk_ack_backlog: current listen backlog 
 * @sk_max_ack_backlog: listen backlog set in listen() 
 */  
struct sock {  
    ...  
    unsigned short sk_ack_backlog; /* 当前的backlog，当前全连接队列长度 */  
    unsigned short sk_max_ack_backlog; /* 参数的backlog，存在这里 */  
    ...  
};  
```

TCP协议的inet_listen()   `net/ipv4/af_inet.c `
```c

/*
 *	Move a socket into listening state.
 */
int inet_listen(struct socket *sock, int backlog)
{
	struct sock *sk = sock->sk;
	unsigned char old_state;
	int err;

	lock_sock(sk);

	err = -EINVAL;
	if (sock->state != SS_UNCONNECTED || sock->type != SOCK_STREAM)
		goto out;
	/* 
	 * 检查进行listen调用的传输控制块的状态。如果该传输控制块不在 
	 * 在TCPF_CLOSE或TCPF_LISTEN状态，则不能进行监听操作，返回 
	 * 相应错误码 
	 */  
	old_state = sk->sk_state;
	if (!((1 << old_state) & (TCPF_CLOSE | TCPF_LISTEN)))
		goto out;

	/* Really, if the socket is already in listen state
	 * we can only allow the backlog to be adjusted.
	 */
    /* 
	 * 如果传输控制块不在LISTEN状态，则调用inet_csk_listen_start() 
	 * 进行监听操作。最后，无论是否在LISTEN状态都需要设置传输控制块 
	 * 的连接队列长度的上限。从这里可以看出，可以通过调用listen() 
	 * 来修改最大连接队列的长度。 
	 */  
	if (old_state != TCP_LISTEN) {
		err = inet_csk_listen_start(sk, backlog);
		if (err)
			goto out;
	}
    
	sk->sk_max_ack_backlog = backlog;
	err = 0;

out:
	release_sock(sk);
	return err;
}
```
inet_listen() 检查了TCP state 并设置state 为 TCP_LISTEN, 然后将listen参数backlog 存入 sock->sk_max_ack_backlog,最后调用inet_csk_listen_start().

inet_csk_listen_start()
----
`net\ipv4\inet_connection_sock.c`
```c
int inet_csk_listen_start(struct sock *sk, const int nr_table_entries)
{
	struct inet_sock *inet = inet_sk(sk);
	struct inet_connection_sock *icsk = inet_csk(sk);
	int rc = reqsk_queue_alloc(&icsk->icsk_accept_queue, nr_table_entries);

	if (rc != 0)
		return rc;

	sk->sk_max_ack_backlog = 0;
	sk->sk_ack_backlog = 0;
	inet_csk_delack_init(sk);

	/* There is race window here: we announce ourselves listening,
	 * but this transition is still not validated by get_port().
	 * It is OK, because this socket enters to hash table only
	 * after validation is complete.
	 */
	sk->sk_state = TCP_LISTEN;
	if (!sk->sk_prot->get_port(sk, inet->num)) {
		inet->sport = htons(inet->num);

		sk_dst_reset(sk);
		sk->sk_prot->hash(sk);

		return 0;
	}

	sk->sk_state = TCP_CLOSE;
	__reqsk_queue_destroy(&icsk->icsk_accept_queue);
	return -EADDRINUSE;
}
```

