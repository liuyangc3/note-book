
# log status 499
```
10.201.10.250 - - [05/Feb/2017:08:09:27 +0800] "POST /person/getUserArchive/634086739144346051 HTTP/1.1" 499 0 "10.001" "-" "okhttp/3.4.1" "-" "proxy_addr:10.201.10.205:8080" proxy_status:-
```

# register hander
如果 proxy_ignore_client_abort on 则开启检测

# 499 handler
```c
ngx_http_upstream_check_broken_connection(ngx_http_request_t *r, ngx_event_t *ev) {
...
c = r->connection;
u = r->upstream;
 
// ngx_use_epoll_rdhup 表示 EPOLLRDHUP 事件，代表对端断开连接
// 如果 出现 EPOLLRDHUP 事件 直接返回499(NGX_HTTP_CLIENT_CLOSED_REQUEST)
if ((ngx_event_flags & NGX_USE_EPOLL_EVENT) && ngx_use_epoll_rdhup) {
    if (!u->cacheable && u->peer.connection) {
        ngx_log_error(NGX_LOG_INFO, ev->log, err,
                    "epoll_wait() reported that client prematurely closed "
                    "connection, so upstream connection is closed too");
        ngx_http_upstream_finalize_request(r, u,
                                        NGX_HTTP_CLIENT_CLOSED_REQUEST);
        return;
    }
  
// 没有 EPOLLRDHUP 事件，读取 1 个字节
n = recv(c->fd, buf, 1, MSG_PEEK);
if (n > 0) { return;}
if (n == -1) { ... return;}
  
// n < -1 的情况
  
// 处理请求的过程中，若 Nginx 服务器主动向上游服务器建立连接，完成连接建立并与之进行通信，这种相对Nginx 服务器来说是一种主动连接，
// 主动连接由结构体 ngx_peer_connection_t 表示 所以 u->peer.connection 表示 upstream 连接仍然还在
if (!u->cacheable && u->peer.connection) {
    ngx_log_error(NGX_LOG_INFO, ev->log, err,
                  "client prematurely closed connection, "
                  "so upstream connection is closed too");
    ngx_http_upstream_finalize_request(r, u,
                                       NGX_HTTP_CLIENT_CLOSED_REQUEST);
    return;
}
```



# rc
- NGX_OK — Server was selected.
- NGX_ERROR — Internal error occurred.
- NGX_BUSY — no servers are currently available. This can happen due to many reasons, including: the dynamic server group is empty, all servers in the group are in the failed state, or all servers in the group are already handling the maximum number of connections.
- NGX_DONE — the underlying connection was reused and there is no need to create a new connection to the upstream server. This value is set by the keepalive module.

https://nginx.org/en/docs/dev/development_guide.html#http_load_balancing
