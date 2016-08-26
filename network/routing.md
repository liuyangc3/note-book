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
this is local table on 172.16.1.24 eth0
```
broadcast 172.16.0.0  proto kernel  scope link  src 172.16.1.24 
local 172.16.1.24  proto kernel  scope host  src 172.16.1.24 
broadcast 172.16.255.255  proto kernel  scope link  src 172.16.1.24 
```
scopes defined in inlcude/linux/rtnetlink.h
```c
enum rt_scope_t {
  RT_SCOPE_UNIVERSE=0,
  /* User defined values */
  RT_SCOPE_SITE=200,
  RT_SCOPE_LINK=253,
  RT_SCOPE_HOST=254,
  RT_SCOPE_NOWHERE=255
};
```
* RT_SCOPE_UNIVERSE indicates that the destination address is not directly connected and it is more than one hop away.
* RT_SCOPE_SITE indicates an interior route within the site.
* RT_SCOPE_HOST indicates that the destination address is for the local host.
* RT_SCOPE_LINK indicates that the destination address is for the local network.
* RT_SCOPE_NOWHERE indicates that there is no route to the destination address.

### main table
The main table consists of all the normal routes, can be viewed by running these commands:
```shell
ip route show table
route - n
netstat - nr
```
and it can be manually configured.

## destination route lookup
The destination route lookup for the outgoing packet.it search route cache first, if no matching then search the FIB detabase.

net/ipv4/route.c `ip_route_output()` for resove routing enrty, it call `ip_route_output_key()` use a routing key(struct rt_key) to find routing cache entry in `rt_hash_table` first,if not found call `ip_route_output_slow()` to search the FIB database based on the input routing key.if the match entry is found, then create a new route cache entry.

