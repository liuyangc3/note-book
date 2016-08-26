## show arp
```shell
arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
172.16.1.24              ether   00:22:7b:10:35:f1   CM                    eth0
103.37.163.1             ether   00:00:5e:00:01:01   C                     eth1
```
```shell
arp -a
test-b.cloud.mos (172.16.1.24) at 00:22:7b:10:35:f1 [ether] PERM on eth0
? (103.37.163.1) at 00:00:5e:00:01:01 [ether] on eth1
```
这些内容来自 /proc/net/arp
```shell
cat /proc/net/arp
IP address       HW type     Flags       HW address            Mask     Device
172.16.1.24      0x1         0x6         00:22:7b:10:35:f1     *        eth0
103.37.163.1     0x1         0x2         00:00:5e:00:01:01     *        eth1
```

The definition of the `Flags Mask` is given in include/uapi/linux/if_arp.h
* 0x0 incomplete - I
* 0x2 complete - C
* 0x6 complete and manually set - CM

## set arp

arp -s <ip> <mac>
