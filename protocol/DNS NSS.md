## Name Services
there were different mechanisms used to perform "human-readable name" -> "IP address" resolution。
DNS， or Sun's NIS and NIS+.


## Network Information Service
NIS 用来在网络上所有的主机间享信息，例如将以下信息由 NIS 维护：
* 登陆名/密码/home目录 (/etc/passwd)
* group 信息 (/etc/group)
如果你的密码条目保存在NIS的数据库，那么你就可以登陆网络内任意一台主机。

C 标准库实现了 NIS 和 NIS+ 

freebsd 的实现 https://www.freebsd.org/doc/handbook/network-nis.html
##  Name Service Switch

GNU C 库 支持名称解析的函数是 gethostbyname(), 或者 getaddrinfo()

http://lists.busybox.net/pipermail/busybox/2012-July/078123.html

当然这2个函数不是纯DNS实现，实际上会根据/etc/nsswitch.conf的配置先查看/etc/hosts 然后nis，最后才走 DNS。

GNU 管这个系统叫做 NSS。

许多C库函数需要配置后才能在本地环境里工作。大多情况的配置是由文件完成的(例如 /etc/passwd)，
但是有些 nameservices (例如NIS DNS)随着它们流行，通过固定的查询顺序，也侵入了 C 库。

对于这些问题 GNU C 库包含了一个干净的解决方案，它是由 Sun 公司在 Solaris 2 上涉及的一个方案， GNU C 库沿用了这个设计名字，
叫做 Name Service Switch NSS。GNU C 库 2.x 实现了 NSS，并且支持支持 NIS/NIS+ 映射。

NSS 基本的想法是把不同服务的信息放入数据库，通过不同的模块去访问数据库，这样做有以下好处
* 贡献者可添加新的 services 而不用把他们加入 GNU C 库。
* 模块可以单独更新。
* C 库镜像很小。

NSS 支持的数据有 (they are the maps provided by NIS.):
* aliases: Mail aliases.
* ethers: Ethernet numbers.
* group: Groups of users.
* hosts: Host names and numbers.
* netgroup: Network wide list of host and users.
* network: Network names and numbers.
* protocols: Network protocols.
* passwd: User passwords.
* rpc: Remote procedure call names and numbers.
* services: Network services.
* shadow: Shadow user passwords.


### /etc/nsswitch.conf
```
...
hosts:      files nisplus nis dns
```
查找主机名先走文件 /etc/hosts 再走NIS+和NIS 最后是 DNS 



# glibc dns 问题
2.9 版本 glibc 会同时发送 IPv4 and IPv6 lookups，在某些不支持 IPv6 的环境里会超时5s。
通过设置 single-request 来取消

single-request (since glibc 2.10)
                     Sets RES_SNGLKUP in _res.options.  By default, glibc
                     performs IPv4 and IPv6 lookups in parallel since
                     version 2.9.  Some appliance DNS servers cannot handle
                     these queries properly and make the requests time out.
                     This option disables the behavior and makes glibc
                     perform the IPv6 and IPv4 requests sequentially (at the
                     cost of some slowdown of the resolving process).



# reference
The Linux NIS(YP)/NYS/NIS+ HOWTO http://www.linux-nis.org/nis-howto/HOWTO/introduction.html

http://www.gnu.org/software/libc/manual/html_node/Name-Service-Switch.html


# DNS in java
http://blog.arganzheng.me/posts/java-dns-lookup-internal.html

JAVA 实现了 InetAddress Caching，如果有 cache 则从 cache 里取得数据，否则执行 getAddressesFromNameService

分为 IPv4 实现 http://hg.openjdk.java.net/jdk7u/jdk7u60/jdk/file/33c1eee28403/src/solaris/native/java/net/Inet4AddressImpl.c#l66
和 IPv6 实现 http://hg.openjdk.java.net/jdk7u/jdk7u60/jdk/file/33c1eee28403/src/solaris/native/java/net/Inet6AddressImpl.c#l66


举个IPv6的 例子

函数 lookupAllHostAddr 
```
Java_java_net_Inet6AddressImpl_lookupAllHostAddr(JNIEnv *env, jobject this,jstring host) {
...
    hostname = JNU_GetStringPlatformChars(env, host, JNI_FALSE);
...
    error = (*getaddrinfo_ptr)(hostname, NULL, &hints, &res);
```
getaddrinfo_ptr 是指针函数，用来从 hostname 获取 DNS

http://hg.openjdk.java.net/jdk7u/jdk7u60/jdk/file/33c1eee28403/src/solaris/native/java/net/net_util_md.c#l452
```
getaddrinfo_ptr = (getaddrinfo_f)
       JVM_FindLibraryEntry(RTLD_DEFAULT, "getaddrinfo");
```
指针函数指向了 getaddrinfo。JVM_FindLibraryEntry 是通过Linux dlsym() 来获取动态库的指针，
而 dlsym(RTLD_DEFAULT, name)中的  RTLD_DEFAULT 是指 “default library search order” 默认搜索顺序。


IPv4中使用 gethostbyname()函数完成主机名到地址解析，IPv6 则使用 getaddrinfo() 


