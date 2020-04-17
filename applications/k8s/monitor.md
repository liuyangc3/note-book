# metrics-server

[monitoring_architecture](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/monitoring_architecture.md)

metrics 被分为两类，core metrics 核心指标和 non-core metrics非核心指标。

核心指标一般指cpu和内存使用，pod 和容器的disk使用，以及一些资源预估，pod和集群水平扩展指标。

