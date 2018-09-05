# mtr (mini-transactions) 

innodb 里对 page 的访问/修改都需要 mtr. 例如修改 page 时, 需要通过 mtr 写 redo log.

在代码中mtr 对应 struct mtr_t 结构体，其内部有一个局部 buffer，
它会将一组 log record 集中起来，然后批量写入 log buffer；mtr_t 的结构体如下所示：
```
// https://github.com/mysql/mysql-server/blob/8.0/storage/innobase/include/mtr0mtr.h
struct mtr_t {
  struct Impl {
    mtr_buf_t  m_memo;  // 由此mtr涉及的操作所造成的脏页列表
    mtr_buf_t  m_log;   // mtr的局部 buffer，记录log-records
    ...
  };
};
```
## log_write_requests metric

通常 一个 dml 语句 redo 操作会执行下面三个函数
```
mtr_start()
mlog_write()
mtr_commit() 
```

mtr_commit() 将 mtr log 写入 redo log buffer.
而 mtr_commit()  中的 log_buffer_reserve 增加了 log_write_requests, 
```
mtr_commit()                          提交mtr，对应了mtr_t::commit()@mtr0mtr.cc
 |-mtr_t::Command::execute()          执行，同样在mtr0mtr.cc文件中
   |-mtr_t::Command::prepare_write()  准备写入，会返回字节数
   |-log_buffer_reserve               分配空间, log_write_requests + 1
```


## log writer thread

log writer 后台线程负责把 log buffer 数据按照操作系统block大小(4KB)写入磁盘

当磁盘里写入了多个 write completed blocks , log_writes 就会加1

当然也有特殊情况,  last incomplete block 也会被写入磁盘, block 中没填满的地方补0, 也算一次 log_writes


```
log_writer                          The log writer thread co-routine.
  |-log_writer_write_buffer
    |-log_files_write_buffer        /* Do the write to the log files */

//innobase/log/log0write.cc#L1450
static void log_files_write_buffer(log_t &log, byte *buffer, size_t buffer_size,
                                   lsn_t start_lsn) {
...

  if (write_from_log_buffer) {
     // log_buffer 中有写满的 block
     ..
  } else {
      // log_buffer 没有写满的 block
      // 也会把 log_buffer 中 这个 incomplete block 的数据 copy 出来
      write_buf = log.write_ahead_buf;
      /* We write all the data directly from the write-ahead buffer,
      where we first need to copy the data. */
      copy_to_write_ahead_buffer(log, buffer, write_size, start_lsn,
                                checkpoint_no);
  }
  // 现在开始把 数据写入磁盘 
  /* Now, we know, that we are going to write completed
  blocks only (originally or copied and completed). */
  write_blocks(log, write_buf, write_size, real_offset); 
  // 增加 log_writes
  srv_stats.log_writes.inc();
```

那么与就是说,服务器只有1个事务要 commit 时, redo log buffer 没有写满 block 也是会进行磁盘写入的

## log_write_requests - log_write
MySQLTuner-perl 中有一个统计项是 log_write_requests - log_write

log_write_requests 可能会小于 log_write, 差值是负数

有个 issue 也提到过 https://github.com/major/MySQLTuner-perl/issues/182

这里模拟一下
```
localhost:testdb> SHOW GLOBAL STATUS like '%innodb_log%'; 
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| Innodb_log_waits          | 0     |
| Innodb_log_write_requests | 15    |
| Innodb_log_writes         | 20    |
+---------------------------+-------+
3 rows in set
Time: 0.013s

localhost:testdb>begin;
Query OK, 0 rows affected
Time: 0.001s
localhost:testdb>insert into test values(1, 'test');
Query OK, 1 row affected
Time: 0.002s

localhost:testdb> SHOW GLOBAL STATUS like '%innodb_log%'; 
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| Innodb_log_waits          | 0     |
| Innodb_log_write_requests | 15    |
| Innodb_log_writes         | 24    |
+---------------------------+-------+
```
事务不提交 是不会产生 mtr_commit() 的, 可以看到 log_write_requests 并没有增加

# refs

http://hedengcheng.com/?p=489

http://mysql.taobao.org/monthly/2015/05/01/

http://mysql.taobao.org/monthly/2017/10/03/

https://jin-yang.github.io/post/mysql-innodb-redo-log.html

https://dev.mysql.com/doc/dev/mysql-server/8.0.11/PAGE_INNODB_REDO_LOG_THREADS.html
