```yaml

- name: task template
  debug: 
  check_mode: yes  # --check -C
  changed_when: bool or expr # define a task is changed
  diff: no
  ignore_errors: no
  register: name # put output in a var name
```
