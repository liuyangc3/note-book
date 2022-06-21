# bsseline performance
gp2 baseline IOPS is 3 IOPS per GB, means 100 GB gp2 volume has a baseline performance of 300 IOPS 

baseline IOPS 最小值 100 最大值 16,000, when size is 5,334 GB reached max baseline IOPS 16,000

有以下特点:
- Each volume receives an initial I/O credit balance of 5.4 million I/O credits
- Volume can accumulate I/O credits, max up to 5.4 million credits, 

# burst performance
> I/O credits represent the available bandwidth that 
 your gp2 volume can use to burst large amounts of 
 I/O when more than the baseline performance is needed.

当 IOPS 超出 baseline 时， IO credits 可以计算 brust 状态的持续时间, 公式如下
```
                                 (Credit balance)
Burst duration second  =  ----------------------------------
                            (Burst IOPS) - (Baseline IOPS)
```

IO 吞吐量
```
Throughput in MiB/s = ((Volume size in GiB) × (IOPS per GiB) × (I/O size in KiB))
```

gp2 最大吞吐量 250 MiB/s，带入公式得到至少需要 334 GiB 的size 才可以达到最高吞吐量


# Aurora
Aurora 的情况不太一样, 根据[3] 中描述，没有 IOPS 限制只有 Throughput 限制
> While using Aurora, make sure that there is technically no limit of IOPS but throughput could be limited to the underlying Aurora instance limit. For better throughput, go for a higher Aurora instance class.


# refs
- https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html
- https://aws.amazon.com/blogs/database/understanding-burst-vs-baseline-performance-with-amazon-rds-and-gp2/
- [3] https://aws.amazon.com/blogs/database/best-storage-practices-for-running-production-workloads-on-hosted-databases-with-amazon-rds-or-amazon-ec2/
