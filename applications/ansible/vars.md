run
```
ansible -i inventory/ec2.py tag_xxx -m gather_facts
```

Cloud provider
```
# Alicloud
"ansible_product_name": "Alibaba Cloud ECS"
"ansible_system_vendor": "Alibaba Cloud",

# AWS
"ansible_product_name": "c5.xlarge"
"ansible_system_vendor": "Amazon EC2",
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
