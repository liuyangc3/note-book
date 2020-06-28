Doubly Linked List
------------------
Linux 内核实现了一套双向链表，在<include/linux/list.h>中可以找到：
```c
struct list_head {
    struct list_head *next, *prev;
};
```
它的结构看起来是这样的:
```
  ┌───────────┐   ┌───────────┐   ┌───────────┐
  │ list_head │   │ list_head │   │ list_head │
  ├───────────┤   ├───────────┤   ├───────────┤
┌>│   next    ├──>│   next    ├──>│   next    ├─┐
│ ├───────────┤   ├───────────┤   ├───────────┤ │
│┌┤   prev    │<──┤   prev    │<──┤   prev    │<┼┐
││└───────────┘   └───────────┘   └───────────┘ ││
└┼──────────────────────────────────────────────┘│
 └───────────────────────────────────────────────┘
```
它与一般的链表实现有所不同，例如
```c
struct List {
    int  data;
    List *next;
    List *prev;
}
```
一般来说，链表结构体包含一个指向数据的指针，而 Linux 内核的实现是一种被称为侵入式的链表（Intrusive list），
这种链表并不在链表结构中包含数据，而仅提供用于维护前向与后向访问结构的指针。
这种实现方式使得链表数据结构非常通用，因为它并不需要关注链表所维护的具体数据类型。

例如：
```c
struct node {
    int data;
    struct list_head list;
}
```

源码里后面紧接着链表的初始化：
```c
#define LIST_HEAD_INIT(name) { &(name), &(name) }

#define LIST_HEAD(name) \
	struct list_head name = LIST_HEAD_INIT(name)
```
和
```c
static inline void INIT_LIST_HEAD(struct list_head *list)
{
	list->next = list;
	list->prev = list;
}
```
LIST_HEAD(name) 是宏声明，一般静态声明一个链表用这种方式。

INIT_LIST_HEAD 是函数，运行时初始化链表，注意参数是指针

添加节点
----
```c
static inline void __list_add(struct list_head *new,
                  struct list_head *prev,
                  struct list_head *next)
{
    next->prev = new;
    new->next = next;
    new->prev = prev;
    prev->next = new;
}

static inline void list_add(struct list_head *new, struct list_head *head)
{
    __list_add(new, head, head->next);
}

static inline void list_add_tail(struct list_head *new, struct list_head *head)
{
    __list_add(new, head->prev, head);
}
```
提供了2个函数

使用例子
----

```c
#include <stdio.h> 
#include <string.h>
#include <linux/list.h> 

struct person {
    int age;
    char name[15];
    struct list_head list;
};

void main(int argc, char* argv[]) {
    struct person *pperson;
    struct person person_head;
    struct list_head *pos, *next;
    
    // 初始化双链表的表头
    INIT_LIST_HEAD(&person_head.list);
    
    // 添加节点
    pperson = (struct person*)malloc(sizeof(struct person));
    pperson->age = 20;
}
```