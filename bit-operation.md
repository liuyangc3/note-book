# 位运算
2016-01-14

liuyangc33@gamil.com
## &, and, 与运算
1 and 1 = 1

1 and 0 = 0

0 and 0 = 0

n & 1 检查末尾一位是否是1,用来判断奇偶

n & k = n % (k + 1)  取余数


## |, or, 或运算
1 or 1 = 1
1 or 0 = 1
0 or 0 = 0
n | 1 最后一位变成1, 如果是偶数则 + 1
n | 0 最后一位变成0 ,如果是奇数则 - 1

## ^, xor, 异或
1 xor 1 = 0
1 xor 0 = 1
0 xor 0 = 0
可用于加密
xor运算的逆运算是它本身，也就是说两次异或同一个数最后结果不变. 即 (a xor b) xor b = a
, 明文 xor 密钥 = 密文, 密文 xor 密钥 = 明文

交换位置
```
a = a xor b
b = a xor b
a = a xor b
```

## !, not, 非
取反,假如用4位的一个数字
!n 表示上限值和n的差 !n = 1111 - n


## <<, 左移
n << b, 表示在n后面加上b个0
n << b = n * 2^b

## >>, 右移
n >> b, 表示n 去掉末尾的b位
n >> b = n / 2^b 取整, 最小值为0

## 一些应用
删除最后一位:
```
0010 1100 -> 0001 0110
x >> 1  
```
最后一位补`0`:
```
0010 1100 -> 0101 1000
x << 1
```
最后一位补`1`:
```
0010 1100 -> 0101 1001
(x << 1) + 1
```
最后一位变成1 : (101100->101101),  x | 1
最后一位变成0 : (101101->101100), x | 1 - 1
最后一位取反:  x ^ 1
把右数第k位变成1      | (101001->101101,k=3)      | x | (1 << (k-1))
把右数第k位变成0      | (101101->101001,k=3)      | x & !(1 << (k-1))
右数第k位取反         | (101001->101101,k=3)      | x xor (1 << (k-1))

从右边取3位             | (1101101->101)            | x and -> x and (2 << 3) -1

取末k位               | (1101101->1101,k=5)       | x and ((1 << k) - 1) | x % (1 << k)

取右数第k位           | (1101101->1,k=4)          | x >> (k-1) and 1

把末k位变成1          | (101001->101111,k=4)      | x or (1 << k-1)

末k位取反             | (101001->100110,k=4)      | x xor (1 << k-1)

将 x 的第 k 位(左起第一位是0)置1 ,x or (x >> n)

把右边连续的1变成0    | (100101111->100100000)    | x and (x+1)

把右起第一个0变成1    | (100101111->100111111)    | x or (x+1)
把右边连续的0变成1    | (11011000->11011111)      | x or (x-1)
取右边连续的1         | (100101111->1111)         | (x xor (x+1)) >> 1
去掉右起第一个1的左边 | (100101000->1000)         | x and (x xor (x-1))

## 计算一个数二进制 1的个数
用 and 取n最后1位，如果最后一位是1，加入count 然后n右移一位
```
def count1(n):
    count = 0
    for i in range(n.bit_length()):
        last_bit = n & 1
        if last_bit:
            count += 1
        n = n >> 1  # remove last bit
    return count
```
## 遍历整数二进制的位
```python
def bitdump(n):
    stack = []
    while n > 0:
        bit = n & 1  # get last bit
        stack.append(str(bit))
        n >>= 1      # remove last bit 
    stack.reverse()
    return "".join(stack)
```
#### Base 128 Varint 编码
如何对一个整数进行变长编码？也就是说给定的一个整数，能用1个字节存储就用一个字节的内存，需要两个字节存储就用两个字节的内存，而不是统一固定用4个字节或者8个字节。好处显然是非常明显的，特别是在二进制网络协议设计的时候，对整数进行变长编码很有必要。

protobuf关于Base 128 Varint的介绍：https://developers.google.com/protocol-buffers/docs/encoding

Base 128 Varint，为什么叫128？其实，就是因为只采用7bit的空间来存储有效数据，7bit当然最大只能存储128了。常规的一个byte是8个bit位，但在Base 128 Varint编码中，将最高的第8位用来作为一个标志位，如果这一位是1，就表示这个字节后面还有其他字节，如果这个位是0的话，就表示这是最后一个字节了，这样一来，就可以准确的知道一个整数的结束位置了

就以protobuf文档中的整数300为例，先看一下如何将300编码成二进制序列

300的二进制表示为：`1 0010 1100`，显然300这个整数只需要2个字节就可以存储了，根本不需要4个字节

第一步：从低位到高位按照7bit分开，最后不足7bit的剩余部分用0补齐。也就是：`0000010 0101100`

第二步：反转字节顺序。结果：`0101100 0000010`。这其实就是规定了字节序的问题。

第三步：填充标志位。上一步产生的二进制序列，每个组只有7个bit位，不足8bit，因为还没有加上最高位的标志位。这一步加上标志位后就是：`10101100 00000010`。这样就得到了300经过base 128 varint编码后的结果了，2个字节搞定。

用py的实现
```
def base128_varint(n, chunk_size=7):
    if n == 0:
        return [0] * 8
        
    # 第一步：从低位到高位按照7bit分开
    result = []
    stack = []
    chunk = []
    count = 1
    while n > 0:
        if not count % (chunk_size + 1):
            stack.append(chunk)
            chunk = []
        bit = n & 1
        chunk.append(bit)
        n >>= 1
        count += 1
    stack.append(chunk)

    last_chunk = stack[-1]
    stack = stack[:-1]
    if len(last_chunk) < chunk_size:
        # 最后不足7bit的剩余部分用0补齐
        last_chunk += [0] * (chunk_size - len(last_chunk))
    last_chunk.reverse()
    result.append(last_chunk)
    try:
        while 1:
            chunk = stack.pop()
            chunk.reverse()
            result.append(chunk)
    except IndexError:
        pass
        
    # 第二步：反转字节顺序
    result.reverse()
    
    # 第三步：填充标志位
    if len(result) > 1:
        result[0].insert(0, 1)
        result[-1].insert(0, 0)
    else:
        result[0].insert(0, 0)
    return result


print(base128_varint(300))
[[1, 0, 1, 0, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0]]
```
