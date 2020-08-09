Linux网络协议栈工作在2层主要有2部分,底层是设备驱动,负责和设备交互数据,上层是设备无关层,它连接了网络3/4层的协议,与各种不同功能的硬件设备,使不同的设备使用统一的方式与协议层交互.

NAPI
----
在Linux2.6.24之前, 数据包到达网卡会产生一个中断IRQ,通知CPU根据协议栈解析数据包的内容,这在低速网络时没有问题,当带宽达到GB时,网卡产生的中断可能达到每秒几千次，而如果每次中断都需要系统来处理，CPU的负载就会非常重.

NAPI的引入,将IRQ放入softirq,