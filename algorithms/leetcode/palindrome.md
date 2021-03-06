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

这个题比回文串多了一个可以删除1位, 可以向右跳过 i 或者 向左跳过 j 两种情况, 判断跳过后的字符串是否是回文串即可

```java
class Solution {
    public boolean validPalindrome(String s) {
        for(int i=0,j=s.length()-1;i<j;i++,j--) {
            if(s.charAt(i) != s.charAt(j)) {
                return isPalindrome(s, i + 1, j) || isPalindrome(s, i, j - 1);
            }
        }
        return true;
    }

    public boolean isPalindrome(String s, int start, int end) {
        for(int i=start,j=end;i<j;i++,j--)
            if(s.charAt(i) != s.charAt(j)) return false;
        return true;
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
        int len = 0, mid = 0;
        for(int i = 0;i < 128; ++i) {
            if(m[i]> 0) {
                if(m[i] % 2 == 0) {
                    // char 个数是偶数个,那么当前能构造最长
                    // 回文的长度就是 char 的个数
                    len += m[i];
                } else {
                    // 奇数-1 变成偶数, 同理
                    len += m[i] - 1;
                    // 是奇数, 说明最后可以在回文中间放一个
                    mid = 1;
                }
            } 
        }
        return len + mid;       
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

其实也不能确切地说是反转链表, 是链表的值的顺序反转回来, 保存值的形式不一定是链表, 我们可以用数组或者栈保存值.

这里用 stack 保存.
```java
class Solution {
    public boolean isPalindrome(ListNode head) {
        Stack<Integer> st = new Stack<>();
        if(head == null) {return true;}
        if(head.next ==  null) {return true;}
        
        // loop half of linklist
        ListNode i= head , j = head;
        while(true) {
 
            if(j.next == null) {
                // i on middle of linklist
                // donet need save i to stack
                break;
            }
            if(j.next.next == null) {
                // i on left of middle
                st.push(i.val);
                break;
            }
            st.push(i.val);
            i = i.next;
            j = j.next.next;
        }
        
        while(i.next != null) {
            i = i.next;
            if(i.val != st.pop()) return false;
        }
        return true;
    }
}
```


进阶, 要求 O(n) 时间复杂度和 O(1) 空间复杂度. 不能使用栈保存元素了

只能修改原链表, 把左边的部分反转, 然后对比左右
```java
class Solution {
    public boolean isPalindrome(ListNode head) {
         if (head == null || head.next == null) {
            return true;
        }
        
        // loop half of linklist
        ListNode i = head , j = head;
        while(j.next != null && j.next.next != null) {
            i = i.next;
            j = j.next.next;
        }
        
        // reverse right part            
        ListNode pre = null, n = null;
        while(i.next != null) {
            n = i.next;
            i.next = pre;
            pre = i;
            i = n;
        }
        i.next = pre;
        
        while(i.next != null) {
            if(i.val != head.val) return false;
             i = i.next;
             head = head.next;
        }
        return true;
    }
}
```

## 回文子串 #647

给定一个字符串，计算这个字符串中有多少个回文子串, 具有不同开始位置或结束位置的子串，即使是由相同的字符组成，也会被计为是不同的子串。

简单思路, 暴力遍历子串, 然后判断字串是不是回文, 并记录到hashset里.

```java
class Solution {
    public int countSubstrings(String s) {
        int res = 0;
        HashSet<String> set = new HashSet<>();
        for(int i=0; i < s.length(); ++i) {
            for(int j = i; j < s.length(); ++j) {
                String sub = s.substring(i, j + 1);
                
                if (set.contains(sub)) {
                    res++;
                } else if (isPalindrome(sub)) {
                    set.add(sub);
                    res++;
                }
            }
        }
        return res;
    }
    
    private boolean isPalindrome(String s) {
        char[] array = s.toCharArray();
        int i = 0, j = array.length - 1;
        while(i < j) {
            if(array[i] != array[j]) {
                return false;
            }
            ++i;
            --j;
        }
        return true;
    }
}
```

思路2

观察可以发现, 如果 `S` 是一个长度 n 回文,  那么  `xSy` 是回文的条件是  x == y, 那么我们可以从字符串中点开始,向两边检查.

S 长度为奇数, 左右起始点就是 s 里当前字符串的位置, 然后依次探测两边即可/

但是如果 S 长度为偶数,左右起始点就是 S最左边和S最右边. 可以通过一种方法把偶数变成奇数,例如在每个 char 之间插入一个 `#`

```
ab -> a#b,  abba -> a#b#b#a#
```
这样中点就成了 `#`

```java
class Solution {
    public int countSubstrings(String s) {
        int res = 0;
        char[] array = transform(s).toCharArray();
        
        for (int i = 0; i < array.length; ++i) {
            for (int left = i, right = i; left >= 0 && right < array.length; --left, ++right) {
                if (array[left] == array[right]) {
                    //  # 不能算作回文次数
                    if(array[left] != '#') res++;
                } else {
                    break; // stop check left and right
                }
            }
        }
        return res;
    }

    private String transform(String s) {
        StringBuilder buf = new StringBuilder();
        for (int i = 0; i < s.length(); ++i) {
            buf.append(s.charAt(i)).append("#");
        }
        // remove last #
        buf.delete(buf.length() - 1, buf.length());
        return buf.toString();
    }
}
```
思路3 Manacher 算法

## 最长回文子串 #5
输入: "babad", 输出: "bab"

思路: 上一题是返回回文字串总个数, 而本题目是返回 回文字串里的最长的那个字串. 感觉大同小异.

也是找出所有的字串, 然后返回长度最大的.



