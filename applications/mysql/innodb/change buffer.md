https://dev.mysql.com/doc/refman/5.7/en/innodb-insert-buffering.html



The change buffer is a special data structure that caches changes to `secondary index` pages
when affected pages are not in the buffer pool.

Change buffer的主要目的是将对二级索引的数据操作缓存下来，以此减少二级索引的随机IO，并达到操作合并的效果。

二级索引(所有非主键/聚簇索引)