
# 指标

## RED
[1] Chapter 6 - Monitoring Distributed Systems 给出监控 The Four Golden Signals

see https://landing.google.com/sre/book/chapters/monitoring-distributed-systems.html#xref_monitoring_golden-signals

RED
在RED方法中，我们通过监控三项关键指标来管理架构中的每个微服务：

* (Request) Rate – 你的服务所服务的每秒的请求数
* (Request) Errors – 每秒失败的请求数
* (Request) Duration – 每个请求所花费的时间，用时间间隔表示

通过RED 检测到通常情况下会影响客户体验的问题

## USE(Utilization Saturation and Errors)
而如果关心性能问题，brendan gregg [2] 给出 USE 方法

* utilization - 使用率，是资源忙/闲时的百分比或者是资源总量的使用率。
* saturation - 饱和量，已经请求的、但是尚未处理的工作，通常是队列。
* errors - 错误，表示的是系统运转过程中也许无法侦测到的内部错误。


# refs

[1] https://landing.google.com/sre/book.html

[2] http://www.brendangregg.com/usemethod.html