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
z = x % 10 = 2
y = 10 * y + z = 12

x = x/10 = 1200
z = x % 10 = 0
y = 10 * y + z = 120 

x = x/10 = 120 
z = x % 10 = 2
y = 10 * y + z = 1202
x < y
```
需要注意一些边界条件, 例如
- 100 这样以`0`结尾的肯定不是回文
- x 长度是偶数时, 最后一次迭代后 y 长度比 x 多一位
- x 长度是奇数时, 最后一次迭代后 y 长度等于 x.

```java
class Solution {
    public boolean isPalindrome(int x) {
        if(x < 0){return false;}
        if(x < 10) {return true;}
        
        int y = x % 10; 
        if(y == 0){return false;}
        while(y < x) {
            x /= 10;
            y = 10 * y + x % 10;
        }
        return x == y || x == y / 10;
    }
}
```

## 回文串2 #680
给定非空字符串a-z, 可以删除一个字符,判断是否是回文, 例如 'abca' 是, 因为可以删除 c or b

这个题比回文串多了一个可以删除1位, 感觉可以在回文的基础上, i,j 对比后如果不等, 跳过1次, 继续对比

```java
class Solution {
    public boolean validPalindrome(String s) {
        for(int i = 0, j = s.length() - 1; i < j; ++i, --j) {
            if(s.charAt(i) != s.charAt(j)) {
                // 当出现不一致的情况后
                // 右移 i 看剩下的是否是回文
                boolean result_move_i = true;
                for(int x= i + 1, y = j ; x < y; ++x, --y) {
                     if(s.charAt(x) != s.charAt(y)) {
                         result_move_i = false;
                         break;
                     }
                }
                // 右移动是回文, 返回结果
                if(result_move_i) return true;
                
                //右移不是回文, 左移 j 看剩下的是否是回文
                for(int x = i, y= j - 1; x < y; ++x, --y) {
                     if(s.charAt(x) != s.charAt(y)) {
                         return false;
                     };
                }
                return true;
            }
        }
        return true;      
    }
}
```
扩展思考, 如果可以删除 2 个呢, abc`z`cb`x`a -> abccba
```
int delCount = 2;
for (i, j ...) {
    if(s.charAt(i) != s.charAt(j)) {
        if(delCount <= 0) return false;
        ...
        // 左右移动后,子串不是回文串不能提前 retrun
        delCount--;
    }
}
```
