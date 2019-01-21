思想, O(1) 存取 kv 对,  使用一个 M size array 保存 value, 使用 hash 函数将 key 映射为正整数, 然后作为 array index.
```js
index = hash(key)  // hash function
value = array[index]
```

# hash function
有如下几种实现

## division Method
如果 有 M 个 key v 对, 需要size M 的数组

根据 key 的类型有不同的 hash function 的实现

1 正整数

hashing 整数最常见的方式是取模运算, array size M 设为质数,  运算函数是 `key % M`,  M 是大质数取模计算冲突会减小.

2 浮点数

可以乘以一个数消除小数点,再取模,但这样会导致一些bit影响权重大,另一些没有影响.  一般拿浮点数二进制表示作为key 进行取模.

3 字符串

一般转化为大整数取模, R是小质数, (java用 31)
```java
int hash = 0;
for (int i = 0; i < s.length(); i++)
    hash = (R * hash + s.charAt(i)) % M;
```

为什么 31 ? 31 是 Mersenne prime, Mersenne数是 2^n -1, 31 是 2^5 - 1, 用 mersenne 可以较快实现乘法, 因为2次幂可以用右移实现, 如 `31 * hash = hash >> 5 - 1`


4 对象

Java Object , 用 `hashCode()`, 一个32位整数 , Python 是 `__hash__`.
32位hashcode 通过 `& 0x7fffffff` 去掉符号位,变成31位的 unsgined 正整数

## multiplication Method

```js
KA = key * A  //  0 < A < 1
hash(key) = floor(m * (KA  - floor(KA))
```
floor 表示取整, `KA  - floor(KA)` 表示取 KA 的小数部分, 也可用 `KA % 1`表示

乘法哈希法的一个优点是对 m 的选择没有什么特别的要求，一般选择它为 2 的某个幂次，这是因为我们可以在大多数计算机上更方便的实现该哈希函数。

虽然这个方法对任何的 A 值都适用，但对某些值效果更好，最佳的选择与待哈希的数据的特征有关。Don Knuth 认为 A ≈ (√5-1)/2 = 0.618 033 988... 比较好，可称为黄金分割点。

## universal hash
todo 

# collision resolution
不同的key 通过hash 函数得到的值可能相同, 这就叫hash冲突, 如果hash 函数将 N 个 KEY 值映射到 M 个整数上(M >= N), 那么这个函数就是  `Perfect Hash Function` 即没有冲突,
如果 M == N, 就叫 Minimal Perfect Hash Function

这种完美hash,可以减少存储空间, 通常需要知道 key的 集合, 通过特定算法生成hash 函数, 而我们日常编程使用的都是不确定 key的. 所以会遇到冲突问题

全域哈希 Univeral Hashing 可以设计完美hash

collision 一般有几种解决方法

## Chaining 链接法
链表, key 冲突了就存到链表的下一个节点

```
+---+    +---+    +---+   
| 0 | -> | X | -> | Y |
+---+    +---+    +---+   
| 1 |
+---+
| 2 |
+---+    +---+
| 3 | -> | Z |
+---+    +---+
  . 
```

## Open Addressing 开放寻址法

主要思想是当出现冲突后, 用 probe 找个一个空的位置,把值存入

这个 probe 方式有

1 linear probe 线性探查
```js
hash(k, j) = (_hash(k) + j) % m    // 0 <= j <= m-1  
```

2 quadratic probing 二次探查

todo





# 一些应用

## bloom filter 布隆过滤器
bitmap 记录,  内置多个 hash 函数, 原理是

bitmap 数组置0, 假设3个hash 函数 `h1,h2,h3`,  插入一个 key 会得到 3个index,   将 bitmap 3个位置改为 1.

查询 key 是否在bitmap里, 只有被这3个函数映射到的bit位全部是1才能说明x可能存在. 
因为bitmap 上的一个 1 可能不同 key 造成的, 所以 key 存在有误报,  key 不存在(即bitmap里每个hash index 的位置都是 0) 是准确的.

减少误报 需要用更多的 hash 函数.

## cuckoo hash  
https://www.cs.cmu.edu/~binfan/papers/conext14_cuckoofilter.pdf

http://codecapsule.com/2013/07/20/cuckoo-hashing/

CMU 发明,基本思想是使用2个hash函数来处理碰撞，从而每个key都对应到2个位置


## consistent hashing 一致性 hash
MIT 提出的分布式hash, 空间范围 [0, 2^32 -1], 是个环形空间, 即 2^32 是 0.

每个分布式 node hash 后, 会在环上的一个位置, 插入的数据 hash 后也会有位置, 数据index < 右边第一个节点index 的 就被记录属于这个节点.

加入新节点后, 只影响 新节点 到 左边节点间的数据.删除也同理

结点数小, 或者分布不均匀, 会造成 某个node 上 key 多 , 其他的少, 解决思路是加虚拟结点

例如节点 A B C, 虚拟节点是2, 那么添加 A1, A2, B1, B2, C1, C2, 落到 A1 A2 上的key,都属于 A

# refs
https://algs4.cs.princeton.edu/34hash/

https://www.cs.cmu.edu/afs/cs/academic/class/15210-s14/www/lectures/hash.pdf
