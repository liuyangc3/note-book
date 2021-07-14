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
        endpoint            = coalescelist(aws_eks_cluster.this[*].endpoint, [""])[0]
        cluster_auth_base64 = coalescelist(aws_eks_cluster.this[*].certificate_authority[0].data, [""])[0]
        pre_userdata = lookup(
          var.worker_groups_launch_template[index],
          "pre_userdata",
          local.workers_group_defaults["pre_userdata"],
        )
        additional_userdata = lookup(
          var.worker_groups_launch_template[index],
          "additional_userdata",
          local.workers_group_defaults["additional_userdata"],
        )
        bootstrap_extra_args = lookup(
          var.worker_groups_launch_template[index],
          "bootstrap_extra_args",
          local.workers_group_defaults["bootstrap_extra_args"],
        )
        kubelet_extra_args = lookup(
          var.worker_groups_launch_template[index],
          "kubelet_extra_args",
          local.workers_group_defaults["kubelet_extra_args"],
        )
        },
        lookup(
          var.worker_groups_launch_template[index],
          "userdata_template_extra_args",
          local.workers_group_defaults["userdata_template_extra_args"]
        )
      )
    )
  ]
  ```
