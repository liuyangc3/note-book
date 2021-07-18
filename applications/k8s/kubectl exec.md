```
+---------+           +------------+    +---------+          +------------+          +------------------------+
| kubectl | - SPDY -> | API server | -> | kubelet | - CRI -> | containerd | - OCI -> |  runc  -> libcontainer |
+---------+           +------------+    +---------+          +------------+          +------------------------+
```

exec 实现原理是通过 setns 系统调用进入到 容器的 namespace， exec 创建一个新进程

这里面 setns 还是用 C 语言实现的，需要进程在启动 runtime 多线程环境之前完成 setns 相关操作。

原因是 gorutine 只能当前线程受到系统调用的影响
> The syscall is doing what it advertises: it invokes
the Linux system call.  And the Linux system call only
affects the calling thread (!), confirmed by reading the
sources.

https://github.com/golang/go/issues/1435#issuecomment-66054163
