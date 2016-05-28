set config file
---------------
create java.env in conf dir
```
export JVMFLAGS="-Xmx3072m"
```
set 3GB on a 4GB machine

log rotate


1 modify conf/log4j.properties 
```
zookeeper.root.logger=INFO, ROLLINGFILE
log4j.appender.ROLLINGFILE=org.apache.log4j.DailyRollingFileAppender
log4j.appender.ROLLINGFILE.DatePattern='.'yyyy-MM-dd
# if dont want a adily rolling 
log4j.appender.ROLLINGFILE.MaxFileSize=40MB

log4j.appender.ROLLINGFILE.MaxBackupIndex=20
```

2 set log path
create conf/zookeeper-env.sh
```
ZOO_LOG4J_PROP=INFO,ROLLINGFILE"

# Open JMX
JMXPORT=10053
```

zoo.cfg
-------
```
skipACL=yes  # skip ACL

```
auto purge log, this is enable by default




