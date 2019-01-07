

# config 
harvester 打开文件, 读取最后一行后, 开始计时, `close_inactive` 时间到达后,关闭文件.


# nginx modules
es 安装模块
```
sudo bin/elasticsearch-plugin install ingest-geoip
sudo bin/elasticsearch-plugin install ingest-user-agent
```




添加额外的信息
```
processors:
- add_host_metadata:
    netinfo.enabled: false
```

# 文本格式处理
1 通过模块
```
./filebeat modules enable nginx
```
会加载 modules.d/nginx.yml

在配置里填写路径
```
- module: nginx
  access:
    var.paths: ["/var/log/nginx/access.log*"]
```


2 通过配置 ingest node 预处理文本

https://github.com/elastic/beats/blob/master/filebeat/module/nginx/access/ingest/default.json

# refs 
https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-getting-started.html

https://note.yuchaoshui.com/blog/post/yuziyue/filebeat-use-ingest-node-dealwith-log-then-load-into-elasticsearch

