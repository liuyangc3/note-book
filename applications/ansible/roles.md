## Role dependencies
store role dependencies in the `meta/main.yml` makes dependency roles run before the currnet role.

use `import_role` in task you can control the running order.

## Role variables
By default, the playbook will override the value of the variable, which has the same name but defined in different roles.

set `ANSIBLE_PRIVATE_ROLE_VARS=true` to avoid this, see https://github.com/ansible/ansible/issues/68922
