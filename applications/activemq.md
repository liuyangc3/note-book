# client/connection/session id

SessionId was in regards to whether its normal for several different consumers to have the exact same value in that column.
```
connectionId = ID:`hostname`-32812-1380176571908-1:1
clientId = ID:`hostname`-32812-1380176571908-0:1
``` 
* 32812 随机值
* 1380176571908 时间戳毫秒

 
# queue
Dispatched Queue represents the number of messages assigned to a given consumer.
 
Dequeue represents the number of messages actually consumed and acked by the client.
