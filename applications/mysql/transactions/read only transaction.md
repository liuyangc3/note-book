https://dev.mysql.com/doc/refman/5.7/en/innodb-performance-ro-txn.html


只读事务在innodb 避免了  transaction ID (TRX_ID field) 开销



innodb 会检测只读事务
1 开启 START TRANSACTION READ ONLY

2 autocommit is ON, 且statement 是 `"non-locking" SELECT statement`
```
SELECT ... FOR UPDAT  or LOCK IN SHARED MODE
```

3 事务未开启 READ ONLY 选项，但是没有更新和特定行锁,直到事务更新数据或得到锁前，它保持在只读事务模式



http://mysql.taobao.org/monthly/2015/04/01/
只读事务不使用临时表，则不需要分配 undo log 回滚段 
