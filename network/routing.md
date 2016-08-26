## routing talbe
Linux supports 255 routing talbes.By defualt, there are only local(id=255) and main(id=245) table are used by kernel.

More tables can be configured when policy routing is defined.

local routing talbe has highest priority.

in net/ipv4/fib_hash.c,function `fib_hash_init()` initializes and allocates a fib_table in the kernel. At least two fib_table instances(local, main) are present in the kernel.

### local table
The local table consists of routes to local and broadcast addresses. This table is maintained by the kernel automatically.

Any routing lookup request has to go through the local table first, and the significance of this table is to determine whether
a packet has to be delivered locally or has to be forwarded.

The local table is searched first for any routing lookup request, and this saves lookup time if the
packet has to be delivered locally and there is no need to search other tables.

The contents of the local table can be viewed by running the command:
``` shell
ip route show table local
```
### main table
The main table consists of all the normal routes, can be viewed by running these commands:
```shell
ip route show table
route - n
netstat - nr
```
and it can be manually configured.

## destination route lookup
The destination route lookup match route cache first, if not found then search the FIB detabase.
