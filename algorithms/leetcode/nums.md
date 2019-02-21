# reverse  number
不考虑负数, 正常反转算法, 每次取末尾数字x, 下一轮 x * 10 在加上新末尾数字 x' 
```java
// 123 -> 321
int reversed = 0;
while (x > 0) {
  reversed = reversed * 10 + x % 10;
  x /= 10;
}
```
这个算法在Java里有int 越界问题, 例如 中间累加过程可能会超出 Integer.MAX_VALUE

改进

```java
int reversed = 0;
while (x > 0) {
  // 1 check  reversed * 10
  // reversed <= Integer.MAX_VALUE / 10 
  
  // 2 check (reversed * 10 + x % 10) < Integer.MAX_VALUE
  // if reversed == Integer.MAX_VALUE / 10, x % 10 sholud <= 7
  // because Integer.MAX_VALUE = 2147483647
  // if reversed < Integer.MAX_VALUE / 10, x % 10 can be any of [0-9]
  if (reversed < Integer.MAX_VALUE / 10
      || ((reversed == Integer.MAX_VALUE / 10) &&  (x % 10 <= 7))
  ) {
    reversed = reversed * 10 + x % 10;
    x /= 10;
  }
}
```
