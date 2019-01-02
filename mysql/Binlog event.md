https://dev.mysql.com/doc/internals/en/event-classes-and-types.html
https://dev.mysql.com/doc/internals/en/event-meanings.html

```c
enum Log_event_type {
  //   
  UNKNOWN_EVENT= 0, 
  // 写在每个 binlog 文件的开始
  START_EVENT_V3= 1,
  // updateing 语句完成时写入 
  QUERY_EVENT= 2, 
  // mysqld 停止时写入
  STOP_EVENT= 3, 
  // mysqld 切换到新 binlog 文件
  ROTATE_EVENT= 4, 
  // 当每个语句使用 AUTO_INCREMENT 列,或者 LAST_INSERT_ID() 函数
  // row-based 不使用这个
  INTVAR_EVENT= 5, 
  LOAD_EVENT= 6, 
  SLAVE_EVENT= 7, 
  CREATE_FILE_EVENT= 8, 
  APPEND_BLOCK_EVENT= 9, 
  EXEC_LOAD_EVENT= 10, 
  DELETE_FILE_EVENT= 11, 
  NEW_LOAD_EVENT= 12, 
  // 语句使用了 RAND() 函数
  RAND_EVENT= 13, 
  // 语句使用了用户变量
  // row-based 不使用这个
  USER_VAR_EVENT= 14, 
  FORMAT_DESCRIPTION_EVENT= 15, 
  // 事务commit 修改了表生成
  XID_EVENT= 16, 
  BEGIN_LOAD_QUERY_EVENT= 17, 
  EXECUTE_LOAD_QUERY_EVENT= 18, 
  //  row-based 使用, 这个event出现在每行操作前
  TABLE_MAP_EVENT = 19, 
  PRE_GA_WRITE_ROWS_EVENT = 20, 
  PRE_GA_UPDATE_ROWS_EVENT = 21, 
  PRE_GA_DELETE_ROWS_EVENT = 22, 
  
  // 这几个是 dml 相关
  WRITE_ROWS_EVENT = 23, 
  UPDATE_ROWS_EVENT = 24, 
  DELETE_ROWS_EVENT = 25, 
  
  INCIDENT_EVENT= 26, 
  HEARTBEAT_LOG_EVENT= 27, 
  IGNORABLE_LOG_EVENT= 28,
  ROWS_QUERY_LOG_EVENT= 29,
  WRITE_ROWS_EVENT = 30,
  UPDATE_ROWS_EVENT = 31,
  DELETE_ROWS_EVENT = 32,
  GTID_LOG_EVENT= 33,
  ANONYMOUS_GTID_LOG_EVENT= 34,
  PREVIOUS_GTIDS_LOG_EVENT= 35, 
  ENUM_END_EVENT 
  /* end marker */ 
};
```

TABLE_MAP_EVENT



Used for row-based binary logging. This event logs inserts of rows in a single table.



Used for row-based binary logging. This event logs updates of rows in a single table.



Used for row-based binary logging. This event logs deletions of rows in a single table.





v4 event structure:
```
+=====================================+
| event  | timestamp         0 : 4    |
| header +----------------------------+
|        | type_code         4 : 1    |
|        +----------------------------+
|        | server_id         5 : 4    |
|        +----------------------------+
|        | event_length      9 : 4    |
|        +----------------------------+
|        | next_position    13 : 4    |
|        +----------------------------+
|        | flags            17 : 2    |
|        +----------------------------+
|        | extra_headers    19 : x-19 |
+=====================================+
| event  | fixed part        x : y    |
| data   +----------------------------+
|        | variable part              |
+=====================================+
```

v4: Used in MySQL 5.0 and up


XXX_ROWS_EVENT

- WRITE_ROWS_EVENT

- UPDATE_ROWS_EVENT

- DELETE_ROWS_EVENT

关于增删改的操作，对应于最核心的  ，它记录了每一行数据的变化情况。而如何解析相关的数据，
是非常复杂的。


TABLE_MAP_EVENT

row-based 使用, 这个event出现在每行操作前,  将一个表结构映射为一个数字,
表结构包括了 数据库, 表名, 列信息


XID_EVENT

在事务提交时，不管是 Statement 还是 Row 模式的 Binlog，都会在末尾添加一个 XID_EVENT 事件代表事务的结束，里面包含事务的 ID 信息


QUERY_EVENT
 


QUERY_EVENT  代码类 Query_log_event

A Query event is written to the binary log whenever the database is modified on the master, unless row based logging is used.

主要用于记录修改数据库的 SQL 语句，MySQL 所有的 DDL 操作都记录在这个 event 里面。


Fixed data part:

- 4 bytes. The ID of the thread that issued this statement. Needed for temporary tables. This is also useful for a DBA for knowing who did what on the master.

- 4 bytes. The time in seconds that the statement took to execute. Only useful for inspection by the DBA.

- 1 byte. The length of the name of the database which was the default database when the statement was executed. 
This name appears later, in the variable data part. It is necessary for statements such as INSERT INTO t VALUES(1) 
that don't specify the database and rely on the default database previously selected by USE.

- 2 bytes. The error code resulting from execution of the statement on the master. Error codes are defined in include/mysqld_error.h. 0 means no error. How come statements with a nonzero error code can exist in the binary log? This is mainly due to the use of nontransactional tables within transactions. For example, if an INSERT ... SELECT fails after inserting 1000 rows into a MyISAM table (for example, with a duplicate-key violation), we have to write this statement to the binary log, because it truly modified the MyISAM table. For transactional tables, there should be no event with a nonzero error code (though it can happen, for example if the connection was interrupted (Control-C)). The slave checks the error code: After executing the statement itself, it compares the error code it got with the error code in the event, and if they are different it stops replicating (unless --slave-skip-errors was used to ignore the error).

- 2 bytes (not present in v1, v3). The length of the status variable block.





# insert
TABLE_MAP_EVENT 只用于 row模式

QUERY_EVENT  (begin) ROW_format 的 DML 的QUERY_EVENT 记录语句为BEGIN

WRITE_ROWS_EVENT  (insert/delete/update事件中不记录表的相关信息，因此每次DML操作都会产生一个TABLE_MAP_EVENT事件，其中存储了获取数据库名和表名)

XID_EVENT  说明commit