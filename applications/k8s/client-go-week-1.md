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
就是http client 的封装， 代码中有几个小技巧

1. if else 的代码可读性, 当 err != nil 时, 逻辑相近的代码放到一起
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

2. 使用闭包处理 http response 逻辑，方便复用， 我提 issue 到 https://github.com/cloudnativeto/sig-k8s-source-code/issues/17

5.2.3
---
ClientSet 根据resource type生成出的代码没什么好说的

5.2.4
---
对于不是kubernetes内置资源例如CRD，使用 Unstructured 来把resource映射到go struct

Unstructured 可以很方便解构YAML格式的文本到 struct， 并且支持GVR GVK，如下面这个例子
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"

    "k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
    "k8s.io/apimachinery/pkg/runtime/serializer/yaml"
)

const dsManifest = `
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: example
  namespace: default
spec:
  selector:
    matchLabels:
      name: nginx-ds
  template:
    metadata:
      labels:
        name: nginx-ds
    spec:
      containers:
      - name: nginx
        image: nginx:latest
`

func main() {
    obj := &unstructured.Unstructured{}

    // decode YAML into unstructured.Unstructured
    dec := yaml.NewDecodingSerializer(unstructured.UnstructuredJSONScheme)
    _, gvk, err := dec.Decode([]byte(dsManifest), nil, obj)

    // Get the common metadata, and show GVK
    fmt.Println(obj.GetName(), gvk.String())

    // encode back to JSON
    enc := json.NewEncoder(os.Stdout)
    enc.SetIndent("", "    ")
    enc.Encode(obj)
}
```
