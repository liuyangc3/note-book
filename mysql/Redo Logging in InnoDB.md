source: https://blogs.oracle.com/mysqlinnodb/entry/redo_logging_in_innodb

翻译： web

介绍
---
InnoDB是一个通用引擎，平衡了性能和可靠性。它是一个事物引擎，完全实现了ACID，如同其他的关系型数据库一样。
可靠性通过redo日志保证。

这篇文章将浏览 InnoDB的 redo log 子系统，先看看如下细节：

* 全局日志系统 提供了访问重要数据结构和信息的能力
* mini-transaction (mtr)，使用了 redo 日志创建的记录
* 全局日志缓存，redo 日志从mini transaction缓存写入这里，缓存里的日志周期性的写入磁盘
* 磁盘上的redo日志是高层次的内部数据结构

我们将讨论LSN的概念，不同值的LSN如何实现write-ahead logging (WAL)。

Redo日志的产生
---------
[Data Organization in InnoDB]()
