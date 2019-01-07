# config 
harvester 打开文件, 读取最后一行后, 开始计时, `close_inactive` 时间到达后,关闭文件.

close_inactive 应设置为日志切割周期

# support nginx modules
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
通过 nginx 模块
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

如果日志有自定义格式,需要通过配置 ingest node `grok` 预处理文本, 位置 /etc/filebeat/module.d 

默认配置 https://github.com/elastic/beats/blob/master/filebeat/module/nginx/access/ingest/default.json

# refs 
https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-getting-started.html

https://www.elastic.co/guide/en/beats/devguide/current/filebeat-modules-devguide.html

https://www.elastic.co/guide/en/elasticsearch/reference/current/grok-processor.html

https://note.yuchaoshui.com/blog/post/yuziyue/filebeat-use-ingest-node-dealwith-log-then-load-into-elasticsearch

