How works
-------
主机和磁盘SCSI接口通过 INQUIRY 指令沟通

SCSI initiator, 初始化一个 session, 并在 session 中发送 SCSI command

SCSI target, 等待 initiator command，一般提供 LUN 设备

Inquiry Command Example
----------
SCSI-2 specification (for details refer to the SCSI-2 standard).
```
                             Table 44: INQUIRY Command
+=====-========-========-========-========-========-========-========-========+
|  Bit|   7    |   6    |   5    |   4    |   3    |   2    |   1    |   0    |
|Byte |        |        |        |        |        |        |        |        |
|=====+=======================================================================|
| 0   |                           Operation Code (12h)                        |
|-----+-----------------------------------------------------------------------|
| 1   | Logical Unit Number      |                  Reserved         |  EVPD  |
|-----+-----------------------------------------------------------------------|
| 2   |                           Page Code                                   |
|-----+-----------------------------------------------------------------------|
| 3   |                           Reserved                                    |
|-----+-----------------------------------------------------------------------|
| 4   |                           Allocation Length                           |
|-----+-----------------------------------------------------------------------|
| 5   |                           Control                                     |
+=============================================================================+
```
and output data 
```
 
 Table 45: Standard INQUIRY Data Format
+=====-========-========-========-========-========-========-========-========+
|  Bit|   7    |   6    |   5    |   4    |   3    |   2    |   1    |   0    |
|Byte |        |        |        |        |        |        |        |        |
|=====+==========================+============================================|
| 0   | Peripheral Qualifier     |           Peripheral Device Type           |
|-----+-----------------------------------------------------------------------|
| 1   |  RMB   |                  Device-Type Modifier                        |
|-----+-----------------------------------------------------------------------|
| 2   |   ISO Version   |       ECMA Version       |  ANSI-Approved Version   |
|-----+-----------------+-----------------------------------------------------|
| 3   |  AENC  | TrmIOP |     Reserved    |         Response Data Format      |
|-----+-----------------------------------------------------------------------|
| 4   |                           Additional Length (n-4)                     |
|-----+-----------------------------------------------------------------------|
| 5   |                           Reserved                                    |
|-----+-----------------------------------------------------------------------|
| 6   |                           Reserved                                    |
|-----+-----------------------------------------------------------------------|
| 7   | RelAdr | WBus32 | WBus16 |  Sync  | Linked |Reserved| CmdQue | SftRe  |
|-----+-----------------------------------------------------------------------|
| 8   | (MSB)                                                                 |
|- - -+---                        Vendor Identification                    ---|
| 15  |                                                                 (LSB) |
|-----+-----------------------------------------------------------------------|
| 16  | (MSB)                                                                 |
|- - -+---                        Product Identification                   ---|
| 31  |                                                                 (LSB) |
|-----+-----------------------------------------------------------------------|
| 32  | (MSB)                                                                 |
|- - -+---                        Product Revision Level                   ---|
| 35  |                                                                 (LSB) |
|-----+-----------------------------------------------------------------------|
| 36  |                                                                       |
|- - -+---                        Vendor Specific                          ---|
| 55  |                                                                       |
|-----+-----------------------------------------------------------------------|
| 56  |                                                                       |
|- - -+---                        Reserved                                 ---|
| 95  |                                                                       |
|=====+=======================================================================|
|     |                       Vendor-Specific Parameters                      |
|=====+=======================================================================|
| 96  |                                                                       |
|- - -+---                        Vendor Specific                          ---|
| n   |                                                                       |
+=============================================================================+
```

LUN Logical Units
-----------

每个 target 至少有一个 logical unit, 编号从0开始.LUN 最大为8个. 通常 LUN 映射到 peripheral devices.

通过 INQUIRY command, initiator 可以决定 target 是否实现 LUN

并且检查指令返回的 peripheral qualifier 和 peripheral device type


SCSI Peripheral Device Type
-------
用来描述一个 SCSI device

https://en.wikipedia.org/wiki/SCSI_Peripheral_Device_Type
```
00h - 直接存取装置（direct-access device，像磁盘机）
01h - 循序存取装置（sequential-access device，像软驱）
02h - 打印装置(printer device)
03h - 处理器装置(processor device)
04h - 一次写入装置(write-once device)
05h - 光驱(CDROM device)
06h - 扫描器(scanner device)
07h - 光学可读写装置（optical memory device，像一些CD-RAM）
08h - 多媒体点唱机（medium Changer 投币式点唱机jukeboxes）
09h - 通讯装置(communications device)
0Ah-0Bh - defined by ASC IT8 (Graphic arts pre-press devices)
0Ch - 磁盘阵列控制装置（Storage array controller device，像RAID）
```


