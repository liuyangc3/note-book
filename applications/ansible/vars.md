run
```
ansible your_remote_host -i inventory/ecs.py tag_xxx -m debug -a 'msg={{ hostvars["your_remote_host"] }}'

ansible -i inventory/ec2.py tag_xxx -m gather_facts
```

Cloud provider
```
# Alicloud
"ansible_product_name": "Alibaba Cloud ECS"
"ansible_system_vendor": "Alibaba Cloud",


"auto_release_time": "",
"availability_zone": "ap-southeast-1a",
"host_name": "zelpool-ali-hhht-00",
"id": "i-hp3eqgbem0sapkq4802h",
"image_id": "m-hp3emoz1gbxej9vt40kv",
"inner_ip_address": "",
"instance_charge_type": "PrePaid",
"instance_id": "i-hp3eqgbem0sapkq4802h",
"instance_name": "zelpool-ali-hhht-00",
"instance_type": "ecs.c5.xlarge",
"instance_type_family": "ecs.c5",
"internet_charge_type": "PayByTraffic",
"internet_max_bandwidth_in": 1500,
"internet_max_bandwidth_out": 100,
"osname": "Ubuntu  18.04 64位",
"osname_en": "Ubuntu  18.04 64 bit",
"ostype": "linux",
"vpc_id": "vpc-t4n8twv78e7ju3m4yfbjd",
"vswitch_id": "vsw-t4net2ksvqq8qim0bwwkj",
            

# AWS
"ansible_product_name": "c5.xlarge"
"ansible_system_vendor": "Amazon EC2",

"block_device_mappings": [
    {
        "device_name": "/dev/sda1",
        "ebs": {
            "attach_time": "2020-09-15T09:51:02+00:00",
            "delete_on_termination": true,
            "status": "attached",
            "volume_id": "vol-0cf2504a8294ffa45"
        }
    },
    {
        "device_name": "/dev/sdb",
        "ebs": {
            "attach_time": "2020-09-15T09:51:02+00:00",
            "delete_on_termination": false,
            "status": "attached",
            "volume_id": "vol-02489e62ae21c3019"
        }
    }
],
"ebs_optimized": true,
"ena_support": true,
"group_names": [
    "aws_ec2",
    "tag_role_btc_node"
],
"image_id": "ami-0071f6f4df15863cc",
"instance_id": "i-089f71777a4fc256b",
"instance_type": "c5.xlarge",
"key_name": "aws-ec2",
"launch_time": "2020-09-15T09:51:01+00:00",
"owner_id": "000404776716",
"placement": {
    "availability_zone": "cn-north-1a",
    "group_name": "",
    "region": "cn-north-1",
    "tenancy": "default"
},
"public_dns_name": "",
"public_ip_address": "245.201",
"public_dns_name": "",
"public_ip_address": "52.80.245.201",
"security_groups": [
  {
    "group_id": "sg-047c909fbd3aedf44",
    "group_name": "aws-sg-btc-node"
   }
],
subnet_id": "subnet-053085e6917f0dd45",
"tags": {},
"vpc_id": "vpc-09e42a662c5bcccb8",
```
Arch
```
ansible_machine": "x86_64",
"ansible_userspace_architecture": "x86_64",
"ansible_userspace_bits": "64",
```

OS
```
"ansible_os_family": "Debian",
"ansible_distribution": "Ubuntu",
"ansible_distribution_major_version": "20",
"ansible_distribution_version": "20.04",
"ansible_nodename": "hostname"
"ansible_distribution_release": "focal", # bionic
```
Python
```
"ansible_python_version": "3.8.2"
"discovered_interpreter_python": "/usr/bin/python3",
"ansible_python": {
  "executable": "/usr/bin/python3",
  "has_sslcontext": true,
  "type": "cpython",
  "version": {
    "major": 3,
    "micro": 2,
    "minor": 8,
    "releaselevel": "final",
    "serial": 0
},
  "version_info": [
    3,
    8,
    2,
    "final",
    0
  ]
},
```

User
```
"ansible_user_id": "username",
"ansible_user_shell": "/bin/bash",
"ansible_user_dir": "/home/yang",
"ansible_user_uid": 1015,
"ansible_user_gid": 1015,
"ansible_real_group_id": 1015,
"ansible_real_user_id": 1015,
```

# other
```
ansible-galaxy collection install community.general
```
