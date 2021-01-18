```yaml

- name: task template
  debug: 
  check_mode: yes  # --check -C
  diff: no
  ignore_errors: no
  register: name # put output in a var name
```
