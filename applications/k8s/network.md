
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

如果 kube-porxy 是iptables mode
```console
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


容器网络通信运行时调用 CNI 接口 Container Network Interface,CNI 有很多实现, 

flannel 是内置的, 还有 calico , cannel (calico+flannel) 等等

# flannel
支持多种方式 vxlan udp, udp 性能稍差, vxlan 已经在内核实现

简单记录下大致过程, 后面有空在补全

每个 Node 上有 flanneld 进程, 从 apiserver 拉取网络配置的网段, 然后每个 Node 分配一个子网段

这些分配好的子网段会写回 etcd, 这样每个Node上的 flannel 就知道其他 Node 的网段

同时会在 Node 上创建一个 bridge 设备 一个flannel vtep 设备 

当一个 Node上的 Pod 去往其他 Node Pod 的 packet 会先发到本Node 的 brige 上

因为是去往其他Node的流量,bridge 把包转发给 flannel 设备

flannel 能通过 apiserver(存在 etcd) 知道这个目的ip 在哪个 Node 上, 然后使用不同的封装方式封装, 发包

接收方 Node 的flannel解包, 根据路由表在转给 bridge, bridge 在转给 pod 


