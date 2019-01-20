# greedy algorithms



问题: 有N个物品, 每个重量不同,价格也不同,假如只能带走`m`kg 的物品,如何选择价值最大?

三种策略

- 重量优先
- 价值优先
- 平均值优先


解决

1 定义问题

对于每个物品记为i, i ∈ I 

- 重量 <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;w_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;w_i" title="w_i" /></a>
- 价值 <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;w_i" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;v_i" title="v_i" /></a>
- K 总重量

那么问题就可以定义为: 找到一个I的子集,使得子集内所有元素

- 总重量不大于 K
- 总价值的最大 (大于其他子集)


决定变量



把问题边界