Peripheral Qualifier (PQ) Definition
-------------
```
+=========-===================================================================+ 
|Qualifier|  Description                                                      |
|---------+-------------------------------------------------------------------|
|   000b  |  The specified peripheral device type is currently connected to   |
|         |  this logical unit.  If the target cannot determine whether or    |
|         |  not a physical device is currently connected, it shall also use  |
|         |  this peripheral qualifier when returning the INQUIRY data.       |
|         |  This peripheral qualifier does not mean that the device is ready |
|         |  for access by the initiator.                                     |
|         |                                                                   |
|   001b  |  The target is capable of supporting the specified peripheral     |
|         |  device type on this logical unit;  however, the physical device  |
|         |  is not currently connected to this logical unit.                 |
|         |                                                                   |
|   010b  |  Reserved                                                         |
|         |                                                                   |
|   011b  |  The target is not capable of supporting a physical device on     |
|         |  this logical unit. For this peripheral qualifier the peripheral  |
|         |  device type shall be set to 1Fh to provide compatibility with    |
|         |  previous versions of SCSI.  All other peripheral device type     |
|         |  values are reserved for this peripheral qualifier.               |
|         |                                                                   |
|   1XXb  |  Vendor-specific                                                  |
+=============================================================================+ 
```
and from linux kernel drivers/scsi/scsi_scan.c
```
For a peripheral qualifier (PQ) value of 1 (001b), the SCSI spec says:
The device server is capable of supporting the specified peripheral device type on this logical unit.
However, the physical device is not currently connected to this logical unit.

For a Peripheral qualifier 3 (011b), the SCSI spec says: 
The device server is not capable of supporting a physical device on this logical unit.
```

大致就是

 
PQ = 0 表示 LUN 有设备类型,但是 target 不知道物理设备连上没，initiator 还不能访问设备
 
PQ = 1 表示 target 支持 LUN上的 Peripheral Device Type(设备类型)，但是 物理设备还没连到 LUN 上

PQ = 3 LUN 上的物理设备不被 target 支持


connect 到 target 后, dmesg 里 可以看到的 PQ
```
scsi 14:0:0:0: Direct-Access     HUAWEI   S5500T           4202 PQ: 1 ANSI: 6
scsi 14:0:0:0: Attached scsi generic sg8 type 0
scsi 14:0:0:1: Direct-Access     HUAWEI   S5500T           4202 PQ: 0 ANSI: 6
```


iSCSI Initiator Creation
---------------
Install iscsi-initiator-utils.
```
yum install iscsi-initiator-utils
```
Discover the target. Use the target's IP address, the one used below serves only as an example.
```
~]# iscsiadm -m discovery -t sendtargets -p 192.168.1.1
Starting iscsid:     [ OK ]
192.168.1.1:3260,1 iqn.2015-06.com.example.test:target1
```
it shows target's IQN address

Connect to the target.
```
iscsiadm -m node -T iqn.2015-06.com.example:target1 --login
iscsiadm -m node -T iqn.2015-06.com.example:target1 --op=update --name=node.startup --value=automatic
```


Find the iSCSI disk name. 
```
grep -i "Attached SCSI" /var/log/messages
Jul  7 11:11:06 bj-yz-mysql02 kernel: sd 21:0:0:1: Attached scsi generic sg17 type 0
Jul  7 11:11:06 bj-yz-mysql02 kernel: sd 21:0:0:1: [sdm] Attached SCSI disk
```
or
```
yum install lsscsi
lsscsi
[20:0:0:1]   disk    HUAWEI   S5500T           4202  /dev/sdm 
```


mutipath
------
```
yum -y install device-mapper-multipath
```

find disk wwid
```
scsi_id -g -u /dev/sdm
360a9800044356546542b464e68395436
```

generate a config file `/etc/multipath.conf`
```
mpathconf --enable
```
modified config file
```
defaults {
        user_friendly_names yes
        find_multipaths yes   # 相同的路径合并
        path_grouping_policy multibus # 同时使用多条路径进行IO
        failback immediate   # 切换策略立刻
        no_path_retry fail
}

# add wwid
multipaths {
    multipath {
        wwid 360a9800044356546542b464e68395436
        alias data0
              }
}
```

start multipath
```
chkconfig multipathd on
service multipathd start
```



参考
-------
http://www.tldp.org/HOWTO/archived/SCSI-Programming-HOWTO/SCSI-Programming-HOWTO-9.html

http://www.staff.uni-mainz.de/tacke/scsi/SCSI2-08.html
