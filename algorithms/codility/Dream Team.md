https://app.codility.com/programmers/challenges

有2个长度N的数组 A, B, 给出一个数子 m, m<N,
从 A 中选择 m 个数字,记录下标 k1,k2...km,  从 B 中选择剩余下标的数字. 使得 m 个数字 + N -m 个数字的和最大. 返回这个最大值


例如
```
m = 2
A = [4, 2, 1] , B = [2, 5, 3]

A 取 [4, 0, 1]   // 0 表示不选择
B 取 [0, 5, 0]

sum = 10
```
```
m = 2
A = [7, 1, 4, 4], B = [5, 3, 4, 3]

A: [7, 0, 0, 4]
B: [0, 3, 4, 0]

sum = 18
```

首先优先从A中选m个数字, A 中选数字的策略是 i 位置上 A[i] - B[i] 差值最大, 这样才能保证和最大

假设 B 都选择得到和 sum, 那我们只需要从A中选一个,减去这个位置对应B的值即可,  即 i 选 A 后, sum += A[i] - B[i], 显然 A[i] - B[i] 最大, sum 就会最大.

```java
class Solution {
    public int solution(int[] A, int[] B, int m) {
        int[] AminusB = new int[A.length];
        int sumB = 0;
        for (int i = 0; i < A.length; i++) {
            sumB += B[i];
            AminusB[i] = A[i] - B[i];
        }
        
        Arrays.sort(AminusB);

        for (int i = A.length - 1; i > A.length - 1 - m; i--)
            sumB += AminusB[i];
        return sumB;
    }
}
```

