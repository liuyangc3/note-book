# install
```
wget http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/0.10.2.0/kafka_2.12-0.10.2.0.tgz
tar -xzf kafka_2.11-0.10.2.0.tgz
```

# config
log dir, in bin/kafka-run-class.sh 加入
```
LOG_DIR=/data0/logs
```
data log in config/server.properties
```
log.dirs=/data0/kafka-data
```
jvm options in bin/kafka-server-start.sh
```
if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
fi
```
```
# Memory options
if [ -z "$KAFKA_HEAP_OPTS" ]; then
  KAFKA_HEAP_OPTS="-Xmx256M"
fi

# JVM performance options
if [ -z "$KAFKA_JVM_PERFORMANCE_OPTS" ]; then
  KAFKA_JVM_PERFORMANCE_OPTS="-server -XX:+UseG1GC -XX:MaxGCPauseMillis=20 -XX:InitiatingHeapOccupancyPercent=35 -XX:+DisableExplicitGC -Djava.awt.headless=true"
fi
```


server
```
echo 'fs.file-max = 32000' >> /etc/sysctl.conf
```
```
mkdir -p /data0/{logs,kafka-data}
```






https://bigdata-ny.github.io/2016/12/05/kafka-cluster-optimize/

http://tech.meituan.com/kafka-fs-design-theory.html

http://www.jianshu.com/p/8689901720fd

https://bigdata-ny.github.io/2016/12/05/kafka-cluster-optimize/