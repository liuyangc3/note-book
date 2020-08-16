https://github.com/kubernetes/sample-controller/blob/master/docs/controller-client-go.md

client-go 三个组件

* Reflector: A reflector 通过`ListAndWatch`函数 watches 特定类型的 (kind) Kubernetes API。 watch 可以针对内置资源或者自定义资源。当 reflector 通过watch API0接收到关于新资存在的源通知，他使用listing API获取最近新创建的对象，并通过`watchHandler`函数将他们放入 Delta 队列. 

* Informer: 从Delta获取对象. 目标是保存对象 base controller is to save the object for later retrieval, and to invoke our controller passing it the object.

* Indexer：将对象indexing

这么设计的意义是让 Client-go 通过增加一个二级缓存层，更快地返回 List/Get 请求的结果、减少对 Kubenetes API 的直接调用
