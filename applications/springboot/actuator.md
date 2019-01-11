






## info

## httptrace

## metrics


## prometheus

添加依赖
```
compile group: 'io.micrometer', name: 'micrometer-registry-prometheus', version: '1.1.1'
```
请求地址
```
curl http://localhost:8080/actuator/prometheus
```
返回内容
```
# HELP hikaricp_connections_active Active connections
# TYPE hikaricp_connections_active gauge
hikaricp_connections_active{pool="HikariPool-1",} 0.0
# HELP jvm_buffer_total_capacity_bytes An estimate of the total capacity of the buffers in this pool
# TYPE jvm_buffer_total_capacity_bytes gauge
jvm_buffer_total_capacity_bytes{id="direct",} 114815.0
jvm_buffer_total_capacity_bytes{id="mapped",} 0.0
# HELP jvm_threads_peak_threads The peak live thread count since the Java virtual machine started or peak was reset
# TYPE jvm_threads_peak_threads gauge
jvm_threads_peak_threads 53.0
# HELP jvm_buffer_count_buffers An estimate of the number of buffers in the pool
# TYPE jvm_buffer_count_buffers gauge
jvm_buffer_count_buffers{id="direct",} 13.0
jvm_buffer_count_buffers{id="mapped",} 0.0
# HELP rabbitmq_consumed_total  
# TYPE rabbitmq_consumed_total counter
rabbitmq_consumed_total{name="rabbit",} 0.0
# HELP hikaricp_connections Total connections
# TYPE hikaricp_connections gauge
hikaricp_connections{pool="HikariPool-1",} 10.0
# HELP process_files_open_files The open file descriptor count
# TYPE process_files_open_files gauge
process_files_open_files 135.0
...
```

配置 prometheus scrape 收集信息

# nginx
deny 外部方式这个 uri
```
location /actuator {
  deny all;
}
```
