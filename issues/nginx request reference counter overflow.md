log
```
2017/02/12 15:36:46 [crit] 16645#0: *18272011 request reference counter overflow while processing "/a.html"
while sending to client, client: 10.212.11.253, server: x.nxin.com, request: "GET /b.html
HTTP/1.1", subrequest: "/xxx.html", upstream: "http://xxxx:8080/a.html", host: "x.nxin.com"
```

src/http/ngx_http_core_module.c
```
if (r->main->count >= 65535 - 1000) {
        ngx_log_error(NGX_LOG_CRIT, r->connection->log, 0,
                      "request reference counter overflow "
                      "while processing \"%V\"", uri);
        return NGX_ERROR;
}
```

http://mailman.nginx.org/pipermail/nginx-devel/2015-August/007259.html
http://nginx.org/patches/attic/chunked/patch-nginx-chunked.txt
