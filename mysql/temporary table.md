http://mysql.taobao.org/monthly/2016/06/07/

max_heap_table_size Default Value (64-bit platforms)	16777216

当临时表数据量大于这个值， HEAP 表 会变为 onDISK 表

出现条件

1 SQL包含 SQL_BUFFER_RESULT

作用是将查询结果缓存到临时表中， 数据量很大，通过网络返回数据会很慢，使用临时表来减少读锁对表的占用时间。

2 SQL包含 DERIVED_TABLE
http://mysql.taobao.org/monthly/2017/03/05/

DERIVED_TABLE 是位于 FROM 里的子查询结果

3 SQL包含 DISTINCT