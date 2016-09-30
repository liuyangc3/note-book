# snmp
## snmp 配置
```
yum install net-snmp
```

## 添加 snmp MIB 库
虽然net-snmp自带了一些标准的MIB，但是世界上支持snmp的设备有无数种，各厂家都有自己的定义，这些定义不可能都包含在net- snmp自带的MIB中，因此，想要正确轮询一个这样的设备，必须载入厂家自己的MIB文件。

首先需要确定net-snmp MIB库的路径
```
$ yum install net-snmp-devel
$ net-snmp-config --default-mibdirs
/root/.snmp/mibs:/usr/share/snmp/mibs
```
将厂商设备的MIB文件放到~/.snmp/mibs目录中

但是光复制过去还不能生效，net-snmp是不会自动加载所有在~/.snmp/mibs目录中的mib文件的

还需要修改配置文件，先查看配置文件路径
```
net-snmp-config --snmpconfpath 
/etc/snmp:/usr/share/snmp:/usr/lib/snmp:/root/.snmp:/var/net-snmp
```

在/etc/snmp/snmpd.conf中加入MIB Module名称，MIB Module名称一般是MIB文件的第一行
```
mibs +Module name
```

