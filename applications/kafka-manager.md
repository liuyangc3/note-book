下载
```
git clone https://github.com/yahoo/kafka-manager.git
cd kafka-manager
```
支持 kafka 0.10.1
```
git fetch origin pull/282/head:0.10.0
git checkout 0.10.0
```

编译
```
./sbt clean dist -sbt-launch-repo http://repox.gtan.com:8078/
```
安装
```
unzip target/universal/kafka-manager-1.3.2.1.zip -d /opt/
cd /opt/kafka-manager-1.3.2.1
```

修改 config/application.conf


启动
```
nohup bin/kafka-manager -Dconfig.file=conf/application.conf >/dev/null -J-server 2>&1 &
```

参考 http://www.yangbajing.me/playing-play/more/sbt-install.html
 
