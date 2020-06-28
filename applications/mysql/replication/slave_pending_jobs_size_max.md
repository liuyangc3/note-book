slave_pending_jobs_size_max
-----
```
 show global variables like '%slave_pending_jobs_size_max%';
+-----------------------------+----------+
| Variable_name               | Value    |
+-----------------------------+----------+
| slave_pending_jobs_size_max | 16777216 |
+-----------------------------+----------+
1 row in set (0.00 sec)
```
它表示在多线程复制时，在队列中Pending的事件所占用的最大内存，默认为16M,过小会导致复制失败，如：
```
show slave status\G;
...
Last_SQL_Error: Cannot schedule event Query, relay-log name ./relay-log.000003, position 8786809 to Worker thread because its size 96041273 exceeds 16777216 of slave_pending_jobs_size_max.
```
调整大小即可
```
stop slave;
set global slave_pending_jobs_size_max=1024*1024*100;
start slave;
```

