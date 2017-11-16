
http.Handler 接口
```go
type Handler interface {
	ServeHTTP(ResponseWriter, *Request)
}
```

http.HandlerFunc 实现了接口 Handler
```go
type HandlerFunc func(ResponseWriter, *Request)

// ServeHTTP calls f(w, r).
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
	f(w, r)
}
```

```go
// Handle registers the handler for the given pattern
// in the DefaultServeMux.
// The documentation for ServeMux explains how patterns are matched.
func Handle(pattern string, handler Handler) { DefaultServeMux.Handle(pattern, handler) }

// HandleFunc registers the handler function for the given pattern
// in the DefaultServeMux.
// The documentation for ServeMux explains how patterns are matched.
func HandleFunc(pattern string, handler func(ResponseWriter, *Request)) {
	DefaultServeMux.HandleFunc(pattern, handler)
}
```
Handle 第二个参数是接口 Handler， 而 HandleFunc 参数是函数


https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/

# code
```go
tr := &http.Transport{
	TLSClientConfig:    &tls.Config{RootCAs: pool},
	DisableCompression: true,
}

client := &http.Client{
	Transport: tr,
	CheckRedirect: redirectPolicyFunc,
}

req, err := http.NewRequest("GET", "http://example.com", nil)

resp, err := client.Do(req)
...
```

call traing
```go
(c *Client) Do(req *Request)
    |
    |---- send(req *Request, t RoundTripper)
            |
            |---- (t *Transport) RoundTrip(req *Request)
```




# timeout
```
<-------- Client.Do --------------
+------+  +---------------+
| Dial |  | TLS handshake | | Request | | Resp.Headers

```