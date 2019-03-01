解析化学表达式  5 kyu
```
input  'H2O'
output {H: 2, O: 1}

input  'Mg(OH)2'
output {Mg: 1, O: 2, H: 2}

input  'K4[ON(SO3)2]2'
output {K: 4, O: 14, N: 2, S: 4}
```
算法第四版 1.3(p128) 讲了用 stack 进行四则运算 ( Dijkstra in the 1960s uses two stacks)


通过观察可以发现 大写开头字母表示元素名`Element`, 后面紧跟一个数字 `n` 表示个数, n = 1 时可以省略 n
```
H2O  -> H 2 + O 1 = {H: 2, O: 1}
Mg2H2OCO2 -> Mg 2 + H 2 + O 1 + C 1 + O 2 = {Mg: 2, H: 2, O: 3, C: 1}
```

首先需要解析 `Element n` 元素表达式
```python
def parse_molecule(formula):
    def parse_element(idx):
        element = formula[idx]
        while idx + 1 < len(formula) and formula[idx + 1].islower():
            element += formula[idx + 1]
            idx += 1

        count, idx = parse_count(idx)
        print({element: count})
        return idx

    def parse_count(idx):
        digit = ''
        while idx + 1 < len(formula) and formula[idx + 1].isdigit():
            digit += formula[idx + 1]
            idx += 1
        count = 1 if digit == '' else int(digit)
        return count, idxt: count})
        return idx

    i = 0
    while i < len(formula):
        if formula[i].isupper():
            i = parse_element_expr(i)
        i += 1
```
```bash
$ print(parse_molecule('H2O'))

{'H': 2}
{'O': 1}
```
