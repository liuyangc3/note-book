解析化学表达式  5 kyu
```
input  'H2O'
output {H: 2, O: 1}

input  'Mg(OH)2'
output {Mg: 1, O: 2, H: 2}

input  'K4[ON(SO3)2]2'
output {K: 4, O: 14, N: 2, S: 4}
```
算法第四版 1.3(p128) 讲了用 stack 进行四则运算 (Dijkstra in the 1960s uses two stacks)


通过观察可以发现 大写开头字母表示元素名`Element`, 后面紧跟一个数字 `n` 表示个数, n = 1 时可以省略 n, 每个元素和其他元素是加法运算求和
```
H2 -> {H: 2}
O -> {O: 1}
H2O -> {H: 2} + {O: 1} = {H: 2, O: 1}

Mg2H2OCO2
Mg 2 + H 2 + O 1 + C 1 + O 2 = {Mg: 2, H: 2, O: 3, C: 1}
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

然后实现一个 dict 加法
```python
def plus(d1, d2):
    for k, v in d1.items():
        d2[k] = v + d2.get(k, 0)
    return d2
```

带括号的表达式
```
(OH)2 = (O1 + H1) * 2 = {O:2, H2}

[ON(SO3)2]2 = (O1 + N1 + (S1 + O3) * 2) * 2 
            = (O1 + N1 + {S2, O6}) * 2
            = {O: 14, N: 2, S: 4}
```
通过观察表达式可以知道, 运算只有加法和乘法,而乘法都是发生在反括号结束时

括号内的元素也都是加法, 所以用栈保存元素 和 括号起始的元素`(``[``{`即可

每当遇到反括号时, 相加括号内的元素, 结果在乘以外面的数字, 结果在放入栈

遍历完成后 栈里所有元素相加即可.

最后的答案
```python
def parse_molecule(formula):
    elements = []

    def parse_element(idx):
        element = formula[idx]
        while idx + 1 < len(formula) and formula[idx + 1].islower():
            element += formula[idx + 1]
            idx += 1
        count, idx = parse_count(idx)
        elements.append({element: count})
        return idx

    def parse_count(idx):
        digit = ''
        while idx + 1 < len(formula) and formula[idx + 1].isdigit():
            digit += formula[idx + 1]
            idx += 1
        count = 1 if digit == '' else int(digit)
        return count, idx

    def plus(d1, d2):
        for k, v in d1.items():
            d2[k] = v + d2.get(k, 0)
        return d2

    i = 0
    while i < len(formula):
        if formula[i].isupper():
            i = parse_element(i)

        elif formula[i] == '(' or formula[i] == '[':
            elements.append('(')

        elif formula[i] == ')' or formula[i] == ']':
            # 先计算 () 之间的加法, 结果入栈
            e = elements.pop()
            while e != '(':
                res = plus(e, elements.pop())
                e = elements.pop()
                elements.append(res)

            # 获取反括号后面的乘数, 并进行乘法运算, 结果入栈
            count, i = parse_count(i)
            e = elements.pop()
            for k, v in e.items():
                e[k] = v * count
            elements.append(e)

        i += 1

    result = {}
    for e in elements:
        result = plus(result, e)

    return result
```



