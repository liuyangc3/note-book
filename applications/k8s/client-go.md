5.2.1
----

ClientConfig 接口设计目标
1. 支持多集群配置
2. 支持从多渠道加载配置,如文件,环境变量,集群Pod内部

ClientConfig 有3个实现
1. DeferredLoadingClientConfig 则加入loader, 由loader从多渠道加载配置并做merge
2. DirectClientConfig merge后的config由这个struct具体实现, 验证认证信息
2. inClusterClientConfig 负责从k8s Pod环境内加载client配置


5.2.2
----


代码可读性, 当 err != nil 时, 逻辑相近的代码放到一起
```
// staging\src\k8s.io\client-go\rest\request.go
		resp, err := client.Do(req)
		updateURLMetrics(r, resp, err)
		if err != nil {
			r.backoff.UpdateBackoff(r.URL(), err, 0)
		} else {
			r.backoff.UpdateBackoff(r.URL(), err, resp.StatusCode)
		}
		if err != nil {
```

举个例子
```go
// before
if something {
  do logicA.part1
  do logicB
} else {
  do logicA.part2
}

// after
if something {
  do logicA.part1
} else {
  do logicA.part2
}

if something {
  do logicB
}
```
