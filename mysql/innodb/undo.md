http://mysql.taobao.org/monthly/2015/04/01/

用回滚段组织log

rseg 1~rseg 32这32个回滚段存放于临时表的系统表空间中（ibtmpl）

rseg33~ 则根据配置存放到独立undo表空间中（如果没有打开独立Undo表空间，则存放于ibdata中）


在InnoDB中，与之相关的还有undo tablespace, undo segment, undo slot, undo log这几个概念。
undo log是最小的粒度，所在的数据页称为undo page，然后若干个undo page构成一个undo slot。
一个事务最多可以有两个undo slot，一个是insert undo slot, 用来存储这个事务的insert undo，
里面主要记录了主键的信息，方便在回滚的时候快速找到这一行。另外一个是update undo slot，
用来存储这个事务delete/update产生的undo，里面详细记录了被修改之前每一列的信息，便于在读请求需要的时候构造。
1024个undo slot构成了一个undo segment。然后若干个undo segemnt构成了undo tablespace。


MySQL 5.6对于没有显示指定READ ONLY事务，默认为是读写事务。在事务开启时刻分配trx_id和回滚段，并把当前事务加到trx_sys的读写事务数组中。

5.7 所有事务默认为只读事务
对于只读事务，如果产生对临时表的写入，则需要为其分配回滚段，使用临时表回滚段（第1~32号回滚段），不需要 TRX_ID 开销

只读事务变为读写事务时，则转换成读写模式，并为其分配事务ID和回滚段


事务修改的行内，聚集索引上 DB_TRX_ID 和DB_ROLL_PTR 记录当前事务id和回滚段地址

二级索引 page header 中有一个MAX_TRX_ID ， 事务修改修改该page的最大事务id，


可见性判断
Read View: 用于一致性读的snapshot，InnoDB里称为视图；在需要一致性读时开启一个视图，记录当时的事务状态快照，包括当时活跃的事务ID以及事务ID的上下水位值，以此用于判断数据的可见性。


http://mysql.taobao.org/monthly/2018/03/01/
