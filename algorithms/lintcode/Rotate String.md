8 Rotate String

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


