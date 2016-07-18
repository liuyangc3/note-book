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
