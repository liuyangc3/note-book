声明
---
普通声明
```groovy
def printer = { line -> println line }

// same to this 
def Closure getPrinter() {
    return { line -> println line }
}
def printer = getPrinter()
```
引用声明

引用一个已经存在的函数作为闭包
```
class MultiMethodSample {
    int mysteryMethod (String value) {
        return value.length()
    }
    
    int mysteryMethod (List list) {
        return list.size()
    }
    
    int mysteryMethod (int x, int y) {
        return x+y
    }
}

MultiMethodSample instance = new MultiMethodSample()
Closure multi = instance.&mysteryMethod
```

GDK方法
-----
each 集合的每个元素传入闭包
```groovy
def res = ""
(1..5).each{
    res += it
}

// return "12345"

def map = [k1: v1, k2: v2]
map.each {elem ->
    println elem.key
    println elem.value
}
```

findAll 集合的每个元素传入闭包，将闭包的返回值为真的元素作为新集合的元素
```groovy
[2,3,4].collect {
    it > 2
}

// return [3,4]
```

collect 集合的每个元素传入闭包，将闭包的返回值作为新集合的元素
```groovy
[2,3,4].collect {
    it * 2
}

// return [4,6,8]
```


any 若有一个元素能使闭包返回真，则立即返回真


every 全部元素都能使闭包返回真，则返回真,否则返回假