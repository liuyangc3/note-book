# Metrics

[monitoring_architecture](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/monitoring_architecture.md)

一般监控指标分为两类，系统指标 system metrics 和 服务指标 service metrics，系统指标就是通用的监控指标，而服务指标指的是应用内部定义的一些数据。

系统指标 system metrics 又被分为两类，core metrics 核心指标和 non-core metrics非核心指标。核心指标一般指cpu和内存使用，pod 和容器的disk使用，以及一些资源预估，pod和集群水平扩展指标。而非核心指标我们可以认为是不能被kubernetes理解的指标

服务指标作为HPA的输入，有时候被叫做custom metrics自定义指标. 


```
## Metrics server
Metrics server 前身是 Heapster。Kubernetes v1.8 开始，资源的使用情况可以通过API server 获取，
kubernetes 提供了 [Metrics API](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/#the-metrics-api), which is under /apis/metrics.k8s.io/ path。 metric-server 属于 core metrics(核心指标)，这些聚合过的数据将存储在内存中，且以 metric-api 的形式暴露出去 以此数据提供给 Dashboard、HPA、scheduler 等使用。

Metrics server 是一个 aggregation API server, 需要 kube-aggregator。

这部分曝露的指标 Resource Metrics API，而 Custom metrics API 由社区实现如
- Prometheus Adapter
- Microsoft Azure Adapter
- Google Stackdriver
- Datadog Cluster Agent


## kube state metrics
主要提供 object 级别的监控，例如

- 我调度了多少个replicas？现在可用的有几个？
- 多少个Pod是running/stopped/terminated状态？
- Pod重启了多少次？
- 我有多少job在运行中

https://github.com/kubernetes/kube-state-metrics

# monitor pipeline

## collector
cAdvisor 集成进 kubelet, 所以可以通过kubelet 采集系统监控数据

kubelet 提供 node/pod/container usage information

kubelet 同时也提供一个 HTTP API 服务，但是并没有文档 see [issue](https://github.com/kubernetes/kubernetes/issues/13470)

下面是几个endpoiont
```
http://localhost:10255/pods
http://localhost:10255/stats/summary
http://localhost:10255/metrics


# Book
https://yasongxu.gitbook.io/container-monitor/
