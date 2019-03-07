有一个长度N的字符串S, 给出一个任意数字 k,  从S中移除一个字串, 使得剩余的字符串内, 刚好有k个不同的字符, 求这个字串的最短长度

1. Given S = "abaacbca" and K = 2, your function should return 3. After removing substring "cbc", string S will contain exactly two different characters: a and b.

2. Given S = "aabcabc" and K = 1, your function should return 5. After removing "bcabc", string S will contain exactly one character: a.

3. Given S = "zaaaa" and K = 1, your function should return 1. You can remove only one letter: z.

4. Given S = "aaaa" and K = 2, your function should return −1. There is no such substring of S that, after removal, leaves S containing exactly 2 different characters.

Write an efficient algorithm for the following assumptions:

- N is an integer within the range [1..1,000,000];
- string S consists only of lowercase letters (a−z);
- K is an integer within the range [0..26].
