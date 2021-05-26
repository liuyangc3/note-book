# Least recently used (LRU)

* cache has fix size.
* discards the least recently used items first.


## Simple version

first thought is sort each item, from recently to least recently used. then delete least recently used item when cache is full.

let's set up a array, so head `cache[0]` is recently used item, and tail `cache[-1]` is least recently used
```python
cache = []
```

so the basic idea is sort of like this
```python
def set(k, v):
    if is_cache_full():
        delete_least_recently_used_item()
        put_v_into_cahce_head()
    else:
        put_v_into_cahce_head()
        
def get(k):
    if is_k_in_cache():
        v = get_v_from_cache(k)
        return v
    
    return None
```

## Challenges

* make set get O(1)
* single link list 
* LinkedHashMap
* python ordered dict

## Refs
https://leetcode.com/problems/lru-cache/

https://zhuanlan.zhihu.com/p/34133067

## code
```python
from typing import Any, Dict


class Node:
    def __init__(self, _next: "Node" = None, prev: "Node" = None, data: Any = None, key: Any = None) -> None:
        self.next = _next
        self.prev = prev
        self.data = data
        self.key = key


class LRUCache:
    def __init__(self, capacity: int):
        self.cache: Dict[Any, Node] = {}
        self.capacity = capacity
        self.head = Node(data=None)
        self.tail = Node(data=None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return
        node = self.cache[key]
        self._move_to_head(node)
        return node.data

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.data = value
            self._move_to_head(node)
        else:
            if len(self.cache) == self.capacity:
                self.cache.pop(self.tail.key)
                self._remove_node(self.tail)

            node = Node(key=key, data=value)
            self.cache[key] = node
            self._add_node(node)

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_node(node)

    def _add_node(self, node: Node, to_head: bool = True):
        if to_head:
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node
        else:
            # add to tail
            node.next = self.tail
            node.prev = self.tail.prev
            self.tail.prev.next = node
            self.tail.prev = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def dump(self):
        node = self.head
        result = ''
        while node:
            if node.data:
                result += str(node.data) + '->'
            node = node.next
        return result


if __name__ == '__main__':
    lru = LRUCache(4)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.put(3, 3)
    lru.put(4, 4)
    assert lru.dump() == '4->3->2->1->'
    lru.get(1)
    assert lru.dump() == '1->4->3->2->'
    lru.put(4, 6)
    assert lru.dump() == '6->1->3->2->'
```
