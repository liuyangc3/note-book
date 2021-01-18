```yaml

- name: task template
  debug: 
  check_mode: yes  # --check -C
  changed_when: bool or expr # define a task is changed
  diff: bool
  ignore_errors: bool
  failed_when: bool or expr # define a task how to fial
  register: name # put output in a var name
  
  when: bool or expr
  failed_when: bool or expr
  changed_when: bool or expr
```

when
```
# and
when:
  - a
  - b
  
# or
when: >
 a or
 b
```
