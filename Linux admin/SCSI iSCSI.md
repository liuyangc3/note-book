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