解析摩尔码 part 1  https://www.codewars.com/kata/54b724efac3d5402db00065e/train/python

6 kyu

`..--` 表示一个字符, 每个字符直接用一个space分割, 例如`..-- --..`,  单词间的空格是 三个space

```python
def decodeMorse(morse_code):
    words = morse_code.strip().split("   ")
    res = []
    for morse_word in words:
        word = ""
        for code in morse_word.split():
            word += MORSE_CODE[code]
        res.append(word)
    return " ".join(res)
```
