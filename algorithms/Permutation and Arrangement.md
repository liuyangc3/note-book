# Permutation 


求 A={1,2,3}的全排列

## Method 1
链接：https://leetcode-cn.com/problems/permutations/solution/quan-pai-lie-by-leetcode-solution-2/

可以看出
- 第一个位置3选择一
- 当第一个位置选择1后, 下一个位置从 [2,3] 中 2选一
- 当第一和第二选择[1, 2] 后, 下一个位置从 [3] 中选一, 只能是3


可以用树形结构表示这个选择过程,最终结果是树的所有**子叶节点**
```

                      []
        /              |             \
      [1]             [2]             [3]
   /       \       /      \        /      \
 [1,2]   [1,3]   [2,1]   [2,3]   [3,1]   [3,2]
   |       |       |       |       |       |
[1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

深度遍历树的过程中，我们需要记录已经选中的数字，我们可以用一个状态数组记录下标来表示是否被选中，
把选中的数字放入结果中，然后递归遍历数组
```python3
def permutation(array: list) -> list:
    result = []  # 全排列结果集 
    selected = [False] * len(array) #  selected[i] 为 True 表示这个下标被选中了
    currnet = [] # 表示当前选中数字

    # 递归 深度遍历
    dfs(array, current，selected, result)
    return result
    
```
下面构造递归函数

```python3
def dfs(array, current, selected, result):
    # 当选中数字长度达到数组长度后，说明已经到子叶节点
    # 添加结果到结果集并退出函数
    if len(current) == len(array):
        result.append(current.copy())
        return

    for i in range(len(array)):
        if selected[i]:
            # 说明当前数字上一步选中了，略过
            continue

        # 选中数字中加入一个数字
        current.append(array[i])
        selected[i] = True
        dfs(array, current, selected, result)
        # 当 i 这个数字完成遍历后，需要清理 i 的选中标记
        # 这样下个循环 i 仍然是未选中的
        # 回溯之前的状态
        selected[i] = False
        current.pop()

```

回溯法: 一种通过探索所有可能的候选解来找出所有的解的算法。如果候选解被确认不是一个解的话（或者至少不是最后一个解），回溯算法会通过在上一步进行一些变化抛弃该解，即回溯并且再次尝试。


## Method 2
