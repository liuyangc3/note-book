```c
eumu Season {
  Spring,
  Summer,
  Autumn,
  Winter
};
```
相当于声明了4个整形常量。
第一个值默认为0，后面的依次加1.

技巧
----
```c
typedef enum {
    FlagNone = 0, // not use
    FlagA = 1 << 0,
    FlagB = 1 << 1,
    FlagC = 1 << 2,
    FlagD = 1 << 3
    // bit map
    // FlagD FlagC FlagB FlagA
} Flags;

int main() {
    Flag f = FlagA | FlagC; // 0101 = 5
    if (f == 5) {printf("set A and C");}
    return 0;
}
```
