TCP Header
```
20 bytes
0                1               2               3
 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8 1 2 3 4 5 6 7 8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |     4
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |     8 
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |     12
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data | Rese  |C|E|U|A|P|R|S|F|                               |
| Offset| rved  |W|C|R|C|S|S|Y|I|            Window             |     16
|       |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
|           Checksum            |         Urgent Pointer        |     20
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

flags
----
`CWR(Congestion Window Reduced)`,`ECE(ECN-Echo)`

主要用在拥塞控制,发送方的包ECE=0，表示出现了congestion；接收方回的包里CWR=1表明收到congestion信息并做了处理。[C]和[E]

`URG`

是urgent的缩写，这个位置为1的数据包要优先发送并被处理。[U]

`SYN/ACK`

这2个老生常谈，三次握手里用到,tcpdump里的写法[S] 和 [.]

`PSH`

Push,数据交给应用层处理.[P]

`FIN` 

Finish,没有数据要发送了,两边各发一个FIN,回一个ACK就可以关闭连接了[F]

`RST`

Reset 断开连接[R]



