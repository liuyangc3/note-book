orignal from https://liquidat.wordpress.com/2013/03/13/uuids-and-linux-everything-you-ever-need-to-know/

## Background
UUIDs are 128 bit long numbers represented by 32 hexadecimal digits described in [RFC4122](https://tools.ietf.org/html/rfc4122)


## Linux implementation and generation
In Linux UUIDs are generated in [/drivers/char/random.c?id=refs/tags/v3.8](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/char/random.c?id=refs/tags/v3.8)
and you can generate new ones via:

```shell
$ cat /proc/sys/kernel/random/uuid
f24c88ba-18e0-48f4-94a1-d6dec0639f19
```

There is also the library [libuuid](https://linux.die.net/man/3/libuuid) which is used by uuidgen and especially by the ext2/3/4 tools E2fsprogs to generate UUIDs:
```shell
$ uuidgen
f81cc383-aa75-4714-aa8a-3ce39e8ad33c
```

## PartUUID
[Using the New GUID Partition Table in Linux](https://www.linux.com/training-tutorials/using-new-guid-partition-table-linux-goodbye-ancient-mbr/)

