
# service

## Cluster IP
环境 https://www.katacoda.com/courses/kubernetes/networking-introduction
创建 service 默认类型 cluster IP， 可以从集群内部通过cluster ip 访问 service

```console
kubectl describe svc webapp1-clusterip-svc 
Name:              webapp1-clusterip-svc
Namespace:         default
...
Type:              ClusterIP
IP:                10.96.49.63
Port:              <unset>  80/TCP
TargetPort:        80/TCP
Endpoints:         10.32.0.5:80,10.32.0.6:80
```
可以看到 cluster ip 负载均衡到2个pod上 10.96.49.63 -> 10.32.0.5:80,10.32.0.6:80

如果 kube-porxy 是iptables mode，kube-proxy 会在 nat table 的 PREROUTING chain 创建 iptables 规则 .
```console
$ iptables -nvL -t nat

Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
   10   918 KUBE-SERVICES  all  --  *      *       0.0.0.0/0            0.0.0.0/0            /* kubernetes service portals */

Chain KUBE-SERVICES (2 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 KUBE-SVC-MOFD5WH2RW6MNEJH  tcp  --  *      *       0.0.0.0/0            10.96.49.63          /* default/webapp1-clusterip-svc: cluster IP */ tcp dpt:80

Chain KUBE-SVC-MOFD5WH2RW6MNEJH (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 KUBE-SEP-XZSXSKAGWEX3WTAR  all  --  *      *       0.0.0.0/0            0.0.0.0/0            statistic mode random probability 0.50000000000
    0     0 KUBE-SEP-YMZLCE5DPP2AQ75P  all  --  *      *       0.0.0.0/0            0.0.0.0/0 
    
Chain KUBE-SEP-XZSXSKAGWEX3WTAR (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 KUBE-MARK-MASQ  all  --  *      *       10.32.0.5            0.0.0.0/0           
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp to:10.32.0.5:80
```

实际上这个负载策略是:
```
KUBE-SERVICES -> KUBE-SVC-MOFD5WH2RW6MNEJH(10.96.49.63:80) -> KUBE-SEP-XZSXSKAGWEX3WTAR(10.32.0.5:80)
                                                          |->  KUBE-SEP-YMZLCE5DPP2AQ75P(10.32.0.6:80)
                                                          
```

从路由表可以看到 10.32.0.0/24 是走了 weave 设备
```
$ ip route
default via 172.17.0.1 dev ens3 
10.32.0.0/24 dev weave  proto kernel  scope link  src 10.32.0.1
```


```console
$ brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.0242726c905a       no
weave           8000.3a83358b1e51       no              vethwe-bridge
                                                        vethwepl1249f9d
                                                        vethwepl1c7c031
                                                        vethwepl3097bf7
                                                        vethwepl3a95fa2
                                                        vethweple0c32e5
```

## Node Port

Node Port 和 Cluster IP 的 iptables 很相似， 区别是 kube-proxy 会创建一个进程侦听在 Node Port 上（Cluster IP不会创建进程），不过需要注意的是：

- 即便kube-proxy进程死掉，流量也能继续转发到pod上
- 如果kill掉这个kube-proxy进程，自己启动的进程如果侦听在相同的端口，那么流量同样会通过iptables转发给Pod，而不会经过进程

无论端口是否占用，流量仍然会转发的pod，但是这个kube-proxy进程还是有意义的

- node 上其他进程 无法 listen 个端口，避免进程使用后出错
- node 上其他进程 socket请求随机端口不会使用到这个端口，避免流量意外转发到pod上


# pod to pod 


容器网络通信运行时调用 CNI 接口 Container Network Interface,CNI 有很多实现, 

flannel 是内置的, 还有 calico , cannel (calico+flannel) 等等

## flannel
支持多种方式 vxlan udp, udp 性能稍差, vxlan 已经在内核实现

简单记录下大致过程, 后面有空在补全

每个 Node 上有 flanneld 进程, 从 apiserver 拉取网络配置的网段, 然后每个 Node 分配一个子网段

这些分配好的子网段会写回 etcd, 这样每个Node上的 flannel 就知道其他 Node 的网段

同时会在 Node 上创建一个 bridge 设备 一个flannel vtep 设备 

当一个 Node上的 Pod 去往其他 Node Pod 的 packet 会先发到本Node 的 brige 上

因为是去往其他Node的流量,bridge 把包转发给 flannel 设备

flannel 能通过 apiserver(存在 etcd) 知道这个目的ip 在哪个 Node 上, 然后使用不同的封装方式封装, 发包

接收方 Node 的flannel解包, 根据路由表在转给 bridge, bridge 在转给 pod 


