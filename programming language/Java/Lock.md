CAS 和 Lock

乐观和悲观



# CAS
```
[lock] cmpxchg reg_src, reg_dsst/mem

[lock]     optional 'prefix' (used for SMP)
cmpxchg    mnemonic opcode 操作码 助记词
reg_src    source operand
reg_dst    destination operand
```
