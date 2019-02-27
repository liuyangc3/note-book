http://www.cs.virginia.edu/~evans/cs216/guides/x86.html
translate http://www.cnblogs.com/YukiJohnson/archive/2012/10/27/2741836.html

# asm
普遍 asm 只能写指令,扩展 asm 可以指定操作数
```c
__asm__ __volatile__(assembly template
        : output operand list 
        : input operand list
        : clobber registers list
                            );
```

assembly template 汇编语句模板，用双引号引起来, 多条语句用 `;` 或者 `\n\t` 来分隔。
里面是汇编指令

%0 %1 占位符, 引用后面的 operand, 双%% 可以指定寄存器 例如 %%eax

operand list 操作数，都是 `"constraint"(operand)` 的形式， var 可以是任意内存变量
constraint  一般是下面这些标识符

- a,b,c,d,S,D 分别代表 eax,ebx,ecx,edx,esi,edi 寄存器
- r 上面的寄存器的任意一个（谁闲着就用谁）
- m 内存
- i 立即数（常量，只用于输入操作数）
- g 寄存器、内存、立即数 都行 
- `=` 表示只写 write-only

constraint 约束操作数使用的内存模型,例如具体的寄存器,内存

output operands 必须是只写的, 即要有 `=` 

clobber registers 告诉gcc 哪些寄存器是我们自己使用的, gcc 不会把值存入它们, 如果有 "memory", 跨指令时,GCC 不会在寄存器保存 memory value cache

`__volatile__`  creates a compiler level memory barrier forcing optimizer to not re-order memory accesses across the barrier.

https://stackoverflow.com/questions/14950614/working-of-asm-volatile-memory

```c
int main() {
    int v1 = 10;
    int v2 = 20;
    int result;
    __asm__ ("imull %1, %2\n\t"
             "movl %2, %0"
            : "=r"(result) // 占位符从0开始编号，result就是%0
            : "r"(v1), "r"(v2) // v1 %1  v2 %2
            ); 
    // 翻译过来
    // imull v1, v2
    // movl  v2, result 
    printf("the result is %d\n", result);
    return 0;
}
```



# CAS

AT &T
```
[lock] cmpxchg reg_src, reg_dst/mem

[lock]     optional 'prefix' (used for SMP)
cmpxchg    mnemonic opcode 操作码 助记词
reg_src    source operand
reg_dst    destination operand
```
Compares the value in the `AL`, `AX`, `EAX`, or `RAX` register with the first operand (destination operand). If the two
values are equal, the second operand (source operand) is loaded into the destination operand. Otherwise, the
destination operand is loaded into the AL, AX, EAX or RAX register. 

可以看到 reg_dst 先和 eax 比较, 虽然指令里 操作数没写 eax, 实际使用过程中用到了


注意 Intel 中 源操作数和目的操作数的地址是反的


CPU core之间通过MESIF协议保证数据一致性


# refs
http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html

http://heather.cs.ucdavis.edu/~matloff/50/PLN/lock.pdf

https://zhuanlan.zhihu.com/p/24146167

https://www.zhihu.com/question/31816461/answer/53424604

https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf  3-181

https://github.com/1184893257/simplelinux/blob/master/inlineasm.md