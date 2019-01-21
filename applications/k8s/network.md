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


