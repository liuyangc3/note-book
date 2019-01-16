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

## 最长回文串 #409
给定一个包含大写字母和小写字母的字符串，找到通过这些字母构造成的最长的回文串, 例如 `abccdd` 可以得到 `ccadd` 或 `ccbdd`, 长度是 5.

思路, 如果只算回文串长度,很简单, 计算所有出现2次字母的个数, 创建一个hashmap, 从左遍历, 字母不在map里加入map, 已经在map, 删除, 总数+2, 遍历完成后,如果map不为空, 总数在加1 

```java
class Solution {
    public int longestPalindrome(String s) {
        Map<Character,Integer> m = new HashMap<>();
        int count =0;
        for(char c: s.toCharArray()) {
            if (m.containsKey(c)) {
                count = count + 2;
                m.remove(c);
            } else {
                m.put(c, 0);
            }
        }
        return m.size() > 0 ? count + 1 : count;       
    }
}

// 优化版本, 用 array 代替 map
class Solution {
    public int longestPalindrome(String s) {
        int[] m = new int[128]; // z is 122
        for(char c: s.toCharArray()) {
            m[c]++;
        }
        int count = 0, carry = 0;
        for(int i = 0;i < 128; ++i) {
            if(m[i]> 0) {
                if(m[i] % 2 == 0) {
                    count += m[i];
                } else {
                    count += m[i] - 1;
                    carry = 1;
                }
            } 
        }
        return count + carry;       
    }
}
```
扩展思考, 不同的最长回文串的个数? 只需改动一行
```
// Solution 1
return m.size() + count;
// Solution 2
carry++;
```

## 回文链表 #234
判断一个链表是否为回文链表,例如 1->2->2->1, 返回true.
```java
public class ListNode {
    int va
    ListNode next;
    ListNode(int x) { val = x; }
}
```
思路, 若反转链表等于原链表,则是回文链表. 两个链表对比遍历到一半都相等即可返回, 所以反转的时候还要把长度也要算出来.

```java


```


进阶, 要求 O(n) 时间复杂度和 O(1) 空间复杂度.

思路, O(n) O(1) 说明只能遍历一次, 不能用map, 链表和数组不同的是,只能从左遍历, 不能访问从任意位置.

这个有点难,
```java
```
