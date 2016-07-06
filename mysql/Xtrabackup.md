Percona XtraBackup 基于 InnoDB crash-recovery 机制. 本文大致描述其工作原理.

背景
---------
表数据/索引 保存在 `datadir`/`table`.ibd, (innodb_file_per_table=1)

Redo log 保存在 ib_logfile*

LSN 记录了 ib_logfile 中已写入的日志在该文件内的偏移量

Undo log 存放在 ibdata1

过程
-------
备份开始后 XtraBackup 进程内部启动2个线程:
* 先启动 Redo log 复制线程，从最新的 checkpoint 开始顺序 copy Redo log 到 xtrabackup_logfile
* 再启动 ibd 复制线程 copy 表 idb 文件

当 ibd 线程完成 copy 后，执行 FLUSH TABLES WITH READ LOCK (FTWRL), 开始备份非 InnoDB 文件(frm、MYD、MYI、CSV、opt、par...)

这时在输出中能看到其过程
```
xtrabackup: Creating suspend file '/backup_path/xtrabackup_suspended_2' with pid '6
9053'

160626 03:25:55  innobackupex: Continuing after ibbackup has suspended
160626 03:25:55  innobackupex: Executing FLUSH TABLES WITH READ LOCK...
160626 03:25:55  innobackupex: All tables locked and flushed to disk

160626 03:25:55  innobackupex: Starting to backup non-InnoDB tables and files
innobackupex: in subdirectories of '/<datadir>/'
innobackupex: Backing up files '/<database>/*.{frm,isl,MYD,MYI,MAD,MAI,MRG,TRG,TRN,ARM,ARZ,CSM,CSV,op
t,par}' (198 files)
innobackupex: Backing up files '/performance_schema/*.{frm,isl,MYD,MYI,MAD,MAI,MRG,TRG,TRN,ARM,ARZ,CSM
,CSV,opt,par}' (53 files)
```

非 InnoDB 文件备份完成后，进行所有日志(除binlog)的落盘 ` FLUSH NO_WRITE_TO_BINLOG ENGINE LOGS`
```
160626 03:26:00  innobackupex: Finished backing up non-InnoDB tables and files

160626 03:26:00  innobackupex: Executing FLUSH NO_WRITE_TO_BINLOG ENGINE LOGS...
160626 03:26:00  innobackupex: Waiting for log copying to finish
```

然后结束 Redo log 线程, 解锁 READ LOCK, 并将 binlog 的位置写入 xtrabackup_binlog_info
```
160626 03:26:01  innobackupex: All tables unlocked

innobackupex: Backup created in directory '/backup_path'
innobackupex: MySQL binlog position: GTID of the last change 'd2d7d8d9-9109-11e4-b9f6-10517226256b:1-30453942,
f4a94630-92f1-11e4-8665-105172262513:1-429765308'
```

最后输出备份成功信息
```
160626 03:26:01  innobackupex: Connection to database server closed
160626 03:26:01  innobackupex: completed OK!
```

xtrabackup_suspended_2 文件
------------------
在 XtraBackup 2.3 版本之前， 备份过程是通过一个 perl脚本 `innobackupex` 和 二进制文件 xtrabackup 进行，
innobackupex 用来备份非InnoDB数据, 他们之间通过 xtrabackup_suspended_2 文件进行通知。

在 2.3 后 innobackupex 功能全部集成到 xtrabackup 里面，为了使用上的兼容考虑，innobackupex 作为 xtrabackup 的一个软链。

Redo log 复制线程
-------
Xtrabackup 启动时会从Redo log file 中获取最近一次的 checkpoint 对应的log sequence number (LSN),
并且从这个LSN开始,把新写入的数据块复制到备份目录的 xtrabackup_logfile 文件.

如果是增量备份，比较表空间中每个页的 LSN 是否大于上次备份的 LSN，如果是，则备份该页并记录当前检查点的 LSN

这个过程持续到非 InnoDB 文件备份结束.

我们可以在输出中可以看到每次记录的 LSN 的信息
```
>> log scanned up to (1607459548622)
```


备份过程中,数据库并发写入很大时, xtrabackup_logfile 文件也会变得很大，会占用很多空间，这需要磁盘有足够的预留空间

如果是流式备份`--stream=tar` 或者远程备份`--remote-host`时，会将临时文件写入/tmp，可以指定参数`--tmpdir`,
以免把 /tmp 目录占满影响备份以及系统其它正常服务.

copy 日志文件的时候，每次读写512字节, 因为 ib_logfile 由连续的日志块组成，每个块大小为 512 字节

Redo log 线程结束时，将备份起始和结束时的 lsn 信息写入 xtrabackup_checkpoints 文件
```
xtrabackup: The latest check point (for incremental): '1607411118902'
xtrabackup: Stopping log copying thread.
.>> log scanned up to (1607461446006)

xtrabackup: Creating suspend file '/backup_path/xtrabackup_log_copied' with pid '69
053'
xtrabackup: Transaction log of lsn (1607410660445) to (1607461446006) was copied.
```

恢复时，还需要使用参数 apply-log 将 xtrabackup_logfile 中的内容写回数据文件，本质就是 InnoDB crash-recovery 机制.

idb 复制线程
--------
这里 Xtrabackup 并不是使用简单的文件复制，而是使用了跟 InnoDB 引擎同样的方式访问数据文件、数据字典，并以数据页为单位来进行 copy.

它的内部使用了 InnoDB 的 lib 库，lib 库使用读写方式(rw)打开数据文件的，因为正常情况下引擎是要写数据的.
所以 Xtrabackup 也是 rw 打开数据文件的，但它并不会修改数据.

在 copy 数据到备份目录的过程中, Xtrabackup 每次读取1M数据（即 64 个 page，不可配置）

每次当 1M 的数据读取完成后，Xtrabackup 会对这 1M 的数据进行扫描，并对内部每一个
page 使用 buf_page_is_corrupted() 函数进行验证，检查其是否损坏，如果page损坏了，对其重新读取并重新
验证。如果重读10次都失败了，那么本次备份失败。


日志中可以看到 ibd 复制的过程
```
[02] Copying ./<database>/<table>.ibd to /xtarbackup_path/2016-06-26_03-10-05/<database>/<table>.ibd
[02]        ...done
```


其他
----

--throttle 这个参数用来限制备份过程中每秒读写的 IO 次数，避免备份时IO过大影响数据库。

--parallel 可以并行备份，默认情况下 xtrabackup 备份时只会开启一个进程进行数据文件的备份，通过这个参数可以加速备份过程


如果是流式备份,可以通过管道使用 pv -L 10m 限制网络流量.

参考
----
https://www.percona.com/doc/percona-xtrabackup/2.4/how_xtrabackup_works.html

https://www.percona.com/doc/percona-xtrabackup/2.3/innobackupex/how_innobackupex_works.html

http://op.baidu.com/2014/07/xtrabackup%E5%8E%9F%E7%90%86%E5%8F%8A%E5%AE%9E%E6%96%BD/

https://ruiaylin.github.io/2014/05/22/xtrabackup/

http://mysql.taobao.org/monthly/2016/03/07/

http://highdb.com/how-innobackupex-works/
