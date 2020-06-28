```
---TRANSACTION 5937657, ACTIVE 58 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 4 lock struct(s), heap size 1184, 2 row lock(s), undo log entries 1
MySQL thread id 104676, OS thread handle 0x7fda94302700, query id 12750155 10.212.17.5 nxin_fund updating
update xxxx ......
------- TRX HAS BEEN WAITING 58 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 8 page no 58 n bits 560 index `uni_trans_account` of table `nxin_fund`.`nxin_fund_transinfo` trx id 5937657 lock_mode X locks rec but not gap waiting
Record lock, heap no 86 PHYSICAL RECORD: n_fields 2; compact format; info bits 0
 0: len 8; hex 3033353434303031; asc 03544001;;
 1: len 8; hex 00000000000017f1; asc         ;;
```

mysql tables in use 1, locked 1





`RECORD LOCKS space id 8` show which index of which table was locked