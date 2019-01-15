# 回文串

## 判断回文串 # 125
忽略标点,大小写


思路, i 从左边向右移动, j 从右边向左移动

每次移动后, 当 i 和 j 是字母或数字时, 比较i和j
```java
class Solution {
    public boolean isPalindrome(String s) {
       if (s.length()==0) {return true;}
        
        for(int i = 0, j = s.length() - 1; i<j; ++i, --j) {
            while(i<j && !isValid(s.charAt(i))) {++i;}
            while(i<j && !isValid(s.charAt(j))) {--j;}
            if(Character.toUpperCase(s.charAt(i)) != Character.toUpperCase(s.charAt(j))) {return false;}
        }   
        return true;
    }
    
    private boolean isValid(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9');
    }   
}
```

## 回文数字 #9
例如 121, 1221 是, -121 不是, 要求不能把数字转为字符串

思路: 当前数字 每次 除 10, 计算回文数字, 当前数字小于回文数字时(位数小于),说明回文串长度超出了一半.

伪代码思路
```java
x = 120021, y = x % 10 = 1

x = x/10 = 12002
x % 10 = 2
y = 10 * y + 2 = 12

x = x/10 = 1200
x % 10 = 0
y = 10 * y + 0 = 120 

x = x/10 = 120 
x % 10 = 2
y = 10 * y + 2 = 1202
x < y
```

```java
```
