最近发现 EKS pod 无法解析域名

排查 /etc/resolv.conf 中 nameserver 的值为 `172.20.0.10` 与 coreDNS 的 ClusterIP 不一致。


# /etc/resolv.conf 是怎么来的？

EKS node userdata 会调用脚本 `/etc/eks/bootstrap.sh` https://github.com/awslabs/amazon-eks-ami/blob/3616f1da5dab0cc6256ee60df4a0e5f2d8a42684/amazon-eks-nodegroup.yaml#L661

terraform eks module 则会直接调用
https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/templates/userdata.sh.tpl#L7


https://github.com/terraform-aws-modules/terraform-aws-eks/blob/e6d76d0a069c0192bdace25e992e54709b667e5c/local.tf
```hcl
launch_template_userdata_rendered = [
    for index in range(var.create_eks ? local.worker_group_launch_template_count : 0) : templatefile(
      lookup(
        var.worker_groups_launch_template[index],
        "userdata_template_file",
        lookup(var.worker_groups_launch_template[index], "platform", local.workers_group_defaults["platform"]) == "windows"
        ? "${path.module}/templates/userdata_windows.tpl"
        : "${path.module}/templates/userdata.sh.tpl"
      ),
      merge({
        platform            = lookup(var.worker_groups_launch_template[index], "platform", local.workers_group_defaults["platform"])
        cluster_name        = coalescelist(aws_eks_cluster.this[*].name, [""])[0]
...
        bootstrap_extra_args = lookup(
          var.worker_groups_launch_template[index],
          "bootstrap_extra_args",
          local.workers_group_defaults["bootstrap_extra_args"],
        )
...
      )
    )
  ]
  ```
默认情况下 bootstrap_extra_args 应该为 ""


在 bootstrap.sh 中可以看到 
```
if [[ -z "${DNS_CLUSTER_IP}" ]]; then
  if [[ ! -z "${SERVICE_IPV4_CIDR}" ]] && [[ "${SERVICE_IPV4_CIDR}" != "None" ]] ; then
    #Sets the DNS Cluster IP address that would be chosen from the serviceIpv4Cidr. (x.y.z.10)
    DNS_CLUSTER_IP=${SERVICE_IPV4_CIDR%.*}.10
  else
    MAC=$(get_meta_data 'latest/meta-data/network/interfaces/macs/' | head -n 1 | sed 's/\/$//')
    TEN_RANGE=$(get_meta_data "latest/meta-data/network/interfaces/macs/$MAC/vpc-ipv4-cidr-blocks" | grep -c '^10\..*' || true )
    DNS_CLUSTER_IP=10.100.0.10
    if [[ "$TEN_RANGE" != "0" ]]; then
      DNS_CLUSTER_IP=172.20.0.10
    fi
  fi
else
  DNS_CLUSTER_IP="${DNS_CLUSTER_IP}"
fi

KUBELET_CONFIG=/etc/kubernetes/kubelet/kubelet-config.json
echo "$(jq ".clusterDNS=[\"$DNS_CLUSTER_IP\"]" $KUBELET_CONFIG)" > $KUBELET_CONFIG
```

可以看到 DNS_CLUSTER_IP 获取流程是

先从命令行参数 `-dns-cluster-ip` 获取IP， 如果没有检查参数 --b64-cluster-ca and --apiserver-endpoint 如果没有这2个参数，describe eks 获取 DNS service IP

如果有 --b64-cluster-ca and --apiserver-endpoint（terraform eks module 会传入这2个参数，则不会得到 DNS service IP，最后取默认值）

默认值给 172.20.0.10



see also 
- https://github.com/awslabs/amazon-eks-ami/issues/636
- https://github.com/awslabs/amazon-eks-ami/issues/639

# how to change 
```
worker_groups_launch_template = [
    {
      name                    = "spot-1"
      override_instance_types = ["m5.large", "m5a.large", "m5d.large", "m5ad.large"]
      bootstrap_extra_args    = "--dns-cluster-ip xxxxx"
    },
  ]
 ```
