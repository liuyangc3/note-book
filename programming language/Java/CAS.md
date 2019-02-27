CAS 和 Lock 区别

乐观, CAS 不会锁住值, 先比较, 值没变,才会写入新值

Lock 是悲观锁模式

# CAS
伪代码
```
compare_and_swap (*p, expect, update):
      if (*p == expect)
          *p = update;
          success;
      else
         fail;
```

```java
public final boolean compareAndSet(int expect, int update) {
    return unsafe.compareAndSwapInt(this, valueOffset, expect, update);
    // compareAndSetInt JDK9
}

// var1 = this, var2 = valueOffset, var4 = expect, var5 = update
public final native boolean compareAndSetInt(Object var1, long var2, int var4, int var5);


// unsafe.cpp
UNSAFE_ENTRY(jboolean, Unsafe_CompareAndSetInt(JNIEnv *env, jobject unsafe, jobject obj, jlong offset, jint e, jint x)) {
  oop p = JNIHandles::resolve(obj);
  
  jint* addr = (jint *)index_oop_from_field_offset_long(p, offset);
  // e = expect, x = update
  return (jint)(Atomic::cmpxchg(x, addr, e)) == e;
} UNSAFE_END
```
JDK 实现
```c++
inline jint Atomic::cmpxchg(jint exchange_value,
                            volatile jint* dest,
                            jint compare_value) {
  int mp = os::is_MP();
  __asm__ volatile (LOCK_IF_MP(%4) "cmpxchgl %1,(%3)"
                    : "=a" (exchange_value)
                    : "r" (exchange_value), "a" (compare_value), "r" (dest), "r" (mp)
                    // cc 表示asm代码可以修改 condition code register
                    // 前面的 LOCK_IF_MP 宏用了 cmp 指令
                    : "cc", "memory");
  return exchange_value;
}

```
LOCK_IF_MP(mp)
```c 
// Adding a lock prefix to an instruction on MP machine
#define LOCK_IF_MP(mp) "cmp $0, " #mp "; je 1f; lock; 1: "

// same as
cmp $0, " #mp ";   // cmp 会修改 condition code register
je 1f; // 向后搜索 label 1:, 跳转过去
lock;
1:    // label 1:
cmpxchgl %1,(%3)
```
mp 是 0 跳转到 cmpxchgl %1,(%3), mp 大于 0, 即多核, lock 给总线上锁，令物理处理器的其他核心不能通过总线访问


```c
// %0 使用 eax, 变量 exchange_value (update)
: "=a" (exchange_value)  
// %1 exchange_value, %2 compare_value, %3 dest, %4 mp
: "r" (exchange_value), "a" (compare_value), "r" (dest), "r" (mp)

cmpxchgl exchange_value,(dest)
```
`