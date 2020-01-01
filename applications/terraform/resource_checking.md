# issue
for instance if you passing a wrong prarameter until accutlly terraform run the code through the prodiver APIs.

for example:
```hcl
resource "alicloud_vswitch" "vswith" {
  name              = "foo"
  vpc_id            = "your_vpc_id"
  cidr_block        = "10.0.0.0/10"
  availability_zone = "fake_zone"
```
if availability_zone or cidr_block is wrong, event they can be pass through the `terraform plan`,
you will get error when runing `terraform apply`.

event worse you pass a right prarameter but not accutlly you expect(for example typo), your resource created success, so you need to pay.

# solution 

the easy way to is that do some checks before accutlly apply anything.

and I use external resource to implement this.
```hcl
locals {
  config = {
    region = "cn-hanghzou"
    availability_zone = "cn-hanghzou-a"
    vpc_id = ...
    ...
  }
}

data "external" "check_instance_prarameters" {
  program = ["python3", "${path.module}/ecs_instance_check.py",
    jsonencode(local.config)
  ]
}
```

and in `ecs_instance_check.py` we can do some checks in it.

```python
import sys
import json

def reurn_result(ok):
    resp = {}
    if ok:
        resp["result"] = "OK"
        print(json.dumps(result))
        sys.exit(0)
    else:
        resp["result"] = "Wrong"
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)


prarameters = josn.loads(sys.argv[1])

# do some checks
region = prarameters['region']
zone = prarameters['availability_zone']
...

reurn_result(True)
```

