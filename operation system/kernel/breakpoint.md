breakpoint 指令，在 x86_64 平台 opcode 是 `int3`, `0xCC` 1 byte ，会出发 Cpu Trap



## 



## why 1 byte
http://www.cs.columbia.edu/~junfeng/09sp-w4118/lectures/int3/int3.txt




Kprobes 在注册了一个 kprobe 后，复制被探测的指令，并且把被探测指令的第一个字节替换为断点指令（例如：在 i386、x86_64 平台上的 int3）。
