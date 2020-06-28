when you did some DDL on a slave,the replication will stop.
```
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.xxx.xxx.xxx
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: binlog.001392
          Read_Master_Log_Pos: 322952270
               Relay_Log_File: relaylog.003062
                Relay_Log_Pos: 321553629
        Relay_Master_Log_File: binlog.001392
             Slave_IO_Running: Yes
            Slave_SQL_Running: No
...
                   Last_Errno: 1396
                   Last_Error: Error 'Operation DROP USER failed for 'test'@'%'' on query. Default database: ''. Query: 'drop user test@'%''
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 321553465
              Relay_Log_Space: 322952715
...
             Master_Server_Id: 2
                  Master_UUID: f4a94630-92f1-11e4-8665-105172262513
...
           Retrieved_Gtid_Set: f4a94630-92f1-11e4-8665-105172262513:50890936-411581385
            Executed_Gtid_Set: 12f7c5c4-d12d-11e4-9c31-10517226256b:1-27,
d2d7d8d9-9109-11e4-b9f6-10517226256b:1-30453942,
f4a94630-92f1-11e4-8665-105172262513:1-411579804
                Auto_Position: 1
1 row in set (0.00 sec)
```
we can found these info from above:
```
Slave_SQL_Running: No
Query: "drop user test@'%'"
Master_UUID: f4a94630-92f1-11e4-8665-105172262513
Executed_Gtid_Set: f4a94630-92f1-11e4-8665-105172262513:1-411579804
```
and we need to fix that

but sicnce `SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1` is no longger supported when GTID mode on.
we need anthoer way.

the next transactionid is 411579804 + 1 = 411579805,
so we can jump to next GITD postion commit an empty transaction to skip this transaction.

the GITD is represented as a pair of coordinates, separated by a colon character (:), as shown here:
```
GTID = source_id:transaction_id
```

The `source_id` identifies the originating server. Normally, the server's server_uuid is used for this purpose.
so the next GITD is `f4a94630-92f1-11e4-8665-105172262513:411579805`

let's do it：
```
# first thing need to stop salve
mysql> STOP SLAVE;
# then jump to next transactionid
mysql> set GTID_NEXT='f4a94630-92f1-11e4-8665-105172262513:411579805';
Query OK, 0 rows affected (0.00 sec)
# commit an empty transaction
mysql> begin;
Query OK, 0 rows affected (0.00 sec)
mysql> commit;
Query OK, 0 rows affected (0.00 sec)
mysql> SET GTID_NEXT="AUTOMATIC"; 
mysql> STRT SLAVE;

begin;
commit;
SET GTID_NEXT="AUTOMATIC"; 
```
check out:
```
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: binlog.001392
          Read_Master_Log_Pos: 339765828
               Relay_Log_File: relaylog.003063
                Relay_Log_Pos: 28046
        Relay_Master_Log_File: binlog.001392
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
...
```
works fine

also, you can do this by using a MySQL utils [mysqlslavetrx](https://dev.mysql.com/doc/mysql-utilities/1.6/en/mysqlslavetrx.html)

see also [gtids-concepts](https://dev.mysql.com/doc/refman/5.6/en/replication-gtids-concepts.html)

