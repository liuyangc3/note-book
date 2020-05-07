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
