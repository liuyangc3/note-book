http://mysql.taobao.org/monthly/2015/04/01/

当事务完成需要提交时，为了和BINLOG做XA，InnoDB的commit被划分成了两个阶段：prepare阶段和commit阶段

http://mysql.taobao.org/monthly/2015/12/01/
当开启binlog时, MySQL默认使用该隐式XA模式。 在5.7版本中，事务的提交流程包括：


Binlog Prepare 设置thd->durability_property= HA_IGNORE_DURABILITY, 表示在innodb prepare时，不刷redo log。

InnoDB Prepare （入口函数innobase_xa_prepare --> trx_prepare）： 更新InnoDB的undo回滚段，将其设置为Prepare状态（TRX_UNDO_PREPARED）。

进入组提交 (ordered_commit)



https://dev.mysql.com/doc/refman/5.7/en/xa.html

MySQL 的 XA 事务基于 X/Open CAE document Distributed Transaction Processing: The XA Specification

http://www.opengroup.org/public/pubs/catalog/c193.htm

内部 XA Binlog/XA 解决 binlog 和 redo log的一致性问题