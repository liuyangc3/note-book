最近发现 EKS pod 无法解析域名

排查 /etc/resolv.conf 中 nameserver 的值为 `172.20.0.10` 与 coreDNS 的 ClusterIP 不一致。


# /etc/resolv.conf 是怎么来的？

EKS node userdata 会调用脚本 `/etc/eks/bootstrap.sh` https://github.com/awslabs/amazon-eks-ami/blob/3616f1da5dab0cc6256ee60df4a0e5f2d8a42684/amazon-eks-nodegroup.yaml#L661

