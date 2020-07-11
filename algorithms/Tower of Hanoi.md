
an example of HanoiTower
```
     |      <---- a rod
     |
   | 0 |    <---- rings on rod
  |  1  |
 |   2   |
|    3    |
```

The goal of the game is to move all the rings to the destination rod. The rules are simple:

- You can only move 1 ring at a time.
- A ring cannot be put on top of a smaller ring.

so begin state of 4 rings of HanoiTower, **F**rom **B**uffer **T**o is the rod.
```
     F          B          T     
     |          |          |     
   | 0 |        |          |     
  |  1  |       |          |     
 |   2   |      |          |     
|    3    |     |          |   
```
and the finall state will be
```
     F          B          T     
     |          |          |     
     |          |        | 0 |   
     |          |       |  1  |  
     |          |      |   2   | 
     |          |     |    3    |
```

**把起点n个盘子移动到终点** 的问题可以递归为

- 把起点n-1个盘子移动到缓冲区 （子问题）
- 把1个盘子从起点移到终点
- 把缓冲区n-1个盘子也移到终点 （子问题）

所以我们可以把移动步骤转化为函数
```
move(n, from, to, buffer)  表示把 n 个盘子从 from 移动到 to， 使用 buffer 当缓冲区
```
那么问题就可以描述成
```
move(n-1, from, buffer, to)
move(1, from, to, buffer)
move(n-1, buffer, to, from)
```

最终代码
```python
rings = 0
state = {'F': [], 'B': [], 'T': []}

def hanoi_tower(r: int):
    global state
    global rings
    rings = r
    state = {
        'F': list(range(rings)),
        'B': [],
        'T': []
    }
    move(rings, 'F', 'T', 'B')


def move(n, f, t, buff):
    # move n rings from `f` rod to `t` rod with `buffer` as templar rod
    if n == 0:
        return
    if n == 1:
        # move v from f -> t
        v = state[f].pop(0)
        dest = state[t]
        state[t] = [v] + dest

    else:
        # reserve 1 ring of f rod, move rest rings to `buff` rod
        move(n - 1, f, buff, t)
        # move reserved 1 ring from `f` to `t` rod
        move(1, f, t, buff)
        # move rest rings from `buff` to `t`
        move(n - 1, buff, t, f)

hanoi_tower(4)
```

为了更直观的展示这个过程，我写了个 draw 函数
```python

def draw():
    towers = []
    pad = " " * (rings + 1)
    for rod, rod_rings in state.items():
        layers = []  # each line of rod to print
        # add header
        layers.append(f'{pad}{rod}{pad}')
        layers.append(f'{pad}|{pad}')

        # add body rings layers, the body total has `rings` layers
        body = []
        len_rod_rings = len(rod_rings)
        for i in range(rings):
            # find current layer whether has a ring
            if i < rings - len_rod_rings:
                # draw a rod
                body.append(f'{pad}|{pad}')
            else:
                # draw a ring in this layer
                index = i - rings + len_rod_rings  # index of ring
                ring = rod_rings[index]
                layer = draw_ring(ring, rings + 1)
                body.append(layer)

        layers.extend(body)
        towers.append(layers)

    # draw each tower, pad 1 space between each tower
    layers = [''] * (2 + rings)
    for t in towers:
        for i in range(2 + rings):
            layer = t[i]
            layers[i] += layer
    for layer in layers:
        print(layer)


def draw_ring(ring, pad_len):
    """
    _ for outside pad, whitespace for internal pad

    __|  1  |__
    _|   2   |_
    |    3    |
    """
    outer = " " * (pad_len - ring - 2)
    inner = " " * (ring + 1)  # pad_len - outer - 1
    layer = f'{outer}|{inner}{ring}{inner}|{outer}'
    return layer
```

outputs
```
     F          B          T     
     |          |          |     
   | 0 |        |          |     
  |  1  |       |          |     
 |   2   |      |          |     
|    3    |     |          |     
move "0" from F -> B
     F          B          T     
     |          |          |     
     |          |          |     
  |  1  |       |          |     
 |   2   |      |          |     
|    3    |   | 0 |        |     
move "1" from F -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
 |   2   |      |          |     
|    3    |   | 0 |     |  1  |  
move "0" from B -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
 |   2   |      |        | 0 |   
|    3    |     |       |  1  |  
move "2" from F -> B
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
     |          |        | 0 |   
|    3    | |   2   |   |  1  |  
move "0" from T -> F
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
   | 0 |        |          |     
|    3    | |   2   |   |  1  |  
move "1" from T -> B
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
   | 0 |     |  1  |       |     
|    3    | |   2   |      |     
move "0" from F -> B
     F          B          T     
     |          |          |     
     |          |          |     
     |        | 0 |        |     
     |       |  1  |       |     
|    3    | |   2   |      |     
move "3" from F -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |        | 0 |        |     
     |       |  1  |       |     
     |      |   2   | |    3    |
move "0" from B -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
     |       |  1  |     | 0 |   
     |      |   2   | |    3    |
move "1" from B -> F
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
     |          |        | 0 |   
  |  1  |   |   2   | |    3    |
move "0" from T -> F
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
   | 0 |        |          |     
  |  1  |   |   2   | |    3    |
move "2" from B -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
   | 0 |        |      |   2   | 
  |  1  |       |     |    3    |
move "0" from F -> B
     F          B          T     
     |          |          |     
     |          |          |     
     |          |          |     
     |          |      |   2   | 
  |  1  |     | 0 |   |    3    |
move "1" from F -> T
     F          B          T     
     |          |          |     
     |          |          |     
     |          |       |  1  |  
     |          |      |   2   | 
     |        | 0 |   |    3    |
move "0" from B -> T
     F          B          T     
     |          |          |     
     |          |        | 0 |   
     |          |       |  1  |  
     |          |      |   2   | 
     |          |     |    3    |

```
