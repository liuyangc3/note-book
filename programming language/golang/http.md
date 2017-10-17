
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