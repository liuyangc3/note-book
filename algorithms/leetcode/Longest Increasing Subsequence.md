# 300

动态规划

找到前 i 个数的 最长子序列的转移方程, 例如

[10,9,2,5,3,7,101,18]


dp(0) - `[10]`, 所以 dp(0) = 1

dp(1) - `[10, 9]`, 9 比 10 小,  dp(1) = 1

dp(2) - `[10, 9, 2]`, 2 比 9 小, dp(2) = 1

dp(3) - `[10, 9, 2, 5]`, 5 比 2 大, dp(3) = dp(2) + 1

dp(4) - `[10, 9, 2, 5, 3]`, 3 比 5 小, 但是 3 比 2 大, dp(4) = dp(2) + 1

dp(5) - `[10, 9, 2, 5, 3, 7]`, 7 比 2, 5, 3 都大, dp(4) = max(dp(2),dp(3),dp(4)) + 1 = dp(4) + 1

dp(6) - `[10, 9, 2, 5, 3, 7, 101]`, 101 比 2, 5, 3, 7 都大, dp(4) = max(dp(2),dp(3),dp(4),dp(5)) + 1 = dp(5) + 1

dp(7) -`[10, 9, 2, 5, 3, 7, 101, 18]` 18 比 2, 5, 3, 7 大,  dp(7) = max(dp(2),dp(3),dp(4),dp(5)) + 1 = dp(5) + 1


```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] dp = new int[nums.length];
        int result = 0;
        for(int i=0;i<nums.length;i++) {
            dp[i] = 1;
            for(int j=0;j<i;j++) {
                if(nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j]+1);
                }
            }
            result = Math.max(result, dp[i]);
        }
        return result;
    }
}
```
