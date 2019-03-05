# lintcode 8 Rotate String

Example 1:
```
	Input: str="abcdefg", offset = 3
	Output:"efgabcd"
	
	Explanation: 
	Given a string and an offset, rotate string by offset. (rotate from left to right)
```
Example 2:
```
	Input: str="abcdefg", offset = 0
	Output: "abcdefg"
	
	Explanation: 
	Given a string and an offset, rotate string by offset. (rotate from left to right)
```
Example 3:
```
	Input: str="abcdefg", offset = 1
	Output: "gabcdef"
	
	Explanation: 
	Given a string and an offset, rotate string by offset. (rotate from left to right)
```
Example 4
```
	Input: str="abcdefg", offset =2
	Output:"fgabcde"
	
	Explanation: 
  Given a string and an offset, rotate string by offset. (rotate from left to right)
```

挑战 O(1) 空间,原地 rotate

3 步反转

```
public class Solution {
    public void rotateString(char[] str, int offset) {
        if(str.length == 0) return;
        // offset can big than str lenth .....
        offset = offset % str.length;
	// reverse chars before offset
        reverse(str, 0, str.length - offset - 1);
	// reverse chars after offset
        reverse(str, str.length - offset, str.length - 1);
	// reverse str
        reverse(str, 0, str.length - 1);
    }
    
    public void reverse(char[] str, int start, int end) {
        for(int i=start,j=end;i<j;i++,j--) {
            char c = str[i];
            str[i] = str[j];
            str[j] = c;
        }
    }
}
```
前两次reverse和是 O(n), 后一次reverse是 O(n) 整体  O(2n) =  O(n)


# leetcode 796. Rotate String
和上面一样, 给出 2个 字符串S1,S2 , 判断其中一个是另一个的 Rolling String

1 每次S1 rolling 1个char, 将结果和S2对比, 相同返回true,  当S1 所有char rolling 完成后, 仍然不相等返回 false

根据上面的算法 每次 rolling 是O(n), rolling n 次. 所以 复杂度 O(n^2).


2 S1 + S1 如果包含 S2 则返回true,  O(n^2).
```java
class Solution {
    public boolean rotateString(String A, String B) {
        return A.length() == B.length() && (A + A).contains(B);
    }
}
```

3 Rolling Hash 

快速检验 S2 是不是 S1+S1的子串, 这里用Rabin-Karp,  还可以用KMP算法

http://courses.csail.mit.edu/6.006/spring11/rec/rec06.pdf

http://blog.teamleadnet.com/2012/10/rabin-karp-rolling-hash-dynamic-sized.html






