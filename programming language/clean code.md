1 坚持使用最直观的编码方式，而不是追求代码简短.

你需要思考左边是 true 右边是 false
```js
// bad
expr ? expr1 ? cond1 : cond2 : cond3
 
// good
if (expr) {
  cond1
} else {
  cond2
}
```

```python
// bad        
[i if i == 1 else i + 1 for i in list]

// good
for i in list:
    if i % 2 == 0:
        r.append(i)
    else:
        r.append(i + 1)
```
